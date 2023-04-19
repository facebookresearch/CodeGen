"""
This only provices an example of training loop that can serve as basis
for others, but it's not necessary
"""
import logging
import dataclasses
import typing as tp
from pathlib import Path
import torch
from torch.nn.parallel import DistributedDataParallel as DDP

from multixp import distrib
from multixp import core
from multixp import loggers
from multixp.common import utils


logger = logging.getLogger(__name__)
# torch.backends.cudnn.benchmark = True
X = tp.TypeVar("X")
PathLike = tp.Union[Path, str]
FloatDict = tp.Dict[str, float]


# simpler to use a protocol for subclassing easily
# this is duplicated code here, but only because it is a base
# class, don't use a protocol otherwise
# pylint: disable=too-few-public-methods
class BaseTrainerProtocol(tp.Protocol):
    experiment: str
    folder: Path
    num_steps: int
    valid_every: int
    checkpoint_every: int
    device: str
    initial_checkpoint: str


@dataclasses.dataclass
class BaseTrainerConfig:
    experiment: str
    folder: Path = Path()
    num_steps: int = 100000
    valid_every: int = 100
    checkpoint_every: int = 10000
    device: str = "cpu"
    initial_checkpoint: str = ""


core.configstore.store(name="train_config", node=BaseTrainerConfig)


class BaseTrainer:
    """Basic and generic training loop for use as derived class,
    or for copying and rewritting.
    This takes care of:
    - evaluating regularly
    - checkpointing regularly
    - initializing distributed mode
    - logging from the main node, including the config
    - reloading from the last checkpoint if available in the workdir
    """

    def __init__(self, cfg: BaseTrainerProtocol) -> None:
        self.cfg = cfg
        if not dataclasses.is_dataclass(cfg):
            raise TypeError("Trainers only accept dataclasses")
        self.step = 0
        self._output_metric = ""  # for checking that it exists
        # logging
        self.hiplogger = loggers.HipLog(self.cfg.folder / "hip.log")
        self.hiplogger(
            **{x: getattr(cfg, x) for x in ["experiment", "initial_checkpoint"]}
        )
        loggers.flatten(self.cfg, sep=".")  # check that export works
        # distributed
        self.task = distrib.TaskEnv.from_env(dataloader=False)
        distrib.init()
        if self.task.world_size > 1:
            if self.cfg.device == "cpu":
                logger.warning("Switching device from cpu to cuda since world size > 1")
                self.cfg.device = "cuda"
        # log all sub parameters
        for field in dataclasses.fields(cfg):
            val = getattr(cfg, field.name)
            if dataclasses.is_dataclass(val):
                self.hiplogger.flattened({field.name: val})

    def _reload(self) -> None:
        # reload current checkpoint if wip, else load any provided model
        if self.checkpoint_path.exists():
            self.load_checkpoint()
        elif self.cfg.initial_checkpoint:
            self.load_checkpoint(Path(self.cfg.initial_checkpoint))

    @property
    def checkpoint_path(self) -> Path:
        out = Path(self.cfg.folder) / "checkpoints" / "latest.pt"
        out.parent.mkdir(parents=True, exist_ok=True)
        return out

    def train_step(self) -> distrib.SumDict:
        return distrib.SumDict()

    def valid_step(self) -> distrib.SumDict:
        return distrib.SumDict()

    def run(self) -> float:
        """Run the training, including
        regular evaluation and checkpointing
        """
        print("Start training")
        for m in self.filtered_content(torch.nn.Module).values():
            m.train()
        metrics = distrib.SumDict()
        for k in range(self.cfg.num_steps):
            last = k == self.cfg.num_steps - 1
            # training
            metrics += self.train_step()  # only the last is kept as metrics
            self.step += 1
            # valid
            if not self.step % 100:
                print(self.step, metrics.export(), flush=True)
            if not k or last or not (k + 1) % self.cfg.valid_every:
                for m in self.filtered_content(torch.nn.Module).values():
                    m.eval()
                with torch.no_grad():
                    metrics += self.valid_step()
                for m in self.filtered_content(torch.nn.Module).values():
                    m.train()
                exported = metrics.reduce().export()
                if self._output_metric and self._output_metric not in exported:
                    raise RuntimeError(
                        f"Output metric {self._output_metric} not available: {exported}"
                    )
                if self.task.is_main:
                    self.hiplogger(**exported, step=self.step)
                    self.hiplogger.write()
                metrics.clear()
            # checkpointing
            if last or not (k + 1) % self.cfg.checkpoint_every:
                self.save_checkpoint()
        return self.hiplogger.last_line().get(self._output_metric, float("inf"))  # type: ignore

    def load_checkpoint(self, filepath: tp.Optional[PathLike] = None) -> None:
        """Reload a checkpoint given a filepath"""
        if filepath is None:
            filepath = self.checkpoint_path
        content = torch.load(filepath, map_location=self.cfg.device)  # type: ignore
        logger.info(f"Loading checkpoint in {filepath}")
        for x, m in self.filtered_content(utils.StateDictable).items():  # type: ignore
            state = content["state_dicts"][x]
            if isinstance(m, DDP):
                state = {"module." + x: y for x, y in state.items()}
            m.load_state_dict(state)
        if filepath == self.checkpoint_path:
            self.step = content["step"]

    def export_checkpoint_info(self) -> tp.Dict[str, tp.Any]:
        """Exports a dictionary for checkpointing"""
        states: tp.Dict[str, tp.Any] = {}
        for x, m in self.filtered_content(utils.StateDictable).items():  # type: ignore
            if isinstance(m, DDP):
                m = m.module
            states[x] = m.state_dict()
        config = loggers.flatten(self.cfg, sep=".")
        return {"step": self.step, "state_dicts": states, "config": config}

    def save_checkpoint(self, filepath: tp.Optional[PathLike] = None) -> None:
        """Saves a checkpoint"""
        if filepath is None:
            filepath = self.checkpoint_path
        if self.task.is_main:
            content = self.export_checkpoint_info()
            torch.save(content, filepath)

    def filtered_content(self, type_: tp.Type[X]) -> tp.Dict[str, X]:
        """Iterates on modules which are attributes of the trainer"""
        out = {}
        for x, v in utils.filtered_content(self.__dict__, type_):
            name = "/".join(str(y) for y in x)
            out[name] = v
        return out


@core.main(config_path=".", config_name="base_config", version_base=None)
def main(dictcfg: core.DictConfig) -> None:
    # we assume cfg is a PretrainConfig (but actually not really)
    cfg = core.to_object(dictcfg)
    trainer = BaseTrainer(cfg)  # type: ignore
    trainer.run()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
