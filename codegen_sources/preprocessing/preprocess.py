# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import logging
import multiprocessing
import os
from pathlib import Path
import argparse

import submitit


from codegen_sources.preprocessing.utils import bool_flag
from codegen_sources.preprocessing import bpe_modes
from codegen_sources.preprocessing import dataset_modes
from codegen_sources.model.src.logger import create_logger


def preprocess(args):

    create_logger(filepath=None, rank=0)
    logger = logging.getLogger()
    logger.info(f"Dataset pipeline for {args.input_path}")
    dataset_class = dataset_modes.DatasetMode.modes
    if args.mode not in dataset_class:
        raise ValueError(
            f"No mode {args.mode!r}, available are: {list(dataset_class.keys())}"
        )  # datasets must be added to dataset_modes/__init__ for auto-inclusion
    dataset_mode = dataset_class[args.mode]

    # bpe mode
    assert args.bpe_mode in ["fast", "roberta"]
    if args.bpe_mode == "fast":
        BPE_mode = bpe_modes.FastBPEMode(
            vocab_path=args.fastbpe_vocab_path,
            codes=args.fastbpe_code_path,
            use_vocab=args.fastbpe_use_vocab,
        )
    else:
        BPE_mode = bpe_modes.RobertaBPEMode()

    inpath = Path(args.input_path)
    executors = {
        name: submitit.AutoExecutor(
            folder=inpath.joinpath("log"), cluster="local" if args.local else None
        )
        for name in ["tokenization", "train_bpe", "apply_bpe"]
    }
    timeouts = {
        "tokenization": args.tokenization_timeout,
        "train_bpe": args.train_bpe_timeout,
        "apply_bpe": args.bpe_timeout,
    }
    for name, executor in executors.items():
        executor.update_parameters(timeout_min=timeouts[name])
        if not args.local:
            executor.update_parameters(
                slurm_partition="learnlab",
                mem_gb=args.job_mem,
                array_parallelism=200,
                cpus_per_task=args.cpu_per_task if name == "tokenization" else 1,
            )
    dataset = dataset_mode(
        folder=args.input_path,
        languages=args.langs,
        bpe=BPE_mode,
        nb_train_split=args.train_splits,
        keep_comments=args.keep_comments,
        repo_split=args.repo_split,
    )
    dataset.extract_data_and_tokenize(
        executor=executors["tokenization"],
        local_parallelism=args.local_parallelism,
        tokenize_line_timeout=args.tokenize_line_timeout,
    )

    dataset.get_train_test_valid_splits(
        percent_test=args.percent_test_valid,
        percent_valid=args.percent_test_valid,
        dedupe=True,
    )
    dataset.learn_bpe(ncodes=args.ncodes, executor=executors["train_bpe"])

    dataset.apply_bpe(
        executor=executors["apply_bpe"], local_parallelism=args.local_parallelism
    )
    dataset.get_vocab(executor=executors["train_bpe"])
    dataset.binarize(
        executor=executors["apply_bpe"], local_parallelism=args.local_parallelism
    )
    dataset.check_files_and_symlink_for_XLM()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("input_path", help="root folder")
    parser.add_argument(
        "--local",
        type=bool_flag,
        default=True,
        help="True if you want to run the processing pipeline locally, false if want to use submitit.",
    )
    parser.add_argument(
        "--local_parallelism",
        type=int,
        default=None,
        help="When running locally, number of files read at the same time.",
    )
    parser.add_argument(
        "--langs",
        nargs="+",
        default=["python", "java", "cpp"],
        help="list of languages to run on",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="monolingual_functions",
        choices=list(dataset_modes.DatasetMode.modes.keys()),
        help="Type of dataset.",
    )  # datasets must be added to dataset_modes/__init__ for auto-inclusion
    parser.add_argument(
        "--train_splits", type=int, default=8, help="Number of train splits."
    )
    parser.add_argument(
        "--job_mem",
        type=int,
        default=250,
        help="Memory in GB for jobs run on the cluster",
    )
    parser.add_argument(
        "--tokenization_timeout",
        type=int,
        default=1000,
        help="Timeout for tokenization/obfuscation jobs",
    )
    parser.add_argument(
        "--tokenize_line_timeout",
        type=int,
        default=240,
        help="Timeout for tokenizing and processing a line",
    )
    parser.add_argument(
        "--bpe_timeout", type=int, default=240, help="Timeout for bpe jobs"
    )
    parser.add_argument(
        "--train_bpe_timeout", type=int, default=500, help="Timeout for bpe jobs"
    )
    parser.add_argument(
        "--cpu_per_task",
        type=int,
        default=10,
        help="Number of cpus per job for the tokenization",
    )

    parser.add_argument(
        "--bpe_mode",
        type=str,
        default="fast",
        choices=["fast", "roberta"],
        help="Type of BPE, should be roberta or fast.",
    )
    parser.add_argument(
        "--fastbpe_use_vocab",
        type=bool_flag,
        default=False,
        help="Whether to use the vocab when applying BPE",
    )
    parser.add_argument(
        "--fastbpe_vocab_path",
        type=str,
        default=None,
        help="Path to existing fastbpe vocab",
    )
    parser.add_argument(
        "--keep_comments",
        type=bool_flag,
        default=False,
        help="Whether to keep the comments (does not happen with deobfuscation dataset).",
    )
    parser.add_argument(
        "--fastbpe_code_path",
        type=str,
        default=None,
        help="Path to existing fastbpe codes",
    )
    parser.add_argument(
        "--ncodes",
        type=int,
        default=50000,
        help="Number of codes to be learnt with fast bpe if no bpe codes is given.",
    )
    parser.add_argument(
        "--percent_test_valid",
        type=int,
        default=1,
        help="Percentage of data that will be put into test and valid sets.",
    )
    parser.add_argument(
        "--repo_split",
        type=bool_flag,
        default=True,
        help="Percentage of data that will be put into test and valid sets.",
    )
    args = parser.parse_args()
    args.input_path = os.path.abspath(args.input_path)
    multiprocessing.set_start_method("fork")
    preprocess(args)
