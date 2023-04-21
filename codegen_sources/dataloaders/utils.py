import time
import json
import gzip
import dataclasses
import contextlib
import typing as tp
from pathlib import Path
import submitit
import numpy as np
import torch


B = tp.TypeVar("B", bound="Batch")
D = tp.TypeVar("D", bound="DelayedReader")
M = tp.TypeVar("M", bound="Modulo")
X = tp.TypeVar("X")

PAD_INDEX = 2  # TODO CHECK


@dataclasses.dataclass
class Batch:
    """Batch instance with fields x, y of size [B, N] and x_len, y_len of size[B]
    batch dimension and lengths can be omitted at instantiation, they will be
    filled autmatically.
    """

    x: torch.Tensor
    y: torch.Tensor
    x_len: torch.LongTensor = dataclasses.field(default_factory=torch.LongTensor)
    y_len: torch.LongTensor = dataclasses.field(default_factory=torch.LongTensor)
    # extra field for debugging
    _ids: np.ndarray = dataclasses.field(
        default_factory=lambda: np.array([], dtype=str)
    )
    # it's (or seems?) important to keep arrays and not list (if I understand
    # correctly) as lists may lead to OOM for reasons I don't get
    # more details here for more information:
    # https://github.com/pytorch/pytorch/issues/13246#issuecomment-445446603

    def __post_init__(self) -> None:
        for name in ["x", "y"]:
            val = getattr(self, name)
            # make sure to add a batch dimension if not there
            if val.ndim == 1:
                val = val.unsqueeze(0)
                setattr(self, name, val)
            # fill in sequence length
            key = name + "_len"
            if not getattr(self, key).numel():
                setattr(self, key, torch.LongTensor([val.shape[1]]))
        if not isinstance(self._ids, np.ndarray):
            self._ids = np.array(self._ids)

    def to(self, device: str) -> "Batch":
        """Creates a new instance on the appropriate device"""
        out: tp.Dict[str, tp.Any] = {}
        for field in dataclasses.fields(self):
            data = getattr(self, field.name)
            out[field.name] = data
            if isinstance(data, torch.Tensor):
                out[field.name] = data.to(device)
        return self.__class__(**out)

    def pin_memory(self: B) -> B:
        for field in dataclasses.fields(self):
            data = getattr(self, field.name)
            if isinstance(data, torch.Tensor):
                data.pin_memory()
        return self

    @classmethod
    def collate_fn(cls, batches: tp.List["Batch"]) -> "Batch":
        """Creates a new instance from several by stacking in a new first dimension
        for all attributes
        """
        if not batches:
            raise ValueError("No data to collate")
        out: tp.Dict[str, tp.Any] = {}
        for name in ["x", "y"]:
            # concat lengths
            key = name + "_len"
            data = [getattr(mf, key) for mf in batches]
            out[key] = torch.cat(data, dim=0)  # type: ignore
            # pad and concatenate data
            data = [getattr(mf, name) for mf in batches]
            max_len = max(d.shape[-1] for d in data)
            batch_size = sum(d.shape[0] for d in data)
            out[name] = torch.LongTensor(batch_size, max_len).fill_(PAD_INDEX)
            start = 0
            for d in data:
                end = start + d.shape[0]
                out[name][start:end, : d.shape[1]] = d
                start = end
        out["_ids"] = np.concatenate([b._ids for b in batches], axis=0)
        return cls(**out)

    def split(self) -> tp.Iterable["Batch"]:
        if self.x.shape[0] == 1:
            yield self  # avoid recreating the object if it's already split
            return
        for k in range(self.x.shape[0]):
            xl = self.x_len[k]
            yl = self.y_len[k]
            sl = slice(k, k + 1)
            # prefill as much as possible to make it fast
            out: tp.Dict[str, tp.Any] = dict(x_len=self.x_len[sl], y_len=self.y_len[sl])
            if self._ids.size:
                out["_ids"] = np.array([self._ids[k]])
            yield Batch(x=self.x[sl, : int(xl)], y=self.y[sl, : int(yl)], **out)


