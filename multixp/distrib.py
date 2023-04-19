import os
import random
import logging
import datetime
import itertools
import contextlib
import collections
import typing as tp
import torch
import torch.distributed as dist
import submitit


logger = logging.getLogger(__name__)
T = tp.TypeVar("T", bound="TaskEnv")
S = tp.TypeVar("S", bound="SumDict")
FloatDict = tp.Dict[str, float]
TensorFloat = tp.Union[float, torch.Tensor]
TIMEOUT = 300


def init() -> None:
    """Initializes torch distributed through env:// method
    This exports standard env variables (WORLD_SIZE etc) into the current env
    """
    task = TaskEnv.from_env(dataloader=False)
    if task.world_size == 1:
        return
    if torch.distributed.is_initialized():
        return
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA not available")
    env = submitit.JobEnvironment()
    # rdv = env.paths.folder.resolve().absolute() / "rendez_vous"
    info = dict(
        WORLD_SIZE=task.world_size, RANK=task.rank, MASTER_ADDR=env.hostnames[0]
    )
    if "MASTER_PORT" not in os.environ:
        rng = random.Random(env.job_id)
        info["MASTER_PORT"] = rng.randint(20000, 60000)
        os.environ.update({x: str(y) for x, y in info.items()})
    os.environ["NCCL_ASYNC_ERROR_HANDLING"] = "1"  # for throwing errors at timeouts
    content = ", ".join(f"{x}={info[x]}" for x in sorted(info))
    logger.info(f"Setting up distributed environement with {content}")
    print(f"Setting up distributed environement with {content}", flush=True)
    torch.distributed.init_process_group(
        backend="nccl",
        init_method="env://",
        # init_method="file://" + str(rdv),
        world_size=task.world_size,
        rank=task.rank,
        timeout=datetime.timedelta(seconds=TIMEOUT),
    )
    torch.cuda.set_device(env.local_rank)
    # torch.distributed.barrier()
    # if task.is_main and rdv.exists():
    #     # Delete rendez vous file early, let's hope this doesn't bug too much.
    #     rdv.unlink()
    if not (dist.is_available() and dist.is_nccl_available() and dist.is_initialized()):
        raise RuntimeError("NCCL incorrectly initialized")
    logger.info("Distributed mode initialized")


def _fix_float(val: TensorFloat) -> float:
    return float(val.item()) if isinstance(val, torch.Tensor) else float(val)


class SumValue:
    """Object holding a value and the way it can be aggregated when summed
    Aggregations include "sum" (default)/"min"/"max", or a float for
    weighted average.
    """

    _DEFAULT: tp.Union[float, str] = "sum"

    def __init__(
        self, value: float, aggregation: tp.Union[float, str] = _DEFAULT
    ) -> None:
        self.value = value
        self.aggregation = aggregation
        if not isinstance(aggregation, str):
            self.aggregation = float(aggregation)
        if isinstance(self.aggregation, str):
            if self.aggregation not in ("min", "max", "sum"):
                raise ValueError(
                    "Only 'min', 'max', 'sum' or a float are allowed for aggregation"
                )
        elif self.aggregation <= 0:
            raise ValueError("Weights need to be strictly positive")

    def __repr__(self):
        name = self.__class__.__name__
        data = ", ".join(f"{n}={getattr(self, n)!r}" for n in ["value", "aggregation"])
        return f"{name}({data})"

    def __add__(self, other: "SumValue") -> "SumValue":
        a0 = self.aggregation
        a1 = other.aggregation
        a2 = a1
        if isinstance(a0, str):
            if not a0 == a1:
                raise ValueError(f"Incompatible aggregations: {a0} and {a1}")
            funcs = {"sum": sum, "max": max, "min": min}
            func: tp.Callable[..., float] = funcs[a0]  # type: ignore
            value = func([self.value, other.value])
        else:
            if not (isinstance(a2, float) and isinstance(a1, float)):
                raise ValueError(f"Incompatible aggregations: {a0} and {a1}")
            a2 += a0
            value = (a0 * self.value + a1 * other.value) / a2
        return SumValue(value, a2)


