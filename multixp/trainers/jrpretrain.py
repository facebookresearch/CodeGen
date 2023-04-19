import logging
import time
import dataclasses
import typing as tp
from pathlib import Path
import torch
from torch.nn.parallel import DistributedDataParallel as DDP

import multixp as mxp
from multixp.interfaces import codegen
from multixp.interfaces.codegen import Batch
from .baseloop import BaseTrainer
from . import tools


# torch.backends.cudnn.benchmark = True
logger = logging.getLogger(__name__)
X = tp.TypeVar("X")
PathLike = tp.Union[Path, str]
FloatDict = tp.Dict[str, float]
TransConf = codegen.TransformerConfig


@dataclasses.dataclass
class TrainerConfig:
    experiment: str
    dataloader: codegen.DeobfCfg = dataclasses.field(
        default_factory=lambda: codegen.DeobfCfg(input_path=Path("missing"))
    )
    encoder: TransConf = dataclasses.field(default_factory=TransConf)
    decoder: TransConf = dataclasses.field(default_factory=TransConf)
    optim: codegen.OptimConfig = dataclasses.field(default_factory=codegen.OptimConfig)
    folder: Path = Path()
    num_steps: int = 10 ** 6
    valid_every: int = 10 ** 4
    checkpoint_every: int = 10 ** 4
    initial_checkpoint: str = ""
    clip_grad_norm: float = 1.0
    # resources
    device: str = "cpu"
    num_workers: int = 8


# you can access a lot of info on parameters through:
# python -m multixp.trainers.jrvision --cfg job
mxp.core.configstore.store(name="train_config", node=TrainerConfig)