class BatchOptimizer:
    """Batch iterable optimizing the batches to hold as many tokens as possible below the
    maximum number,
    This is done by pre-fetching a buffer of batches, sorting the sequences, choosing one
    starting point then greedily grow the Batch with samples smaller and longer.
    Samples which are beyond the maximum lenght are removed.

    iterable: Iterable of Batch
        iterable of Batch instances to pull from
    max_num_tokens: int
        maximum number of tokens allowed in a batch
    buffer_size: int
        size of the number of samples to use for creating new batches
    """

    def __init__(
        self,
        iterable: tp.Iterable[Batch],
        max_num_tokens: int,
        max_sequence_length: int = 2048,
        buffer_size: int = 100,
        seed: int = 12,
    ) -> None:
        self.iterable = iterable
        self.rng = np.random.RandomState(seed)
        self.max_sequence_length = min(max_sequence_length, max_num_tokens)
        self.max_num_tokens = max_num_tokens
        self._batches: tp.List[Batch] = []
        self._buffer_size = buffer_size
        self.removed = 0
        self.timer = Timer()

    @staticmethod
    def _sort_key(batch: Batch) -> int:
        return int(batch.x_len[0])

    @staticmethod
    def _get_num_tokens(batches: tp.List[Batch]) -> int:
        max_len = max(b.x.shape[1] + b.y.shape[1] for b in batches)
        num_batches = sum(b.x.shape[0] for b in batches)
        return int(max_len) * num_batches

    def _get_length(self, ind: int) -> int:
        """lengths of a sequence (x+y)
        returns 0 if index is out of bond
        """
        if ind < 0 or ind >= len(self._batches):
            return 0
        b = self._batches[ind]
        return b.x.shape[0] + b.y.shape[0]

    def _extract(self) -> Batch:
        # start = self.rng.choice(len(self._batches))
        p = np.array([b.x_len[0] for b in self._batches], dtype=float)
        p /= sum(p)
        # favor longer sentences because batches are smaller so they aren't
        # selected as often
        start = self.rng.choice(len(self._batches), p=p)
        bounds = [start, start + 1]
        # we will loop until we cant either increase on
        # smaller sequences or on larger sequences
        lengths = [self._get_length(ind) for ind in [bounds[0] - 1, bounds[1]]]
        tentatives = 0
        while any(lengths):
            tentatives += 1
            if tentatives > len(self._batches):
                raise RuntimeError(
                    "Batch creation failed to converge\n"
                    f"{lengths=} {bounds=} {len(self._batches)=}"
                )
            # either increase by smaller seq (ind=0)
            # or larger (ind=1)
            # give more weights to larger seq since they are less likely to get
            # selected
            p = np.array(lengths, dtype=float) / sum(lengths)
            ind = self.rng.choice(2, p=p)
            tentative = list(bounds)
            tentative[ind] += -1 if not ind else 1
            num_tokens = self._get_num_tokens(
                self._batches[tentative[0] : tentative[1]]
            )
            if num_tokens < self.max_num_tokens:
                bounds = tentative
                new = bounds[0] - 1 if not ind else bounds[1]
                lengths[ind] = self._get_length(new)
            else:
                lengths[ind] = 0
        out = Batch.collate_fn(self._batches[bounds[0] : bounds[1]])
        self._batches = self._batches[: bounds[0]] + self._batches[bounds[1] :]
        return out

    def __iter__(self) -> tp.Iterator[Batch]:
        self._batches = []
        for batch in self.timer.iter(self.iterable, inner="fetch"):
            splitted = [
                b
                for b in batch.split()
                if max(b.x.shape[-1], b.y.shape[-1]) <= self.max_sequence_length
                and b.y_len[0]
            ]
            # print("lenghts", [b.x_len for b in splitted])
            self.removed += len(splitted) - int(batch.x.shape[0])
            self._batches.extend(splitted)
            self._batches.sort(key=self._sort_key)
            while len(self._batches) > self._buffer_size:
                with self.timer.timed("extract"):
                    out = self._extract()
                yield out
        while self._batches:
            yield self._extract()


