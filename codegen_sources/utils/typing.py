"""Definitions of some convenient types.
If you know better practices, feel free to submit it ;)
"""  # from nevergrad

# pylint: disable=unused-import
# structures
from concurrent.futures.process import ProcessPoolExecutor
from typing import Any as Any
from typing import Generic as Generic
from typing import Type as Type
from typing import TypeVar as TypeVar
from typing import Optional as Optional
from typing import Union as Union
from typing import NewType as NewType

# containers
from typing import Dict as Dict
from typing import Tuple as Tuple
from typing import List as List
from typing import Set as Set
from typing import Deque as Deque
from typing import Sequence as Sequence
from typing import NamedTuple as NamedTuple
from typing import MutableMapping as MutableMapping
from typing import Mapping as Mapping

# iterables
from typing import Iterator as Iterator
from typing import Iterable as Iterable
from typing import Generator as Generator
from typing import KeysView as KeysView
from typing import ValuesView as ValuesView
from typing import ItemsView as ItemsView

# others
from typing import Callable as Callable
from typing import Hashable as Hashable
from typing import Match as Match
from typing import cast as cast
from pathlib import Path as Path
from typing_extensions import Protocol as Protocol
from typing import TextIO as TextIO

# specific
PathLike = Union[str, Path]


# %% Protocol definitions for executor typing

X = TypeVar("X", covariant=True)


class JobLike(Protocol[X]):
    # pylint: disable=pointless-statement

    def done(self) -> bool:
        ...

    def result(self) -> X:
        ...


class ExecutorLikeCLS(Protocol):
    # pylint: disable=pointless-statement, unused-argument

    def submit(self, fn: Callable[..., X], *args: Any, **kwargs: Any) -> JobLike[X]:
        ...


ExecutorLike = Union[ExecutorLikeCLS, ProcessPoolExecutor]
OptExecutor = Optional[ExecutorLike]
