import os
import argparse
import datetime
import typing as tp
from pathlib import Path
import json
import itertools
import submitit
import multixp as mxp
from . import executor as _ex
from . import runner


def sweep_iterator(
    data: tp.Dict[str, tp.List[tp.Any]]
) -> tp.Iterator[tp.Dict[str, tp.Any]]:
    keys = []
    vals = []
    for key, val in data.items():
        if not isinstance(key, str):
            raise TypeError(f"Keys must be strings, got {key} of type {type(key)}")
        keys.append(key)
        if not isinstance(val, list):
            raise TypeError(
                f"Values must be list, got {val} of type {type(val)} for key {key}"
            )
        vals.append(val)
    for selected in itertools.product(*vals):
        yield dict(zip(keys, selected))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="""Run a json experiment
(eg: `python -m multixp.runners.jsonrun 2022_10_20_online_example`)
The json file needs to have a __global__ field with fields trainer pointing to the
trainer class name (full python path) and metric as a valid logged metric name.
All other (non- __global__) fields need to be lists for the sweep.
The parser takes the experiment name as input pointing to the json name in runs_jsons
directory. Other parameters are job submission parameters.
"""
    )
    parser.add_argument(
        "experiment", type=str, help="name of an experiment (same as the json)"
    )
    parser.add_argument(
        "--hours", type=int, default=24, help="Number of hours the job can run"
    )
    parser.add_argument("--gpus", type=int, default=8, help="Number of gpus to use")
    parser.add_argument(
        "--comment", type=str, default=None, help="Comment for the submission"
    )
    parser.add_argument("--partition", type=str, default="learnlab")
    parser.add_argument(
        "--constraint", type=str, default="volta32gb", help="Slurm constraint"
    )
    args = parser.parse_args()
    # prepare submitit executor
    date = datetime.date.today().isoformat()
    user = os.getlogin()
    xp = args.experiment
    executor = submitit.AutoExecutor(
        folder=f"/checkpoint/{user}/codegen/xps/{date}_{xp}/%j"
    )
    workdir = executor.folder.with_name("workdir")
    workdir.parent.mkdir(exist_ok=True, parents=True)
    executor.update_parameters(
        timeout_min=args.hours * 60,
        slurm_partition=args.partition,
        slurm_constraint=args.constraint,
        mem_gb=60 * args.gpus,
        gpus_per_node=args.gpus,
        cpus_per_task=8,
        tasks_per_node=args.gpus,
        name=xp,
    )
    dexec = _ex.DelayedExecutor(
        executor, default=float("inf"), batch_size=1, working_directory=workdir
    )
    # get sweep (and copy file to workdir for conservation
    filepath = Path(mxp.__file__).parent.with_name("runs_jsons") / f"{xp}.json"
    assert filepath.exists(), f"Missing file {filepath}"
    (workdir.parent / filepath.name).write_bytes(filepath.read_bytes())
    with filepath.open("r") as f:
        data = json.load(f)
    assert isinstance(data, dict)
    info = data.pop("__global__")
    sweep = list(sweep_iterator(data))
    # creacte function, check it, submit it
    func = runner.TrainerFunction(
        info["trainer"], metric=info["metric"], working_directory=workdir
    )
    func.validated(experiment=xp, **sweep[0])  # check that parameters are correct
    jobs = [dexec.submit(func, experiment=xp, **params) for params in sweep]
    print(f"Launched in {workdir}: {[j.job.job_id for j in jobs]}")  # type: ignore


if __name__ == "__main__":
    main()
