import time
import concurrent.futures
import typing as tp


X = tp.TypeVar("X")


# pylint: disable=too-few-public-methods
class InfiniteIterator(tp.Generic[X]):
    """Makes an infinite iterator out of a fixed finite iterator
    while keeping track of:
    - call durations
    - number of epochs
    """

    def __init__(self, iterable: tp.Iterable[X]) -> None:
        self._iterable = iterable
        self._iterator = iter(self._iterable)
        self.epoch = 0
        self.calls = 0
        self.total_duration = 0.0
        self.last_duration = 0.0

    @property
    def average_duration(self) -> float:
        return self.total_duration / self.calls

    def __next__(self) -> X:
        t0 = time.time()
        try:
            x = next(self._iterator)
        except StopIteration:
            self.epoch += 1
            self._iterator = iter(self._iterable)
            try:
                x = next(self._iterator)
            except StopIteration as e:
                # iterables should be re-iterable...
                raise RuntimeError("Iterable is consumed") from e
        self.calls += 1
        self.last_duration = time.time() - t0
        self.total_duration += self.last_duration
        return x

    def __iter__(self) -> tp.Iterator[X]:
        return self


class PrefetchedIterable:
    """Prefetches the first element when finishing
    iterating over the iterable.

    NOTE: CURRENTLY IT SEEMS UNHELPFUL for test batch optimization
    """

    def __init__(self, iterable: tp.Iterable[X]) -> None:
        self._iterable = iterable
        self._iterator = iter(self._iterable)
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._initial: tp.Any = self._executor.submit(next, self._iterator)

    def __iter__(self) -> tp.Iterator[X]:
        if self._initial is not None:
            yield self._initial.result()
            self._initial = None
        else:
            # not consumed entirely, so reset
            self._iterator = iter(self._iterable)
        yield from self._iterator
        # reinitialize for next round
        self._iterator = iter(self._iterable)
        self._initial = self._executor.submit(next, self._iterator)