MDIter = tp.Union[tp.Mapping[str, TensorFloat], tp.Iterable[tp.Tuple[str, TensorFloat]]]


class SumDict:
    """Records summed metrics which can be reduced among multiple workers,
    and exported to a dict after renormalizing them by their count.
    Metrics dict can be summed, differing keys will be added, and values
    from similar keys will be added up.

    Example
    -------
    metrics = SumDict()
    for k in range(num_steps):
        loss =...
        current = SumDict(sequences=batchsize)
        with current.summed_over(batchsize):
            current["loss"] = loss.sum()
        metrics() += current
    ...
    metrics.set_prefix("train/").reduce().export()
    """

    def __init__(self, mapping: MDIter = (), **kwargs: TensorFloat) -> None:
        self._state = SumValue._DEFAULT
        self.data: tp.Dict[str, SumValue] = {}
        self._context_updated = False
        self.update(mapping, **kwargs)

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}(data={self.data})"

    def __str__(self) -> str:
        return str(self.export())

    def __setitem__(self, key: str, value: float) -> None:
        self._context_updated = True
        div = 1.0 if isinstance(self._state, str) else self._state
        self.data[key] = SumValue(value / div, self._state)

    def __getitem__(self, key: str) -> float:
        return self.data[key].value

    def __delitem__(self, key: str) -> None:
        del self.data[key]

    def update(self, mapping: MDIter = (), **kwargs: TensorFloat) -> None:
        self._context_updated = True
        div = 1.0 if isinstance(self._state, str) else self._state
        div = self._state if isinstance(self._state, float) else 1.0
        if hasattr(mapping, "items"):
            mapping = getattr(mapping, "items")()
        iterable: tp.Any = itertools.chain(mapping, kwargs.items())
        sv = {k: SumValue(_fix_float(y) / div, self._state) for k, y in iterable}
        self.data.update(sv)

    def set_prefix(self: S, prefix: str) -> S:
        self.data = {prefix + x: y for x, y in self.data.items()}
        return self

    def __add__(self: S, other: S) -> S:
        out = dict(self.data)
        for k, val in other.data.items():
            if k in out:
                out[k] += val
            else:
                out[k] = val
        outd = self.__class__()
        outd.data = out
        return outd

    @contextlib.contextmanager
    def summed_over(self: S, weight: TensorFloat) -> tp.Generator[S, None, None]:
        weight = _fix_float(weight)
        with self._context(weight) as sub:
            yield sub

    @contextlib.contextmanager
    def aggregation(self: S, name: str) -> tp.Generator[S, None, None]:
        if not isinstance(name, str):
            raise TypeError(f"Only aggreagation string names are allowed, got {name!r}")
        with self._context(name) as sub:
            yield sub

    @contextlib.contextmanager
    def _context(self: S, value: tp.Union[str, float]) -> tp.Generator[S, None, None]:
        default = SumValue._DEFAULT
        if self._state != default:
            raise RuntimeError("Already in a non-default context")
        self._context_updated = False
        SumValue(0.0, value)  # triggers check
        self._state = value
        try:
            yield self
        finally:
            was_updated = self._context_updated
            # do the cleaning
            self._state = default
            self._context_updated = False
            if not was_updated:
                raise RuntimeError(f"Nothing happened during context of {self!r}")

    def reduce(self: S) -> S:
        """Reduces between workers, aggregating all values.
        Only the main process gets the data, others are emptied out
        """
        data = {}
        dtag = "-%DIVISOR%-"
        ttag = "-%TASK{r}%-"
        env = TaskEnv.from_env(dataloader=False)
        for k, value in self.data.items():
            agg = value.aggregation
            if isinstance(agg, float):
                data[k] = agg * value.value
                data[k + dtag] = agg
            elif agg in ("max", "min"):
                for r in range(env.world_size):
                    data[k + ttag.format(r=r)] = value.value if r == env.rank else 0
            elif agg == "sum":
                data[k] = value.value
            else:
                raise RuntimeError(f"Unknown aggregation {agg}")
        out = reduce_dict(data)
        if not out:
            self.clear()
            return self
        data2 = {}
        for k, value in self.data.items():
            agg = value.aggregation
            if isinstance(agg, float):
                w = out[k + dtag]
                data2[k] = SumValue(out[k] / w, w)
            elif agg == "sum":
                data2[k] = SumValue(out[k], value.aggregation)
            elif agg in ("max", "min"):
                func = max if agg == "max" else min
                val = func(out[k + ttag.format(r=r)] for r in range(env.world_size))
                data2[k] = SumValue(val, value.aggregation)
        self.data = data2
        return self

    def export(self) -> FloatDict:
        """Exports the normalized values
        Fields starting with "_" are ignored.
        """
        outiter = ((x, y.value) for x, y in self.data.items())
        return dict(sorted(outiter))  # sorted for conveniency

    def items(self) -> tp.Generator[tp.Tuple[str, float], None, None]:
        return ((k, v.value) for k, v in self.data.items())

    def keys(self) -> tp.Generator[str, None, None]:
        return (x for x in self.data.keys())

    def values(self) -> tp.Generator[float, None, None]:
        return (x.value for x in self.data.values())

    def clear(self) -> None:
        """Reset all data"""
        self.data = {}


