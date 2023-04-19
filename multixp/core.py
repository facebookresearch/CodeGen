import os
import inspect
import dataclasses
import functools
import typing as tp
from pathlib import Path
import hydra
from hydra import main as main  # pylint: disable=unused-import
from hydra.core.config_store import ConfigStore
from omegaconf import DictConfig as DictConfig  # pylint: disable=unused-import
from omegaconf import OmegaConf

to_object = OmegaConf.to_object
configstore = ConfigStore.instance()


X = tp.TypeVar("X", covariant=True)
F = tp.Callable[..., X]


class Builder(tp.Protocol[X]):
    def build(self) -> X:
        ...


def _get_config(func: F[X]) -> tp.Any:
    is_cls = isinstance(func, type)
    f = func.__init__ if is_cls else func  # type: ignore
    params = tp.get_type_hints(f)
    cfg = next(iter(params.values()))
    if cfg.__module__ == "typing":  # expecting to see an optional param
        args = cfg.__args__
        assert len(args) == 2 and args[1] is type(None)  # noqa
        cfg = args[0]
    if not dataclasses.is_dataclass(cfg):
        raise TypeError(f"First parameter should be a dataclass: {cfg}")
    return cfg


class Register(tp.Generic[X]):
    def __init__(self) -> None:
        self.funcs: tp.Dict[str, tp.Tuple[tp.Any, F[X]]] = {}

    def __call__(self, name: str) -> tp.Callable[[F[X]], F[X]]:
        return functools.partial(self._register, name=name)

    def builder(
        self, name: str
    ) -> tp.Callable[[tp.Type[Builder[X]]], tp.Type[Builder[X]]]:
        """Register a builder config, i.e. a dataclass object with a build method
        to create the object
        """
        return functools.partial(self._register_builder, name=name)

    def _register_builder(
        self, builder: tp.Type[Builder[X]], name: str
    ) -> tp.Type[Builder[X]]:
        if not dataclasses.is_dataclass(builder):
            raise ValueError(f"Builder {builder} must be a dataclass")
        if not isinstance(builder, type):
            raise ValueError(f"Builder {builder} must be a class and not an instance")
        if not hasattr(builder, "build"):
            raise ValueError(f"Builder {builder} needs a 'build' method")
        self.funcs[name] = (builder, builder.build)  # type: ignore
        return builder  # type: ignore

    def _register(self, func: F[X], name: str) -> F[X]:
        if name in self.funcs:
            raise ValueError(
                f"Trying to register {func} as {name}, already got {self.funcs[name]}"
            )
        self.funcs[name] = (_get_config(func), func)
        return func

    def link_to_param(self, param: str) -> None:
        for name, (cfg, _) in self.funcs.items():
            print(f"Linking {name} to {param}: {cfg}")
            configstore.store(group=param, name=name, node=cfg)

    def build(self, cfg: tp.Any) -> X:
        if not dataclasses.is_dataclass(cfg):
            raise TypeError(f"Config should be a dataclass, got: {cfg}")
        for Cfg, build in self.funcs.values():
            if isinstance(cfg, Cfg):
                return build(cfg)
        raise TypeError(f"Could not find any config with type: {type(cfg)}")


def instantiate(Config: tp.Type[X], **kwargs: tp.Any) -> X:
    """Instantiates a config given overrides
    This script assumes the main config name to instantiate is basic_config
    """
    module = inspect.getmodule(Config)
    assert module is not None
    overrides = [f"{x}={y}" for x, y in kwargs.items()]
    rel_path = Path(os.path.relpath(module.__file__, Path(__file__).parent))  # type: ignore
    with hydra.initialize(config_path=str(rel_path.parent), version_base=None):
        cfg_ = hydra.compose(config_name="base_config", overrides=overrides)
    return to_object(cfg_)  # type: ignore
