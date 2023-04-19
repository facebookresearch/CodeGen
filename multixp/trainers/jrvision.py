import logging
import dataclasses
import typing as tp
from pathlib import Path
import torch
from torch.nn.parallel import DistributedDataParallel as DDP
import torch.nn.functional as F

import multixp
from multixp import core
from multixp import common
from multixp.distrib import SumDict
from .baseloop import BaseTrainer
from . import tools


# torch.backends.cudnn.benchmark = True
logger = logging.getLogger(__name__)
X = tp.TypeVar("X")
PathLike = tp.Union[Path, str]
FloatDict = tp.Dict[str, float]
Batch = tp.Tuple[torch.Tensor, torch.Tensor]


@dataclasses.dataclass
class TrainerConfig:
    experiment: str
    dataloader: tp.Any
    model: tp.Any
    optim: tools.OptimConfig = dataclasses.field(default_factory=tools.OptimConfig)
    folder: Path = Path()
    num_steps: int = 100000
    valid_every: int = 100
    checkpoint_every: int = 10000
    initial_checkpoint: str = ""
    # resources
    device: str = "cpu"
    num_workers: int = 8
    defaults: tp.List[tp.Any] = dataclasses.field(
        default_factory=lambda: [{"model": "dense"}, {"dataloader": "vision"}]
    )


# you can access a lot of info on parameters through:
# python -m multixp.trainers.jrvision --cfg job
core.configstore.store(name="train_config", node=TrainerConfig)
multixp.models.register.link_to_param("model")
multixp.dataloaders.register.link_to_param("dataloader")


class VisionTrainer(BaseTrainer):
    def __init__(self, cfg: TrainerConfig) -> None:
        super().__init__(cfg)
        self.cfg: TrainerConfig = cfg
        # datasets
        self.dataloaders: tp.Mapping[
            str, tp.Iterable[Batch]
        ] = multixp.dataloaders.register.build(cfg.dataloader)
        self.train_stream = common.iterators.InfiniteIterator(self.dataloaders["train"])
        tools.distributed_loaders_safety_check(self.dataloaders, lambda b: b[0])
        # dark magick for fitting batches and models
        cfg.model._in_shape = cfg.dataloader._in_shape
        cfg.model._out_shape = cfg.dataloader._out_shape
        # model and optim
        self.model = multixp.models.register.build(cfg.model)
        for name, model in self.filtered_content(torch.nn.Module).items():
            model.to(cfg.device)
            if self.task.world_size > 1:
                setattr(self, name, DDP(model))
        opt, sched = tools.build_optimizer(self.model.parameters(), cfg.optim)
        self.optimizer = opt
        self.lr_sched = sched
        self._reload()  # must be called for automatic reloading

    def train_step(self) -> SumDict:
        assert self.model.training
        batch = next(self.train_stream)
        data = self._step(batch)
        loss = data["loss"]
        loss.backward()
        self.optimizer.step()
        self.lr_sched.step(loss)
        self.optimizer.zero_grad()
        n_batches = data.pop("count")
        with SumDict(batches=n_batches).summed_over(n_batches) as metrics:
            metrics.update(data)
        with metrics.summed_over(1):
            metrics.update(epoch=self.train_stream.epoch)
        return metrics.set_prefix("train/")

    def valid_step(self) -> SumDict:
        assert not self.model.training
        metrics = SumDict()
        for batch in self.dataloaders["valid"]:
            data = self._step(batch)
            n_batches = data.pop("count")
            with SumDict(batches=n_batches).summed_over(n_batches) as sub:
                sub.update(data)
            metrics += sub
        return metrics.set_prefix("valid/")

    def _step(self, batch: Batch) -> tp.Dict[str, tp.Any]:
        x, y = (z.to(self.cfg.device) for z in batch)
        logits = self.model(x)
        loss = F.nll_loss(logits, y)
        preds = logits.argmax(-1)
        accuracy = preds == y
        return {"loss": loss.sum(), "acc": accuracy.sum(), "count": x.shape[0]}


@core.main(config_path=".", config_name="base_config", version_base=None)
def main(dictcfg: core.DictConfig) -> None:
    # we assume cfg is a PretrainConfig (but actually not really)
    cfg = core.to_object(dictcfg)
    trainer = VisionTrainer(cfg)  # type: ignore
    trainer.run()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
