from . import jsonrun


def test_json_sweep() -> None:
    sweep = {"a": [1, 2, 3], "b": ["b1", "b2"], "c": ["c"]}
    configs = list(jsonrun.sweep_iterator(sweep))  # type: ignore
    assert len(configs) == 6
