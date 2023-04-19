import pytest
from . import iterators


def test_prefetch() -> None:
    data = (1, 2, 3)
    prefetched = iterators.PrefetchedIterable(data)
    assert tuple(prefetched) == data
    assert prefetched._initial is not None
    assert next(iter(prefetched)) == 1
    assert tuple(prefetched) == data


def test_infinite_iterator() -> None:
    iterable = [1, 2, 3]
    stream = iterators.InfiniteIterator(iterable)
    x = [next(stream) for _ in range(7)]
    assert x == [1, 2, 3, 1, 2, 3, 1]
    assert stream.epoch == 2


def test_consumed_infinite_iterator() -> None:
    iterable = (x for x in range(3))
    stream = iterators.InfiniteIterator(iterable)
    with pytest.raises(RuntimeError):
        _ = [next(stream) for _ in range(7)]
