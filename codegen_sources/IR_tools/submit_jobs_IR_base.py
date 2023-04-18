import argparse
import datetime
import os
import time

import numpy as np
import submitit

_DEFAULT_SLURM_PARTITION = "learnlab"


def bool_flag(s):
    """
    Parse boolean arguments from the command line.
    """
    if s.lower() == "false":
        return False
    elif s.lower() == "true":
        return True
    else:
        raise argparse.ArgumentTypeError("Invalid value for a boolean flag!")


def launch_jobs(
    function_and_args,
    n_chunks,
    output_dir,
    timeout_min,
    num_gpus_per_node=0,
    chunks_to_run=None,
    local=False,
    slurm_partition=_DEFAULT_SLURM_PARTITION,
):
    # function_and_args is a list of the function to parallelise followed by its arguments
    # Create the executor
    print("Create the submitit Executor (can take time on FB cluster)")
    # Note that the folder will depend on the job_id, to easily track experiments
    log_test_dir = os.path.join(output_dir, f"log_test_{int(time.time())}", "%j")
    if local:
        executor = submitit.LocalExecutor(folder=log_test_dir)
    else:
        executor = submitit.AutoExecutor(folder=log_test_dir)
        executor.update_parameters(
            mem_gb=8,
            gpus_per_node=num_gpus_per_node,
            tasks_per_node=max(1, num_gpus_per_node),  # one task per GPU
            cpus_per_task=4,
            nodes=1,
            slurm_partition=slurm_partition,
            slurm_constraint="pascal",
        )

        executor.update_parameters(slurm_array_parallelism=n_chunks + 1)
    executor.update_parameters(timeout_min=timeout_min)
    jobs = executor.map_array(*function_and_args)
    print("Jobs launched...", flush=True)

    return jobs


def launch_and_monitor_jobs_w_args(
    function,
    get_parameters,
    args,
    num_gpus_per_node=0,
    slurm_partition=_DEFAULT_SLURM_PARTITION,
):
    output_dir = os.path.abspath(args.output_path)
    function_and_args = [function] + get_parameters(args)

    jobs = launch_jobs(
        function_and_args,
        args.total_chunks,
        output_dir,
        args.timeout_min,
        num_gpus_per_node=num_gpus_per_node,
        local=args.local if hasattr(args, "local") else False,
        slurm_partition=slurm_partition,
    )
    submitit.helpers.monitor_jobs(jobs)


def build_default_parser():
    parser = argparse.ArgumentParser(description="Process Command-line Arguments")
    parser.add_argument(
        "--total_chunks",
        default=1,
        type=int,
        action="store",
        help="Total number of chunks",
    )
    parser.add_argument(
        "--chunks_to_run",
        default=None,
        type=str,
        action="store",
        help="Id of chunks to run (e.g. for failed runs), separated by a comma",
    )
    parser.add_argument(
        "--timeout_min",
        default=4000,
        type=int,
        action="store",
        help="Timeout (in minutes) for the jobs",
    )
    parser.add_argument(
        "--output_path",
        default=None,
        action="store",
        help="The base path of the videos",
    )
    parser.add_argument(
        "--lang",
        default=None,
        action="store",
        help="Language, should be go, rust, java or cpp",
    )

    parser.add_argument(
        "--local",
        default=False,
        action="store_true",
        help="If set, runs locally instead of on the cluster",
    )
    return parser
