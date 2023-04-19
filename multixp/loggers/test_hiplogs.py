import subprocess
import sys
import json
import tempfile
import typing as tp
from pathlib import Path
import hydra
import numpy as np
from . import hiplogs


def test_parse_logs() -> None:
    path = Path(__file__).parents[1] / "runners" / "data" / "mockpretrain" / "hip.log"
    hlog = hiplogs.HipLog(path)
    logs = hlog.to_hiplot_experiment().datapoints
    assert len(logs) == 13
    vals = logs[-1].values
    assert vals["workdir"] == "054238_fb_ddpg", "Xp id not exported"
    bad_type = {x: y for x, y in vals.items() if not isinstance(y, (int, float, str))}
    assert not bad_type, "Found unsupported type(s)"


def test_load() -> None:
    xp = hiplogs.load(str(Path(__file__).parents[1] / "runners"), step=2)
    assert len(xp.datapoints) == 6


def test_sanitization(tmp_path: Path) -> None:
    hiplog = hiplogs.HipLog(tmp_path / "log.txt")
    hiplog(path=Path("blublu"), val=np.int32(4), inf=np.inf, nan=np.nan)
    _ = json.dumps(hiplog.content)  # should not bug


def test_hiplog(tmp_path: Path) -> None:
    hiplog = hiplogs.HipLog(tmp_path / "log.txt")
    hiplog(hello="world")
    hiplog.write()
    hiplog(hello="monde")
    hiplog(number=12).write()
    hiplog(something=np.int32(12)).write()
    data = hiplog.read()
    for d in data:
        for key in list(d):
            if key.startswith("#"):
                d.pop(key)
    expected = [
        dict(hello="world"),
        dict(hello="monde", number=12),
        dict(hello="monde", number=12, something=12),
    ]
    assert data == expected
    # reloaded
    assert not hiplog._reloaded
    hiplog = hiplogs.HipLog(tmp_path / "log.txt")
    assert hiplog._reloaded == 1


def test_hiplog_stats(tmp_path: Path) -> None:
    hiplog = hiplogs.HipLog(tmp_path / "log.txt")
    for vals in ([3, 5], [7, 8, 9]):
        for val in vals:
            hiplog.with_stats("mean")(val=val)
        hiplog.write()
    data = hiplog.read()
    for d in data:
        for key in list(d):
            if key.startswith("#"):
                d.pop(key)
    expected = [{"val#mean": 4}, {"val#mean": 8}]
    assert data == expected


def test_repository_information() -> None:
    out = hiplogs.repository_information()
    assert len(out) in [2, 3]  # IR_project available or not


def test_hiplogs_from_hydra_config(tmp_path: Path) -> None:
    train_cmd = [
        sys.executable,
        "-m",
        "multixp.loggers.test_hiplogs",
        f"hydra.run.dir={tmp_path}",
        "experiment=hiplogtest",
    ]
    subprocess.check_call(train_cmd)


@hydra.main(config_name="base_config", config_path="../trainers", version_base=None)
def main(args: tp.Any) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        log = hiplogs.HipLog(Path(tmp) / "hiplog.test.log").flattened(args)
        assert "experiment" in log.content


if __name__ == "__main__":
    # needed to load the config:
    from multixp.trainers import (
        baseloop,
    )  # pylint: disable=unused-import,import-outside-toplevel

    main()