class CodegenPretrainer(BaseTrainer):
    def __init__(self, cfg: TrainerConfig) -> None:
        super().__init__(cfg)
        self.cfg: TrainerConfig = cfg
        # change seed to avoid restarting from same point when reloading
        workers = cfg.dataloader.loading.num_workers
        workers = 1 if workers is None else workers
        workers *= self.task.world_size
        cfg.dataloader.seed += self.hiplogger.num_reloaded * workers
        self.dataloaders = cfg.dataloader.build()
        self.transform = cfg.dataloader.transform()
        tools.distributed_loaders_safety_check(
            self.dataloaders, lambda b: b.x  # type: ignore
        )
        self.train_stream = mxp.common.iterators.InfiniteIterator(
            self.dataloaders["train"]
        )
        # model and optim
        self.cfg.encoder._dico = self.transform.dico
        self.cfg.decoder._dico = self.transform.dico
        self.cfg.encoder._is_encoder = True
        self.cfg.decoder._is_encoder = False
        self.cfg.decoder._emb_dim_encoder = self.cfg.encoder.emb_dim
        self.cfg.encoder._emb_dim_decoder = self.cfg.decoder.emb_dim
        self.models = {
            "encoder": mxp.models.register.build(cfg.encoder),
            "decoder": mxp.models.register.build(cfg.decoder),
        }
        for name, model in self.models.items():
            model.to(cfg.device)
            if self.task.world_size > 1:
                # note: find unused parameters is used in codegen since
                # some model parameters are not always used, but that
                # may (?) increase compute time
                self.models[name] = DDP(model, find_unused_parameters=True)
                print(f"Wrapped {name} in DDP:", self.models[name])
        self.scheds = {}
        self.optims: tp.Dict[str, torch.optim.Optimizer] = {}
        params = [p for model in self.models.values() for p in model.parameters()]
        self._params = params
        opt, sched = codegen.build_optimizer(params, cfg.optim)
        self.scheds["models"] = sched
        self.optims["models"] = opt
        self.scaler: tp.Optional[torch.cuda.amp.GradScaler] = None
        if cfg.device != "cpu":
            self.scaler = torch.cuda.amp.GradScaler()
        self._reload()  # must be called for automatic reloading
        self.export_checkpoint_info()  # checking this works

    def export_checkpoint_info(self) -> tp.Dict[str, tp.Any]:
        content = super().export_checkpoint_info()
        encoder = self.models["encoder"]
        if isinstance(encoder, DDP):
            encoder = encoder.module
        content["word2id"] = dict(encoder.dico)  # type: ignore
        return content

    def train_step(self) -> mxp.SumDict:
        assert self.models["encoder"].training
        t0 = time.time()
        batch = next(self.train_stream)
        t1 = time.time()
        with torch.cuda.amp.autocast():
            data = self._step(batch)
            loss = data["loss"]
        if self.scaler is not None:
            loss = self.scaler.scale(loss)
        loss.backward()
        if self.cfg.clip_grad_norm > 0:
            if self.scaler is not None:
                for opt in self.optims.values():
                    self.scaler.unscale_(opt)
            for model in self.models.values():
                torch.nn.utils.clip_grad_norm_(  # type: ignore
                    model.parameters(), self.cfg.clip_grad_norm
                )
        lr = next(iter(self.optims.values())).param_groups[0]["lr"]
        for optimizer in self.optims.values():
            if self.scaler is not None:
                self.scaler.step(optimizer)
            else:
                optimizer.step()
        if self.scaler is not None:
            self.scaler.update()
        for optimizer in self.optims.values():
            optimizer.zero_grad()
        t2 = time.time()

        sequences = data.pop("processed_sequences")
        right_toks = data.pop("right_tokens")
        metrics = mxp.SumDict(
            {
                "sequences": sequences,
                "duration/batch": t1 - t0,
                "duration/step": t2 - t1,
            }
        )
        with metrics.summed_over(sequences):
            metrics.update({f"{x}/sequence": y for x, y in data.items()})
        with metrics.summed_over(1):
            metrics.update({f"{x}/batch": y for x, y in data.items()})
            metrics.update(epoch=self.train_stream.epoch, lr=lr)
        with metrics.summed_over(data["processed_words_y"]):
            metrics["next_tok_acc"] = right_toks
        return metrics.set_prefix("train/")

    def valid_step(self) -> mxp.SumDict:
        assert not self.models["encoder"].training
        metrics = mxp.SumDict()
        t0 = time.time()
        for batch in self.dataloaders["valid"]:
            with torch.cuda.amp.autocast():
                data = self._step(batch)
            sequences = data.pop("processed_sequences")
            right_toks = data.pop("right_tokens")
            batch_sum = mxp.SumDict(sequences=sequences)
            with batch_sum.summed_over(sequences):
                batch_sum.update({x + "/sequence": y for x, y in data.items()})
            with batch_sum.summed_over(data["processed_words_y"]):
                batch_sum["next_tok_acc"] = right_toks
            metrics += batch_sum
        metrics.update(duration=time.time() - t0)
        metrics = metrics.set_prefix("valid/")
        # add gpu memory approximation (hack to get the max instead of mean)
        # TODO move out of here
        if self.cfg.device != "cpu":
            gpu_mem = torch.cuda.max_memory_allocated() / 1024.0 ** 3
            with metrics.aggregation("max"):
                metrics.update({"#mem/GPU/max": gpu_mem})
        return metrics

    def _step(self, batch: Batch) -> tp.Dict[str, tp.Any]:
        batch.x = batch.x.T
        batch.y = batch.y.T
        batch = batch.to(self.cfg.device)

        # pylint: disable=no-member
        alen = torch.arange(
            batch.y_len.max(), dtype=torch.long, device=batch.y.device
        )  # type: ignore
        # do not predict anything given the last target word
        pred_mask = alen[:, None] < batch.y_len[None] - 1
        y = batch.y[1:].masked_select(pred_mask[:-1])
        assert len(y) == (batch.y_len - 1).sum().item()
        # encode source sentence
        enc1 = self.models["encoder"](
            "fwd",
            x=batch.x,
            lengths=batch.x_len,
            langs=None,
            causal=False,
            spans=None,
            positions=None,
        )
        enc1 = enc1.transpose(0, 1)
        # decode target sentence
        dec2 = self.models["decoder"](
            "fwd",
            x=batch.y,
            lengths=batch.y_len,
            langs=None,
            causal=True,
            src_enc=enc1,
            src_len=batch.x_len,
            spans=None,
            positions=None,
        )
        # loss
        scores, loss = self.models["decoder"](
            "predict", tensor=dec2, pred_mask=pred_mask, y=y, get_scores=False
        )
        ypred = torch.argmax(scores, dim=1)
        if not self.step % 100:
            decoder: tp.Any = self.models["decoder"]
            if isinstance(decoder, DDP):
                decoder = decoder.module
            sh = dec2.shape
            with torch.no_grad():
                scores2 = decoder.pred_layer.get_scores(
                    dec2.reshape(-1, sh[-1])
                ).reshape(sh[0], sh[1], -1)
                ypred2 = torch.argmax(scores2, dim=-1)
            print(
                f"@ @ @ @ @ At step {self.step},  checking batch output with size {batch.y.shape}"
            )
            for k, id_ in enumerate(batch._ids):
                print(
                    f"# # # Expecting ({id_}):\n{self.transform.revert(batch.y[:, k])}\n"
                )
                print(f"# # # Predicting:\n{self.transform.revert(ypred2[:, k])}\n")
                break
        # number of processed sentences / words
        out = {
            "right_tokens": (y == ypred).sum().item(),
            "loss": loss,
            "processed_sequences": batch.y_len.size(0),
            "processed_words_y": (batch.y_len - 1).sum().item(),
            "processed_words_x": (batch.x_len - 1).sum().item(),
        }
        return out


@mxp.core.main(config_path=".", config_name="base_config", version_base=None)
def main(dictcfg: mxp.core.DictConfig) -> None:
    # we assume cfg is a PretrainConfig (but actually not really)
    cfg = mxp.core.to_object(dictcfg)
    trainer = CodegenPretrainer(cfg)  # type: ignore
    trainer.run()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
