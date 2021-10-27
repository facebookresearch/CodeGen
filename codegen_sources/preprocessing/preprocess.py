# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from pathlib import Path

import argparse
from submitit import AutoExecutor, LocalExecutor

from codegen_sources.preprocessing.bpe_modes.fast_bpe_mode import FastBPEMode
from codegen_sources.preprocessing.bpe_modes.roberta_bpe_mode import RobertaBPEMode
from codegen_sources.preprocessing.dataset_modes.monolingual_functions_mode import (
    MonolingualFunctionsMode,
)

from codegen_sources.preprocessing.dataset_modes.monolingual_mode import MonolingualMode
from codegen_sources.preprocessing.dataset_modes.obfuscation_mode import ObfuscationMode
from codegen_sources.preprocessing.dataset_modes.obfuscation_functions_mode import (
    ObfuscationFunctionsMode,
)


from codegen_sources.model.src.logger import create_logger
import logging
import multiprocessing
import os

from codegen_sources.preprocessing.utils import bool_flag


def preprocess(args):

    create_logger(filepath=None, rank=0)
    logger = logging.getLogger()
    logger.info(f"Dataset pipeline for {args.input_path}")
    # dataset mode
    dataset_class = {
        "obfuscation": ObfuscationMode,
        "monolingual": MonolingualMode,
        "monolingual_functions": MonolingualFunctionsMode,
        "obfuscation_functions": ObfuscationFunctionsMode,
    }
    dataset_mode = dataset_class[args.mode]

    # bpe mode
    assert args.bpe_mode in ["fast", "roberta"]
    if args.bpe_mode == "fast":
        BPE_mode = FastBPEMode(
            vocab_path=args.fastbpe_vocab_path,
            codes=args.fastbpe_code_path,
            use_vocab=args.fastbpe_use_vocab,
        )
    else:
        BPE_mode = RobertaBPEMode()

    if args.local is False:
        cluster_tokenization = AutoExecutor(Path(args.input_path).joinpath("log"))
        cluster_tokenization.update_parameters(
            cpus_per_task=40,
            mem_gb=args.job_mem,
            slurm_partition="learnlab",
            array_parallelism=200,
        )
        cluster_train_bpe = AutoExecutor(Path(args.input_path).joinpath("log"))
        cluster_train_bpe.update_parameters(
            cpus_per_task=1, mem_gb=args.job_mem, slurm_partition="learnlab",
        )
        cluster_apply_bpe = AutoExecutor(Path(args.input_path).joinpath("log"))
        cluster_apply_bpe.update_parameters(
            cpus_per_task=1,
            mem_gb=args.job_mem,
            slurm_partition="learnlab",
            array_parallelism=200,
        )
    else:
        cluster_tokenization = LocalExecutor(Path(args.input_path).joinpath("log"))
        cluster_train_bpe = LocalExecutor(Path(args.input_path).joinpath("log"))
        cluster_apply_bpe = LocalExecutor(Path(args.input_path).joinpath("log"))
    cluster_tokenization.update_parameters(timeout_min=args.tokenization_timeout)
    cluster_train_bpe.update_parameters(timeout_min=args.train_bpe_timeout)
    cluster_apply_bpe.update_parameters(timeout_min=args.bpe_timeout)

    dataset = dataset_mode(
        folder=args.input_path,
        languages=args.langs,
        bpe=BPE_mode,
        nb_train_split=args.train_splits,
        keep_comments=args.keep_comments,
    )
    dataset.extract_data_and_tokenize(
        executor=cluster_tokenization, local_parallelism=args.local_parallelism
    )

    dataset.get_train_test_valid_splits(
        percent_test=args.percent_test_valid,
        percent_valid=args.percent_test_valid,
        dedupe=True,
    )
    dataset.learn_bpe(ncodes=args.ncodes, executor=cluster_train_bpe)

    dataset.apply_bpe(
        executor=cluster_apply_bpe, local_parallelism=args.local_parallelism
    )
    dataset.get_vocab(executor=cluster_train_bpe)
    dataset.binarize(
        executor=cluster_apply_bpe, local_parallelism=args.local_parallelism
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
        choices=[
            "obfuscation",
            "monolingual",
            "monolingual_functions",
            "obfuscation_functions",
        ],
        help="Type of dataset.",
    )
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
        default=500,
        help="Timeout for tokenization/obfuscation jobs",
    )
    parser.add_argument(
        "--bpe_timeout", type=int, default=240, help="Timeout for bpe jobs"
    )
    parser.add_argument(
        "--train_bpe_timeout", type=int, default=500, help="Timeout for bpe jobs"
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
    args = parser.parse_args()
    args.input_path = os.path.abspath(args.input_path)
    multiprocessing.set_start_method("fork")
    preprocess(args)
