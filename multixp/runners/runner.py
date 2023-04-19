import uuid
import shutil
import logging
import datetime
import importlib
import traceback
import typing as tp
from pathlib import Path
import submitit
import omegaconf
import multixp as mxp
from multixp.common import utils
from multixp.trainers.baseloop import BaseTrainer
from .executor import (  # pylint: disable=unused-import
    DelayedExecutor as DelayedExecutor,
)


PathLike = tp.Union[str, Path]
logger = logging.getLogger(__name__)


class TrainerFunction:
    def __init__(
        self,
        name: str,
        metric: str = "",
        working_directory: tp.Optional[PathLike] = None,
    ) -> None:
        self.working_directory = (
            Path("") if working_directory is None else Path(working_directory)
        )
        self.working_directory = self.working_directory.resolve().absolute()
        self.working_directory.mkdir(parents=True, exist_ok=True)
        self.name = name
        self.metric = metric
        self._folder: tp.Optional[Path] = None  # defined later
        # copy to working_directory if not available
        if working_directory is not None:
            if "multixp" in [fp.name for fp in self.working_directory.iterdir()]:
                logger.warning(
                    f"Run dir {self.working_directory} already exists, it will **not** be updated"
                )
            else:
                logger.info(f"Copying genVarNames to {self.working_directory}")
                basepath = Path(mxp.__file__).parents[1]
                for name in ["data", "tree-sitter", "fastBPE"]:
                    assert (basepath / name).exists(), basepath / name
                    (self.working_directory / name).symlink_to(basepath / name)
                ignore = shutil.ignore_patterns("exp_*", ".git", "__pycache__", "*.pyc")
                for name in ["multixp", "codegen_sources"]:
                    assert (basepath / name).exists()
                    # dirs_exist_ok=True,
                    shutil.copytree(
                        basepath / name, self.working_directory / name, ignore=ignore
                    )

    @property
    def folder(self) -> Path:
        if self._folder is None:
            raise RuntimeError(
                "Folder is not defined if call method has not be called yet"
            )
        return self._folder

    def _trainer_cls(self, check_workdir: bool = True) -> tp.Type[BaseTrainer]:
        with utils.working_directory(self.working_directory):
            *parts, name = self.name.split(".")
            base = importlib.import_module("multixp.trainers.baseloop")
            module = importlib.import_module(".".join(parts))
            # reload to override hydra configstore
            module = importlib.reload(module)
            mod_path = Path(module.__file__).parent.absolute()  # type: ignore
            if check_workdir and not str(mod_path).startswith(
                str(self.working_directory)
            ):
                raise RuntimeError(
                    f"Running from {mod_path} but expected {self.working_directory}"
                )
        cls = getattr(module, name)
        # given we are using a different code we need to compare class to the different code...
        # but for type hints we don't care
        assert issubclass(
            cls, base.BaseTrainer
        ), "Only subclasses of BaseTrainer are supported"
        return cls  # type: ignore

    def _config(self, **kwargs: tp.Any) -> tp.Any:
        if "folder" in kwargs:
            raise ValueError(f"folder parameter is set by {self.__class__.__name__}")
        cls = self._trainer_cls(check_workdir=False)
        Config = mxp.core._get_config(cls)
        return mxp.core.instantiate(Config, **kwargs, folder="")

    def validated(self, **kwargs: tp.Any) -> "TrainerFunction":
        self._folder = (
            None  # reset folder if validated to avoid reusing a previous test folder
        )
        self._config(**kwargs)
        return self

    def get_hiplog(self) -> tp.Any:
        from multixp.loggers import hiplogs  # avoid circular imports

        loggers = list(hiplogs.HipLog.find_in_folder(self.folder))
        loggers = [hl for hl in loggers if "data/mockpretrain" not in str(hl._filepath)]
        assert len(loggers) == 1, f"Found {loggers} in {self.folder}"
        return loggers[0]

    def __call__(self, **kwargs: tp.Any) -> float:
        print(f"Running package: {mxp}")
        config = self._config(**kwargs)
        if self._folder is None:
            try:
                self._folder = submitit.JobEnvironment().paths.folder
            except RuntimeError:
                now = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
                name = f"{now}_{config.experiment}_{uuid.uuid4().hex[:6]}"
                self._folder = Path("outputs").resolve().absolute() / name
            self._folder.mkdir(exist_ok=True, parents=True)
        for name in ["multixp", "codegen_sources"]:
            logging.getLogger(name).setLevel(logging.DEBUG)
        omegaconf.OmegaConf.save(config=config, f=str(self._folder / "config.yaml"))
        assert hasattr(config, "folder")
        config.folder = self.folder
        with utils.working_directory(self.folder):
            trainer = self._trainer_cls()(config)
            trainer._output_metric = self.metric
            try:
                trainer.run()
            except Exception as e:  # pylint: ignore=broad-except
                if not self.get_hiplog().last_line():
                    raise e  # it did not even run one eval :s
                logger.warning(f"Something went wrong:\n{traceback.format_exc()}")
        return self.get_hiplog().last_line().get(self.metric, float("inf"))

    def checkpoint(self, *args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        return submitit.helpers.DelayedSubmission(self, *args, **kwargs)


def on_exception_enter_postmortem(f):
    """Decorator for triggering pdb in case of exception"""
    import pdb
    import sys
    from functools import wraps
    import traceback

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:
            traceback.print_exc()
            pdb.post_mortem(sys.exc_info()[2])
            raise

    return wrapper