def extract_dict(obj: tp.Any, reset_keys: tp.Iterable[str]) -> tp.Dict[str, tp.Any]:
    """Extract the dict of a object and reset to None
    some of the keys (after checking that they do exist).
    This is useful for delayed instanciation of attributes which may
    not support pickling.
    """
    attributes = dict(obj.__dict__)
    for key in reset_keys:
        assert key in attributes
        attributes[key] = None
    return attributes


class DelayedReader:
    """Lazily opens files or process json lines.
    DelayedReader instances have a code property and id property
    which are filled on demand only to spare useless computation.
    """

    def __init__(self, value: tp.Any, reader: str) -> None:
        self._reader = reader
        self._value = value
        self._code: tp.Optional[str] = None
        self._id: tp.Optional[str] = None
        self._info: tp.Dict[str, tp.Any] = {}

    @classmethod
    def from_file(cls: tp.Type[D], filepath: tp.Union[str, Path]) -> D:
        """Load lazily from a path"""
        return cls(value=filepath, reader="file")

    @classmethod
    def from_json_string(cls: tp.Type[D], string: bytes) -> D:
        """Load lazily from a json string with fields
        repo_name, path and content
        """
        if not isinstance(string, bytes):
            raise TypeError("String must be provided as bytes")
        return cls(value=string, reader="json_string")

    def _read(self) -> None:
        if self._code is not None:
            return
        if self._reader == "file":
            self._code = Path(self._value).read_text("utf8")
            self._id = "filepath:" + str(self._value)
            return
        if self._reader == "json_string":
            data = json.loads(self._value)
            try:
                self._code = data["content"]
            except KeyError as e:
                raise ValueError(
                    f"Missing content field in the json_string: {data}"
                ) from e
            if all(x in data for x in ["repo_name", "path"]):
                self._id = data["repo_name"] + ":" + data["path"]
            elif all(x in data for x in ["max_stars_repo_name", "max_stars_repo_path"]):
                self._id = (
                    data["max_stars_repo_name"] + ":" + data["max_stars_repo_path"]
                )
            self._info = data
            return
        raise ValueError(f"Unknown specified reader {self._reader}")

    @property
    def licenses(self) -> tp.Optional[tp.List[str]]:
        """Return the licenses if available"""
        out = self.info.get("license", None)  # only one in big query
        if out is None:
            return self.info.get(  # type: ignore
                "max_stars_repo_licenses", self.info.get("licenses", None)
            )
        return [out]

    @property
    def code(self) -> str:
        self._read()
        return self._code  # type: ignore

    @property
    def id(self) -> str:
        self._read()
        return self._id  # type: ignore

    @property
    def info(self) -> tp.Dict[str, str]:
        self._read()
        return self._info  # type: ignore

    def __repr__(self) -> str:
        try:
            return f"DelayedReader<id={self.id},code={self.code}>"
        except Exception:  # pylint: disable=broad-except
            return f"DelayedReader<UNREADABLE VALUE={self._value}>)"