def reduce_dict(metrics: FloatDict) -> FloatDict:
    """Sums a dictionary of metrics over a distributed set of GPUs
    """
    task = TaskEnv.from_env(dataloader=False)
    if task.world_size == 1:
        return metrics
    metrics = dict(metrics)
    key = "_task_id_check_"  # for a dummy check to make sure we don't do stupid things
    metrics[key] = task.rank
    keys, values = zip(*sorted(metrics.items()))
    tensor = torch.tensor(
        list(values), device="cuda", dtype=torch.float64
    )  # type: ignore
    # dist.reduce(tensor, dst=0, op=dist.ReduceOp.SUM, async_op=False)  # type: ignore
    # dist.all_reduce(tensor, dist.ReduceOp.SUM, async_op=False)
    work = dist.all_reduce(tensor, dist.ReduceOp.SUM, async_op=True)
    work.wait(datetime.timedelta(seconds=TIMEOUT))
    summed = tensor.cpu().numpy().tolist()
    # if not task.is_main:
    #     return {}
    out = dict(zip(keys, summed))
    # dummy check!
    check = out.pop(key)
    expected = task.world_size * (task.world_size - 1.0) / 2
    if abs(check - expected) > 0.001:
        raise RuntimeError(
            f"reducing on GPUs did not work (expected average rank {expected} but got {check})"
        )
    return out


class TaskEnv:
    """Keeps a unique rank for a task, the total number of tasks

    Parameters
    ----------
    rank: int
        rank of the task
    world_size: int
        total number of tasks
    Note
    ----
    Instances of this object can be created through from_env which checks slurm
    and pytorch context
    """

    def __init__(self, rank: int, world_size: int) -> None:
        if rank >= world_size:
            raise ValueError(f"Rank {rank} must be stricly lower than {world_size}")
        if rank < 0:
            raise ValueError("Rank must be positive or null")
        self.world_size = world_size
        self.rank = rank

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}(rank={self.rank}, world_size={self.world_size})"

    def modulo(self, ind: int) -> bool:
        out = ind % self.world_size == self.rank
        return out

    @property
    def is_main(self) -> bool:
        return not self.rank

    def __mul__(self: T, other: T) -> T:
        world_size = self.world_size * other.world_size
        ind = self.world_size * other.rank + self.rank
        return self.__class__(ind, world_size)

    @classmethod
    def from_env(cls: tp.Type[T], slurm: bool = True, dataloader: bool = True) -> T:
        """Creates a Modulo instance according to
        slurm task and pytorch dataloader worker info
        """
        out = cls(0, 1)
        if dataloader:
            worker_info = torch.utils.data.get_worker_info()
            if worker_info is not None:
                out *= cls(worker_info.id, worker_info.num_workers)
        if slurm:
            try:
                env = submitit.JobEnvironment()
            except RuntimeError:
                pass
            else:
                out *= cls(env.global_rank, env.num_tasks)
        return out
