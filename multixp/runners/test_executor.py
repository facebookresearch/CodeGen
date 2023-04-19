import time
from pathlib import Path
import pytest
import submitit
from . import executor as _exec


def func(fail: bool = False) -> str:
    if fail:
        raise ValueError("This is a failure")
    return "success"


def get_executor(tmp_path: Path) -> _exec.DelayedExecutor[str]:
    local_exec = submitit.AutoExecutor(folder=tmp_path, cluster="debug")
    return _exec.DelayedExecutor(
        local_exec, default="ERROR", batch_size=2, max_delay=0.2, max_failure_rate=0.5
    )


def test_delayed_exec_num(tmp_path: Path) -> None:
    executor = get_executor(tmp_path)
    job1 = executor.submit(func)
    assert not job1.done()
    assert job1._job is None, "Job should not be submitted"
    job2 = executor.submit(func)
    assert job2.done()
    assert job1._job is not None, "Job should not be submitted"
    assert job2._job is not None, "Job should not be submitted"
    assert not executor._unsubmitted, "Unsubmitted jobs should be purged"


def test_delayed_exec_delay(tmp_path: Path) -> None:
    executor = get_executor(tmp_path)
    job1 = executor.submit(func)
    time.sleep(0.1)
    assert job1._job is None, "Job should not be submitted"
    time.sleep(0.11)
    job1.done()  # trigger a possible submission
    assert job1.job is not None, "Job should be submitted"
    assert not executor._unsubmitted, "Unsubmitted jobs should be purged"


def test_delayed_exec_error(tmp_path: Path) -> None:
    executor = get_executor(tmp_path)
    jobs = [executor.submit(func, fail=f) for f in [True, True]]
    with pytest.raises(RuntimeError):
        jobs[0].result()


def test_delayed_exec_caught_error(tmp_path: Path) -> None:
    executor = get_executor(tmp_path)
    jobs = [executor.submit(func, fail=f) for f in [False, True]]
    assert jobs[0].result() == "success"
    assert jobs[1].result() == "ERROR"
