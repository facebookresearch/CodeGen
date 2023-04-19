import typing as tp
import itertools
from pathlib import Path
import torch
import pytest
import submitit
from . import distrib


def test_task_env_from_no_env() -> None:
    task = distrib.TaskEnv.from_env()
    assert task.world_size == 1
    assert not task.rank
    task *= distrib.TaskEnv(2, 3)
    assert str(task) == "TaskEnv(rank=2, world_size=3)"


def test_task_mult() -> None:
    tasks1 = [distrib.TaskEnv(k, 3) for k in range(3)]
    tasks2 = [distrib.TaskEnv(k, 4) for k in range(4)]
    tasks = [x * y for x, y in itertools.product(tasks1, tasks2)]
    assert all(t.world_size == 12 for t in tasks)
    assert set(t.rank for t in tasks) == set(range(12))


def test_metrics_dict() -> None:
    with distrib.SumDict().summed_over(2) as metrics:
        metrics.update(blublu=21, stuff=2)
    with metrics.summed_over(1):
        metrics["truc"] = 12
    with metrics.aggregation("max"):
        metrics["maxtest"] = 24
    with metrics.aggregation("min"):
        metrics["mintest"] = 24
    other = distrib.SumDict()
    with other.summed_over(2):
        other.update(stuff=4, blublu=torch.Tensor([3]))
    with other.aggregation("max"):
        other["maxtest"] = 10
    with other.aggregation("min"):
        other["mintest"] = 10
    metrics += other
    out = metrics.set_prefix("@").reduce().export()
    exp = {
        "@blublu": 6.0,
        "@stuff": 1.5,
        "@truc": 12.0,
        "@maxtest": 24,
        "@mintest": 10,
    }
    assert out == exp


def test_metrics_dict_basics() -> None:
    metrics = distrib.SumDict([("sum1", 1)], sum2=2)
    metrics += distrib.SumDict({"sum2": 2})
    assert metrics["sum2"] == 4
    assert set(metrics.keys()) == {"sum1", "sum2"}
    assert set(metrics.values()) == {1, 4}
    expected = dict(sum1=1, sum2=4)
    assert repr(metrics) != str(metrics)
    # errors
    with pytest.raises(RuntimeError):
        with metrics.summed_over(2):
            pass  # nothing happened
    with pytest.raises(ValueError):
        with metrics.summed_over(0):
            pass
    with pytest.raises(RuntimeError):
        with metrics.summed_over(2):
            with metrics.summed_over(2):
                metrics["nothing"] = 12
    with pytest.raises(ValueError):
        with metrics.aggregation("blublu"):
            pass
    # nothing should have changed
    assert dict(metrics.items()) == expected


def _metrics_distrib_task() -> tp.Dict[str, float]:
    distrib.init()
    task = distrib.TaskEnv.from_env()
    metrics = distrib.SumDict({"rank_sum": task.rank + 1})
    with metrics.summed_over(1):
        metrics["rank_mean"] = task.rank + 1
    with metrics.aggregation("max"):
        metrics.update(rank_max=task.rank + 1)
    with metrics.aggregation("min"):
        metrics["rank_min"] = task.rank + 1
    return metrics.reduce().export()


def test_metrics_dict_reduce(tmp_path: Path) -> None:
    if not (torch.cuda.is_available() and torch.cuda.device_count() >= 2):
        pytest.skip("Need 2 GPUs")
    executor = submitit.AutoExecutor(tmp_path, cluster="local")
    executor.update_parameters(timeout_min=6, gpus_per_node=2, tasks_per_node=2)
    job = executor.submit(_metrics_distrib_task)
    res1, res2 = job.results()
    assert res1 == res2
    assert res1 == dict(rank_mean=1.5, rank_sum=3, rank_min=1, rank_max=2)
