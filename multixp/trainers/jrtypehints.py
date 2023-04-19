from datetime import datetime
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
    dataloader: codegen.TypeInferenceIteratorConfig
    # dataloader: tp.Any
    encoder: TransConf = dataclasses.field(default_factory=TransConf)
    decoder: TransConf = dataclasses.field(default_factory=TransConf)
    optim: codegen.OptimConfig = dataclasses.field(default_factory=codegen.OptimConfig)
    folder: Path = Path()
    num_steps: int = 10000
    valid_every: int = 100
    checkpoint_every: int = 10000
    initial_checkpoint: str = ""
    clip_grad_norm: float = 1.0
    # resources
    device: str = "cpu"
    num_workers: int = 8
    defaults: tp.List[tp.Any] = dataclasses.field(
        default_factory=lambda: [{"dataloader": "cg_type"}]
    )


# you can access a lot of info on parameters through:
# python -m multixp.trainers.jrvision --cfg job
mxp.core.configstore.store(name="train_config", node=TrainerConfig)
mxp.dataloaders.register.link_to_param("dataloader")


class CodegenTrainer1(BaseTrainer):
    def __init__(self, cfg: TrainerConfig) -> None:
        super().__init__(cfg)
        self.cfg: TrainerConfig = cfg
        # change seed to avoid restarting from same point when reloading
        workers = cfg.dataloader.loading.num_workers
        workers = 1 if workers is None else workers
        workers *= self.task.world_size
        cfg.dataloader.seed += self.hiplogger.num_reloaded * workers
        # datasets
        self.dataloaders: tp.Mapping[
            str, tp.Iterable[Batch]
        ] = mxp.dataloaders.register.build(cfg.dataloader)
        # self.dataloaders["valid"] = common.iterators.PrefetchedIterable(self.dataloaders["valid"])
        self.train_stream = mxp.common.iterators.InfiniteIterator(
            self.dataloaders["train"]
        )
        tools.distributed_loaders_safety_check(
            self.dataloaders, lambda b: b.x
        )  # type: ignore
        self.tensorizer = self.cfg.dataloader.transform()
        self.dictifier = self.cfg.dataloader.dictifier()
        # model and optim
        dico = self.tensorizer.dico  # type: ignore  # this is a hack :(
        self.cfg.encoder._dico = dico
        self.cfg.decoder._dico = dico
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
        self.scaler = torch.cuda.amp.GradScaler()
        self._reload()  # must be called for automatic reloading

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
        # loss.backward()
        self.scaler.scale(loss).backward()
        if self.cfg.clip_grad_norm > 0:
            for opt in self.optims.values():
                self.scaler.unscale_(opt)
            for model in self.models.values():
                torch.nn.utils.clip_grad_norm_(  # type: ignore
                    model.parameters(), self.cfg.clip_grad_norm
                )
        lr = next(iter(self.optims.values())).param_groups[0]["lr"]
        for optimizer in self.optims.values():
            self.scaler.step(optimizer)
            # optimizer.step()
        self.scaler.update()
        for optimizer in self.optims.values():
            optimizer.zero_grad()
        t2 = time.time()

        proc_seq = data.pop("processed_sequences")
        metrics = mxp.SumDict(
            {
                "sequences": proc_seq,
                "duration/batch": t1 - t0,
                "duration/step": t2 - t1,
            }
        )
        with metrics.summed_over(proc_seq):
            metrics.update({f"{x}/sequence": y for x, y in data.items()})
        with metrics.summed_over(1):
            metrics.update({f"{x}/batch": y for x, y in data.items()})
            metrics.update(epoch=self.train_stream.epoch, lr=lr)
        return metrics.set_prefix("train/")

    def valid_step(self) -> mxp.SumDict:
        assert not self.models["encoder"].training
        metrics = mxp.SumDict()
        batcher = iter(self.dataloaders["valid"])
        while True:
            t0 = time.time()
            try:
                batch = next(batcher)
            except StopIteration:
                break
            t1 = time.time()
            with torch.cuda.amp.autocast():
                data = self._step(batch, generate=True)
            t2 = time.time()
            proc_seq = data.pop("processed_sequences")
            num_masks = data.pop("num_masks")
            exact_matches = data.pop("exact_matches")
            pred = data.pop("predicted")
            batch_sum = mxp.SumDict(
                {
                    "sequences": proc_seq,
                    "duration/batch": t1 - t0,
                    "duration/step": t2 - t1,
                }
            )
            with batch_sum.summed_over(proc_seq):
                batch_sum.update({f"{x}/sequence": y for x, y in data.items()})
            with batch_sum.summed_over(1):
                batch_sum.update({f"{x}/batch": y for x, y in data.items()})
            with batch_sum.summed_over(num_masks):
                batch_sum.update(exact_matches=exact_matches, predicted=pred)
            metrics += batch_sum
        metrics.set_prefix("valid/")
        gpu_mem = torch.cuda.max_memory_allocated() / 1024.0 ** 3
        with metrics.aggregation("max"):
            metrics.update({"#mem/GPU/max": gpu_mem})
        return metrics

    def _step(self, batch: Batch, generate: bool = False) -> tp.Dict[str, tp.Any]:
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
        _, loss = self.models["decoder"](
            "predict", tensor=dec2, pred_mask=pred_mask, y=y, get_scores=False
        )
        # number of processed sentences / words
        out = {
            "loss": loss,
            "processed_sequences": batch.y_len.size(0),
            "processed_words_y": (batch.y_len - 1).sum().item(),
            "processed_words_x": (batch.x_len - 1).sum().item(),
        }
        if not generate:
            return out
        decoder = self.models["decoder"]
        if isinstance(decoder, DDP):
            decoder = decoder.module
        generated, _ = decoder.generate(  # type: ignore
            enc1, batch.x_len, None, max_len=int(max((batch.y_len + 10) * 1.05))
        )
        total = 0
        matches = 0
        num_pred = 0
        for j in range(generated.shape[1]):
            expected, predicted = (
                self.tensorizer.revert(z[:, j]) for z in (batch.y, generated)
            )
            exp_dict, pred_dict = (
                self.dictifier.apply(w.split(" ")) for w in (expected, predicted)
            )
            parts = []
            for key, val in exp_dict.items():
                parts.append(f"{key}: {pred_dict.get(key, '#NOPRED#')} ({val})")
            # print(predicted)
            print(", ".join(parts), flush=True)
            total += len(exp_dict)
            for key, val in exp_dict.items():
                matches += val == pred_dict.get(key, "")
            num_pred += len(set(exp_dict) & set(pred_dict))
        out.update(num_masks=total, exact_matches=matches, predicted=num_pred)
        return out


@mxp.core.main(config_path=".", config_name="base_config", version_base=None)
def main(dictcfg: mxp.core.DictConfig) -> None:
    # we assume cfg is a PretrainConfig (but actually not really)
    cfg = mxp.core.to_object(dictcfg)
    trainer = CodegenTrainer1(cfg)  # type: ignore
    trainer.run()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
