from pathlib import Path
from . import hiplogs


def test_parse_logs() -> None:
    path = Path(__file__).with_name("mock")
    logs = hiplogs.parse_logs(path)
    assert len(logs) == 4
    assert logs[-1]["exp_id"] == path.name, "Xp id not exported"
    assert logs[-1]["i_am_a_parameter"] == 12, "parameters not exported"


def test_load() -> None:
    xp = hiplogs.load("recursive:" + str(Path(__file__).parent))
    assert len(xp.datapoints) == 4
