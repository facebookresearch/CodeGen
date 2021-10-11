# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from codegen_sources.preprocessing.preprocess import preprocess
from pathlib import Path
import os
import shutil

input_path = Path(__file__).parents[4].joinpath("data/test_dataset")
bpe_path = Path(__file__).parents[4].joinpath("data/bpe/cpp-java-python")


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


# Roberta Mode
def test_obfuscation_roberta_pipeline():
    args = AttrDict()
    args.update(
        {
            "input_path": str(input_path),
            "langs": ["java", "python"],
            "mode": "obfuscation",
            "local": "True",
            "train_splits": 1,
            "ncodes": 100,
            "percent_test_valid": 10,
            "bpe_mode": "roberta",
            "keep_comments": False,
            "local_parallelism": None,
            "tokenization_timeout": 2,
            "bpe_timeout": 2,
            "train_bpe_timeout": 5,
        }
    )
    preprocess(args)
    shutil.rmtree(input_path.joinpath("XLM-syml"))


def test_obfuscation_functions_roberta_pipeline():
    args = AttrDict()
    args.update(
        {
            "input_path": str(input_path),
            "langs": ["java", "python"],
            "mode": "obfuscation_functions",
            "local": "True",
            "train_splits": 1,
            "ncodes": 100,
            "percent_test_valid": 10,
            "bpe_mode": "roberta",
            "keep_comments": False,
            "local_parallelism": None,
            "tokenization_timeout": 2,
            "bpe_timeout": 2,
            "train_bpe_timeout": 5,
        }
    )
    preprocess(args)
    shutil.rmtree(input_path.joinpath("XLM-syml"))


def test_monolingual_roberta_pipeline():
    args = AttrDict()
    args.update(
        {
            "input_path": str(input_path),
            "langs": ["java", "python", "cpp"],
            "mode": "monolingual",
            "local": "True",
            "train_splits": 1,
            "ncodes": 100,
            "percent_test_valid": 10,
            "bpe_mode": "roberta",
            "keep_comments": False,
            "local_parallelism": None,
            "tokenization_timeout": 2,
            "bpe_timeout": 2,
            "train_bpe_timeout": 5,
        }
    )
    preprocess(args)
    shutil.rmtree(input_path.joinpath("XLM-syml"))


def test_monolingual_functions_roberta_pipeline():
    args = AttrDict()
    args.update(
        {
            "input_path": str(input_path),
            "langs": ["java", "python", "cpp"],
            "mode": "monolingual_functions",
            "local": "True",
            "train_splits": 1,
            "ncodes": 100,
            "percent_test_valid": 10,
            "bpe_mode": "roberta",
            "keep_comments": False,
            "local_parallelism": None,
            "tokenization_timeout": 2,
            "bpe_timeout": 2,
            "train_bpe_timeout": 5,
        }
    )
    preprocess(args)
    shutil.rmtree(input_path.joinpath("XLM-syml"))


# Fast BPE Mode
def test_monolingual_fast_pipeline():
    args = AttrDict()
    args.update(
        {
            "input_path": str(input_path),
            "langs": ["java", "python", "cpp"],
            "mode": "monolingual",
            "local": "True",
            "train_splits": 1,
            "ncodes": 100,
            "percent_test_valid": 10,
            "bpe_mode": "fast",
            "keep_comments": False,
            "local_parallelism": None,
            "fastbpe_code_path": None,
            "fastbpe_vocab_path": None,
            "fastbpe_use_vocab": False,
            "tokenization_timeout": 2,
            "bpe_timeout": 2,
            "train_bpe_timeout": 5,
        }
    )
    preprocess(args)
    shutil.rmtree(input_path.joinpath("XLM-syml"))


def test_monolingual_functions_fast_pipeline():
    args = AttrDict()
    args.update(
        {
            "input_path": str(input_path),
            "langs": ["java", "python", "cpp"],
            "mode": "monolingual_functions",
            "local": "True",
            "train_splits": 1,
            "ncodes": 100,
            "percent_test_valid": 10,
            "bpe_mode": "fast",
            "keep_comments": False,
            "local_parallelism": None,
            "fastbpe_code_path": None,
            "fastbpe_vocab_path": None,
            "fastbpe_use_vocab": False,
            "tokenization_timeout": 2,
            "bpe_timeout": 2,
            "train_bpe_timeout": 5,
        }
    )
    preprocess(args)
    shutil.rmtree(input_path.joinpath("XLM-syml"))


def test_monolingual_functions_fast_pipeline_keep_comments():
    args = AttrDict()
    args.update(
        {
            "input_path": str(input_path),
            "langs": ["java", "python", "cpp"],
            "mode": "monolingual_functions",
            "local": "True",
            "train_splits": 1,
            "ncodes": 100,
            "percent_test_valid": 10,
            "bpe_mode": "fast",
            "keep_comments": True,
            "local_parallelism": None,
            "fastbpe_code_path": None,
            "fastbpe_vocab_path": None,
            "fastbpe_use_vocab": False,
            "tokenization_timeout": 2,
            "bpe_timeout": 2,
            "train_bpe_timeout": 5,
        }
    )
    preprocess(args)
    shutil.rmtree(input_path.joinpath("XLM-syml"))


def test_obfuscation_fast_pipeline():
    args = AttrDict()
    args.update(
        {
            "input_path": str(input_path),
            "langs": ["java", "python"],
            "mode": "obfuscation",
            "local": "True",
            "train_splits": 1,
            "percent_test_valid": 10,
            "bpe_mode": "fast",
            "keep_comments": False,
            "local_parallelism": None,
            "fastbpe_code_path": f"{os.path.abspath(bpe_path.joinpath('codes'))}",
            "fastbpe_vocab_path": f"{os.path.abspath(bpe_path.joinpath('vocab'))}",
            "fastbpe_use_vocab": False,
            "ncodes": 50000,
            "tokenization_timeout": 2,
            "bpe_timeout": 2,
            "train_bpe_timeout": 5,
        }
    )
    preprocess(args)
    shutil.rmtree(input_path.joinpath("XLM-syml"))


def test_obfuscation_functions_fast_pipeline():
    args = AttrDict()
    args.update(
        {
            "input_path": str(input_path),
            "langs": ["java", "python"],
            "mode": "obfuscation_functions",
            "local": "True",
            "train_splits": 1,
            "percent_test_valid": 10,
            "bpe_mode": "fast",
            "keep_comments": False,
            "local_parallelism": None,
            "fastbpe_code_path": f"{os.path.abspath(bpe_path.joinpath('codes'))}",
            "fastbpe_vocab_path": f"{os.path.abspath(bpe_path.joinpath('vocab'))}",
            "fastbpe_use_vocab": False,
            "ncodes": 50000,
            "tokenization_timeout": 2,
            "bpe_timeout": 2,
            "train_bpe_timeout": 5,
        }
    )
    preprocess(args)
    shutil.rmtree(input_path.joinpath("XLM-syml"))
