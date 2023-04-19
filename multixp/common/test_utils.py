import os
from pathlib import Path
from . import utils


class ExpectedError(Exception):
    "Raised for testing the context"


def test_working_dir() -> None:
    current = os.getcwd()
    wanted = str(Path(__file__).parent)
    try:
        with utils.working_directory(wanted):
            assert wanted == os.getcwd()
            raise ExpectedError("just for testing")
    except ExpectedError:
        pass
    assert current == os.getcwd()


def test_filter_content() -> None:
    container = {"a": object(), "b": [12, "truc"], "c": 1}
    out = list(utils.filtered_content(container, int))
    assert out == [(("b", 0), 12), (("c",), 1)]
    out = list(utils.filtered_content(3, int))
    assert out == [((), 3)]
