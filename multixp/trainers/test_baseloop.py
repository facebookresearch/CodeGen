import subprocess
import sys
from pathlib import Path
import torch
import pytest
import submitit
from multixp import core
from . import jrvision


def test_baseloop_from_commandline(tmp_path: Path) -> None:
    train_cmd = [
        sys.executable,
        "-m",
        "multixp.trainers.baseloop",
        f"hydra.run.dir={tmp_path}",
        "experiment=test",
        f"folder={tmp_path}",
    ]
    out = subprocess.check_output(train_cmd).decode()
    print(out)


def test_instantiation() -> None:
    out = core.instantiate(
        jrvision.TrainerConfig, experiment="mytest", **{"dataloader.num_workers": 144}
    )
    assert isinstance(out, jrvision.TrainerConfig)
    assert out.dataloader.num_workers == 144


def _config(path: Path) -> jrvision.TrainerConfig:
    return core.instantiate(
        jrvision.TrainerConfig,
        experiment="mytest",
        folder=path,
        model="dense",
        num_steps=2,
        **{
            "dataloader.name": "unittest",
            "dataloader.num_workers": 0,
            "dataloader.batch_size": 4,
        },
    )


def test_jrvision(tmp_path: Path) -> None:
    config = _config(tmp_path)
    trainer = jrvision.VisionTrainer(config)
    trainer.run()
    assert (tmp_path / "checkpoints" / "latest.pt").exists()
    lines = trainer.hiplogger.read()
    assert len(lines) == 2, "1 for 1st step, 1 for last"
    assert lines[0]["model"] == "BasicConfig"
    # state dict
    content = torch.load(trainer.checkpoint_path)
    assert set(content["state_dicts"].keys()) == {"lr_sched", "optimizer", "model"}
    # reloaded
    trainer = jrvision.VisionTrainer(config)
    assert trainer.step == 2
    trainer.run()
    lines = trainer.hiplogger.read()
    assert len(lines) == 4
    assert lines[-1]["step"] == 4
    assert lines[-1]["#reloaded"] == 1


def test_distributed_training(tmp_path: Path) -> None:
    if not (torch.cuda.is_available() and torch.cuda.device_count() >= 2):
        pytest.skip("Need 2 GPUs")
    config = _config(tmp_path)
    trainer = jrvision.VisionTrainer(config)
    trainer.run()
    executor = submitit.AutoExecutor(tmp_path, cluster="local")
    executor.update_parameters(timeout_min=6, gpus_per_node=2, tasks_per_node=2)
    job = executor.submit(lambda x: jrvision.VisionTrainer(x).run(), config)
    job.results()