class CodeWalker:
    """Utility for walking code files randomly while avoiding
    loading too much into memory at once

    Parameters
    ---------
    extensions: list of str
        extensions to read data from. Currently supports .py and .json.gz
    buffer_size: int
        maximum buffer size for storing json.gz lines and be able to yield
        from it in a random order
    rng: RandomState or int
        random state or seed for a random state

    Returns
    -------
    DelayedReader
        an object with fields code and id which loads the code lazily
    """

    SUPPORTED_CODE_EXTENSIONS = (".py",)

    def __init__(
        self,
        extensions: tp.List[str],
        buffer_size: int = 1000,
        rng: tp.Optional[tp.Union[int, np.random.RandomState]] = None,
    ) -> None:
        if isinstance(rng, np.random.RandomState):
            self.rng = rng
        else:
            self.rng = np.random.RandomState(rng)
        self.extensions = tuple(extensions)
        self.buffer_size = buffer_size
        for ext in self.extensions:
            if ext not in (".json.gz",) + self.SUPPORTED_CODE_EXTENSIONS:
                raise ValueError(f"Extension {ext} is not supported")

    def walk(self, input_path: tp.Union[str, Path]) -> tp.Iterator[DelayedReader]:
        """Walks a folder or a file and yields DelayedReader from it, in
        a random order. Delayed reader have code and id fields that are fetched
        on demand.

        Parameter
        ---------
        input_path: str or Path
           path to the file to read or folder to walk

        Yields
        ------
        str, str
            an identifier for the code and the corresponding code
        """
        input_path = Path(input_path)
        if not input_path.exists():
            raise ValueError(f"Missing input path: {input_path}")
        if input_path.is_file():
            if not any(input_path.name.endswith(x) for x in self.extensions):
                return
        if input_path.is_dir():
            if input_path.name[0] in (".", "_"):
                return
            if self.extensions == (".json.gz",):
                # dive into sub-directories for json.gz files
                # this is especially useful when a folder is a language
                sub_paths = list(input_path.rglob(f"*{self.extensions[0]}"))
            else:
                sub_paths = list(input_path.iterdir())
            self.rng.shuffle(sub_paths)  # type: ignore
            for sub_path in sub_paths:
                yield from self.walk(sub_path)
        elif input_path.suffix in self.SUPPORTED_CODE_EXTENSIONS:
            yield DelayedReader.from_file(input_path)
        elif input_path.name.endswith(".json.gz"):
            yield from self._gzip_walk(input_path)
        else:
            raise ValueError(f"Unsupported extension {input_path.suffix}")

    def _gzip_walk(self, input_path: Path) -> tp.Iterator[DelayedReader]:
        """Reads a json.gz code data and returns lines in a
        random order (although not uniformly).
        Lines are first added to a buffer until reaching a given
        buffer size, and then it randomly yields from it while
        replacing yielded lines with the new read lines.
        """
        if not input_path.name.endswith("json.gz"):
            raise RuntimeError("gzip_walk only works on json.gz files")
        lines: tp.List[bytes] = []
        with gzip.open(input_path, "rb") as f:
            for line in f:  # readlines() would load all data -> bad idea
                line = line.strip()
                if not line:
                    continue
                if len(lines) < self.buffer_size:
                    lines.append(line)
                else:
                    ind = self.rng.choice(len(lines))
                    yield DelayedReader.from_json_string(lines[ind])
                    lines[ind] = line
        while lines:
            ind = self.rng.choice(len(lines))
            content = lines.pop(ind)
            yield DelayedReader.from_json_string(content)


class Modulo:
    """Modulo-like object for identifying a task, with the index of the task,
    and the mod (number of total tasks).
    Calling this object on an index will return the modulo, and lets you select
    what this task should work on.

    Parameters
    ----------
    index: int
        index of the task
    mod: int
        total number of tasks

    Note
    ----
    Instances of this object can be created through from_env which checks slurm
    and pytorch context
    """

    def __init__(self, index: int, mod: int) -> None:
        if index >= mod:
            raise ValueError(f"Index {index} must be stricly lower than {mod}")
        if index < 0:
            raise ValueError("Index must be positive or null")
        self.mod = mod
        self.index = index

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}(index={self.index}, mod={self.mod})"

    def __call__(self, ind: int) -> bool:
        out = ind % self.mod == self.index
        return out

    def __mul__(self: M, other: M) -> M:
        mod = self.mod * other.mod
        ind = self.mod * other.index + self.index
        return self.__class__(ind, mod)

    @classmethod
    def from_env(cls: tp.Type[M]) -> M:
        """Creates a Modulo instance according to
        slurm task and pytorch worker info
        """
        out = cls(0, 1)
        worker_info = torch.utils.data.get_worker_info()
        if worker_info is not None:
            out *= cls(worker_info.id, worker_info.num_workers)
        try:
            env = submitit.JobEnvironment()
        except RuntimeError:
            pass
        else:
            out *= cls(env.global_rank, env.num_tasks)
        return out


