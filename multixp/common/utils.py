import os
import contextlib
import typing as tp
from pathlib import Path

PathLike = tp.Union[str, Path]
X = tp.TypeVar("X")


@contextlib.contextmanager
def working_directory(path: PathLike) -> tp.Iterator[None]:
    """Temporarily changes the working directory"""
    cwd = Path().cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)


@tp.runtime_checkable
class StateDictable(tp.Protocol):
    """Object with a state dict. With isinstance(obj, StateDictable) we can capture
    optimizers, models and lr schedulers.
    """

    def load_state_dict(self, state: tp.Dict[str, tp.Any]) -> tp.Any:
        pass

    def state_dict(self) -> tp.Dict[str, tp.Any]:
        pass


def filtered_content(
    data: tp.Any, type_: tp.Type[X]
) -> tp.Iterator[tp.Tuple[tp.Tuple[tp.Any, ...], X]]:
    """Recursively filters the content of ontainers (dict, list, tuple) according to a given type

    Yields
    ------
    key, value
        the key is specified as a sequence of keys to reach the object, and the value is of
        the required type
    """
    containers = (dict, list, tuple)
    if isinstance(data, containers):
        if isinstance(data, dict):
            iterator: tp.Iterable[tp.Tuple[tp.Union[str, int], tp.Any]] = data.items()
        else:
            iterator = enumerate(data)
        for key, val in iterator:
            if isinstance(val, containers):
                for skey, sval in filtered_content(val, type_):
                    yield ((key,) + skey), sval
            elif isinstance(val, type_):
                yield (key,), val
    elif isinstance(data, type_):
        yield (), data
