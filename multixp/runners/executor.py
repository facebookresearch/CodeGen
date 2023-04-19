import time
import logging
import traceback
import contextlib
from pathlib import Path
import nevergrad.common.typing as tp
from multixp.common import utils


logger = logging.getLogger(__name__)


@contextlib.contextmanager
def batch_if_available(executor: tp.ExecutorLike) -> tp.Iterator[None]:
    """Only submitit executors have a batch context, so we need different
    cases for other executor (eg: concurrent.futures)
    Batch context in submitit allows for using arrays in slurm, which is
    better for the cluster health.
    """
    if hasattr(executor, "batch"):
        with executor.batch():  # type: ignore
            yield
    else:
        yield


X = tp.TypeVar("X")
Fn = tp.Callable[..., X]


class DelayedJob(tp.Generic[X]):
    def __init__(
        self, executor: "DelayedExecutor[X]", fn: Fn[X], *args: tp.Any, **kwargs: tp.Any
    ) -> None:
        self.executor = executor
        self.time = time.time()
        self._job: tp.Optional[tp.JobLike[X]] = None
        self._submission: tp.Optional[
            tp.Tuple[Fn[X], tp.Tuple[tp.Any, ...], tp.Dict[str, tp.Any]]
        ] = (
            fn,
            args,
            kwargs,
        )

    def _is_submited(self, force: bool = False) -> bool:
        if self._job is None:
            self.executor._check_submit(force=force)
        return self._job is not None

    def done(self) -> bool:
        if not self._is_submited():
            return False
        return self._job is not None and self._job.done()

    def result(self) -> X:
        error = ""
        try:
            result = self.job.result()
        except Exception:  # pylint: disable=broad-except
            error = traceback.format_exc()
            result = self.executor._default
        self.executor._add_result(error=error)
        return result

    @property
    def job(self) -> tp.JobLike[X]:
        self._is_submited(force=True)
        if self._job is None:
            raise RuntimeError("Job should have been submitted")
        return self._job

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(job={self.job})"

    def stdout(self) -> str:
        return self.job.stdout()  # type: ignore

    def cancel(self) -> None:
        return self.job.cancel()  # type: ignore

    def stderr(self) -> str:
        return self.job.stderr()  # type: ignore


class DelayedExecutor(tp.Generic[X]):
    def __init__(
        self,
        executor: tp.ExecutorLike,
        default: X,
        batch_size: int = 8,
        max_delay: float = 45 * 60,
        max_failure_rate: float = 0.25,
        working_directory: tp.Optional[tp.Union[Path, str]] = None,
    ) -> None:
        self.executor = executor
        self.batch_size = batch_size
        self.max_failure_rate = max_failure_rate
        # This is an ugly messy hack
        self.working_directory = (
            None if working_directory is None else Path(working_directory)
        )
        self.max_delay = max_delay
        self._default = default
        self._unsubmitted: tp.List[DelayedJob[X]] = []
        self._total_results = 0
        self._total_failures = 0
        assert 0 < max_failure_rate < 1

    def submit(self, fn: Fn[X], *args: tp.Any, **kwargs: tp.Any) -> DelayedJob[X]:
        if self.working_directory is not None and not self.working_directory.exists():
            raise RuntimeError(
                f"executor.run_dir must be populated by user: {self.working_directory}"
            )
        job = DelayedJob(self, fn, *args, **kwargs)
        self._unsubmitted.append(job)
        return job

    def _check_submit(self, force: bool = False) -> None:
        if not self._unsubmitted:
            return
        delay = time.time() - self._unsubmitted[0].time
        if self._unsubmitted:
            if (
                force
                or len(self._unsubmitted) >= self.batch_size
                or delay > self.max_delay
            ):
                logger.info(
                    f"Submitting {len(self._unsubmitted)} job(s) after {int(delay / 60)}min wait"
                )
                work_dir = (
                    Path.cwd()
                    if self.working_directory is None
                    else self.working_directory
                )
                with utils.working_directory(work_dir):
                    with batch_if_available(self.executor):
                        for job in self._unsubmitted:
                            assert job._submission is not None
                            fn, args, kwargs = job._submission
                            job._submission = None
                            job._job = self.executor.submit(fn, *args, **kwargs)
                        self._unsubmitted = []

    def _add_result(self, error: str) -> None:
        self._total_results += 1
        self._total_failures += bool(error)
        if error:
            logger.warning(
                f"Caught {self._total_failures} out of {self._total_results} runs:\n{error}"
            )
            if self._total_failures / self._total_results > self.max_failure_rate:
                raise RuntimeError(
                    f"Stopping since failure rate is above the threshold: {self.max_failure_rate}."
                )
            logger.warning("Ignoring since this is below max failure rate")

    def __del__(self) -> None:
        # unsafe, but better than nothing
        self._check_submit(force=True)