class Timer:
    def __init__(self) -> None:
        self._starts: tp.Dict[str, float] = {}
        self._durations = dict(self._starts)

    def __contains__(self, key: str) -> bool:
        return key in self._starts

    def iter(
        self, iterable: tp.Iterable[X], *, inner: str = "", outer: str = "",
    ) -> tp.Generator[X, None, None]:
        iterator = iter(iterable)
        while True:
            if inner:
                self.start(inner)
            if outer:
                # cant rely on standard approach because extract can happen in between
                outer_start = time.time()
            try:
                val = next(iterator)
            except StopIteration:
                for key in (inner, outer):
                    if key:
                        self._starts.pop(key, None)
                break
            else:
                if inner:
                    self.stop(inner)
                yield val
                if outer:
                    if outer in self._starts:
                        raise ValueError(f"Key {outer} already in use")
                    self._starts[outer] = outer_start
                    self.stop(outer)

    @contextlib.contextmanager
    def timed(self, key: str) -> tp.Iterator[None]:
        self.start(key)
        try:
            yield
        finally:
            self.stop(key)

    def start(self, *keys: str) -> "Timer":
        for key in keys:
            if key in self._starts:
                raise ValueError(f"Key {key} already in use")
            self._starts[key] = time.time()
        return self

    def stop(self, *keys: str) -> "Timer":
        now = time.time()
        for key in keys:
            self._durations[key] = self._durations.get(key, 0) + now - self._starts[key]
            del self._starts[key]
        return self

    def extract(self) -> tp.Dict[str, float]:
        durations = self._durations
        self._durations = {}
        self._starts = {}
        return durations


def split_python_code(code: str) -> tp.Tuple[str, tp.List[str]]:
    """Split code between base-level def and class definitions

    Parameter
    ---------
    code: str
        code to analyze

    Returns
    -------
    str, List[str]
        the header string, and the list of parts for the rest of the code
    """
    lines = code.splitlines()
    header: tp.Optional[str] = None
    out = []
    current: tp.List[str] = []
    ready = False
    for line in lines:
        if line and line[0] not in (" ", "\t"):
            if ready:
                ready = False
                out.append("\n".join(current))
                current = []
            if line.startswith(("def ", "class ", "@")):
                if line.startswith(("def ", "class ")):
                    ready = True
                if header is None:
                    header = "\n".join(current)
                    current = []
        current.append(line)
    out.append("\n".join(current))
    if header is None:
        header = ""
    return header, out


class PyAugmenter:
    """Modify the code by removing some parts and reordering base level class/functions
    This can serve as data augmentation

    Parameters
    ----------
    keep_origin: float
        probability to keep origin file unchanged
    rng: np.random.RandomState
        random state for reproducibility
    """

    def __init__(
        self, keep_origin: float = 0.3, rng: tp.Optional[np.random.RandomState] = None
    ) -> None:
        if rng is None:
            rng = np.random.RandomState()
        self.p = keep_origin
        self.rng = rng

    def __call__(self, code: str) -> str:
        """Modify the code by reordering/removing base def/class definitions

        Parameter
        ---------
        code: str
            code to analyze

        Returns
        -------
        str
            the updated code
        """
        if self.rng.rand() < self.p:
            return code
        header, parts = split_python_code(code)
        if len(parts) == 1:
            return code
        self.rng.shuffle(parts)
        weights = np.array([float(k ** 2) for k in range(len(parts))])
        weights /= weights.sum()
        selected = int(self.rng.choice(range(len(parts)), p=weights))
        return "\n".join([header] + parts[:selected])
