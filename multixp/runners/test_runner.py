from pathlib import Path
import pytest
import submitit
from multixp.common import utils
from . import executor
from . import runner


def test_trainer_function(tmp_path: Path) -> None:
    func = runner.TrainerFunction(
        "multixp.trainers.jrvision.VisionTrainer", metric="valid/acc"
    )
    func.validated(experiment="blublu")
    with pytest.raises(Exception):
        func.validated()
    with utils.working_directory(tmp_path):
        out = func(
            experiment="mytest",
            model="dense",
            num_steps=2,
            **{
                "dataloader.name": "unittest",
                "dataloader.num_workers": 0,
                "dataloader.batch_size": 4,
            },
        )
    assert isinstance(out, float)
    assert 0 <= out <= 1


def test_trainer_function_copied(tmp_path: Path) -> None:
    ex = executor.DelayedExecutor(
        submitit.AutoExecutor(cluster="local", folder=tmp_path),
        batch_size=1,
        default=float("inf"),
        working_directory=tmp_path / "run_dir",
    )
    func = runner.TrainerFunction(
        "multixp.trainers.jrvision.VisionTrainer",
        metric="valid/acc",
        working_directory=ex.working_directory,
    )
    job = ex.submit(
        func,
        experiment="mytest",
        model="dense",
        num_steps=2,
        **{
            "dataloader.name": "unittest",
            "dataloader.num_workers": 0,
            "dataloader.batch_size": 4,
        },
    )
    out = job.result()
    assert isinstance(out, float)
    assert "run_dir/multixp/__init__.py" in job.stdout()
    assert 0 <= out <= 1
