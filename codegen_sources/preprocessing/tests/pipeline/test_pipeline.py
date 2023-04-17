# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import logging
import shutil
import unittest
from pathlib import Path

import pytest


from codegen_sources.preprocessing.preprocess import preprocess
from codegen_sources.model.src.utils import AttrDict

RELATIVE_TOLERANCE = 0.005

input_path = Path(__file__).parents[4].joinpath("data/sample_dataset")
bpe_path = Path(__file__).parents[4].joinpath("data/bpe/cpp-java-python")
logger = logging.getLogger(__name__)


def _deactivate_in_ci() -> None:
    """Diminish number of used processors in the CI since it triggers
    memory errors (with Roberta mode)
    """
    if os.environ.get("CIRCLECI", False):
        # might be related to downloading the model, and/or to load in multiple
        # processes
        raise unittest.SkipTest("Roberta is deactivated because of OOM in the CI")


DEFAULT_PARAMETERS = AttrDict(
    {
        "input_path": str(input_path),
        "local": "True",
        "train_splits": 1,
        "ncodes": 100,
        "percent_test_valid": 10,
        "keep_comments": False,
        "local_parallelism": None,
        "tokenization_timeout": 2,
        "bpe_timeout": 2,
        "train_bpe_timeout": 5,
        "repo_split": True,
        "fastbpe_code_path": None,
        "fastbpe_vocab_path": None,
        "fastbpe_use_vocab": False,
        "tokenize_line_timeout": 60,
    }
)


@pytest.fixture(autouse=True)
def setup() -> None:
    subdirs = ["log", "XLM-syml"]
    for name in subdirs:
        subpath = input_path / name
        if subpath.is_dir():
            try:
                shutil.rmtree(subpath)
            except OSError as e:
                logger.warning(f"Could not delete the folder ({subpath}):\n{e}")
    for f in input_path.glob("*"):
        if not f.name.endswith(".json.gz") and f.name not in subdirs:
            try:
                f.unlink()
            except OSError as e:
                if not f.name.startswith(".nfs"):
                    raise e
                logger.warning(f"Could not delete file:\n{e}")


def check_number_lines_is(nb):
    assert abs(count_bpe_lines() - nb) / nb < RELATIVE_TOLERANCE, count_bpe_lines()


def count_bpe_lines():
    tok_files = list(input_path.glob("*.bpe")) + list(input_path.glob("*.bperob"))
    count = 0
    for path in tok_files:
        with open(path) as f:
            count += len(f.readlines())
    return count


# Roberta Mode
def test_obfuscation_roberta_pipeline() -> None:
    args = AttrDict(DEFAULT_PARAMETERS)
    args.update(
        {"langs": ["java", "python"], "mode": "obfuscation", "bpe_mode": "roberta",}
    )
    _deactivate_in_ci()
    preprocess(args)
    # shutil.rmtree(input_path.joinpath("XLM-syml"))
    check_number_lines_is(316)


def test_obfuscation_functions_roberta_pipeline() -> None:
    args = AttrDict(DEFAULT_PARAMETERS)
    args.update(
        {
            "langs": ["java", "python"],
            "mode": "obfuscation_functions",
            "bpe_mode": "roberta",
        }
    )
    _deactivate_in_ci()
    preprocess(args)
    # shutil.rmtree(input_path.joinpath("XLM-syml"))
    check_number_lines_is(2710)


def test_monolingual_roberta_pipeline() -> None:
    args = AttrDict(DEFAULT_PARAMETERS)
    args.update(
        {
            "langs": ["java", "python", "cpp"],
            "mode": "monolingual",
            "bpe_mode": "roberta",
        }
    )
    _deactivate_in_ci()
    preprocess(args)
    # shutil.rmtree(input_path.joinpath("XLM-syml"))
    check_number_lines_is(294)


def test_monolingual_functions_roberta_pipeline() -> None:
    args = AttrDict(DEFAULT_PARAMETERS)
    args.update(
        {
            "langs": ["java", "python", "cpp"],
            "mode": "monolingual_functions",
            "bpe_mode": "roberta",
        }
    )
    _deactivate_in_ci()
    preprocess(args)
    # shutil.rmtree(input_path.joinpath("XLM-syml"))
    check_number_lines_is(3717)


# Fast BPE Mode
def test_monolingual_fast_pipeline() -> None:
    args = AttrDict(DEFAULT_PARAMETERS)
    args.update(
        {
            "langs": ["java", "python", "cpp"],
            "mode": "monolingual",
            "bpe_mode": "fast",
            "fastbpe_code_path": None,
            "fastbpe_vocab_path": None,
            "fastbpe_use_vocab": False,
        }
    )
    preprocess(args)
    # shutil.rmtree(input_path.joinpath("XLM-syml"))
    check_number_lines_is(529)


def test_monolingual_functions_fast_pipeline() -> None:
    args = AttrDict(DEFAULT_PARAMETERS)
    args.update(
        {
            "langs": ["java", "python", "cpp"],
            "mode": "monolingual_functions",
            "bpe_mode": "fast",
            "fastbpe_code_path": None,
            "fastbpe_vocab_path": None,
            "fastbpe_use_vocab": False,
        }
    )
    preprocess(args)
    # shutil.rmtree(input_path.joinpath("XLM-syml"))
    check_number_lines_is(6629)


def test_monolingual_functions_fast_pipeline_keep_comments() -> None:
    args = AttrDict(DEFAULT_PARAMETERS)
    args.update(
        {
            "langs": ["java", "python", "cpp"],
            "mode": "monolingual_functions",
            "bpe_mode": "fast",
            "keep_comments": True,
            "fastbpe_code_path": None,
            "fastbpe_vocab_path": None,
            "fastbpe_use_vocab": False,
        }
    )
    preprocess(args)
    # shutil.rmtree(input_path.joinpath("XLM-syml"))
    check_number_lines_is(6616)


def test_monolingual_functions_sentencepiece_pipeline_keep_comments() -> None:
    args = AttrDict(DEFAULT_PARAMETERS)
    args.update(
        {
            "langs": ["java", "python", "cpp"],
            "mode": "sentence_piece_function",
            "bpe_mode": "fast",
            "keep_comments": True,
        }
    )
    preprocess(args)
    # shutil.rmtree(input_path.joinpath("XLM-syml"))
    check_number_lines_is(3728)
    # TODO: why is it so much smaller?


def test_obfuscation_fast_pipeline() -> None:
    args = AttrDict(DEFAULT_PARAMETERS)
    args.update(
        {
            "langs": ["java", "python"],
            "mode": "obfuscation",
            "bpe_mode": "fast",
            "fastbpe_code_path": f"{os.path.abspath(bpe_path.joinpath('codes'))}",
            "fastbpe_vocab_path": f"{os.path.abspath(bpe_path.joinpath('vocab'))}",
            "fastbpe_use_vocab": False,
            "ncodes": 50000,
        }
    )
    preprocess(args)
    # shutil.rmtree(input_path.joinpath("XLM-syml"))
    check_number_lines_is(316)


def test_obfuscation_functions_fast_pipeline() -> None:
    args = AttrDict(DEFAULT_PARAMETERS)
    args.update(
        {
            "langs": ["java", "python"],
            "mode": "obfuscation_functions",
            "bpe_mode": "fast",
            "fastbpe_code_path": f"{os.path.abspath(bpe_path.joinpath('codes'))}",
            "fastbpe_vocab_path": f"{os.path.abspath(bpe_path.joinpath('vocab'))}",
            "fastbpe_use_vocab": False,
            "ncodes": 50000,
        }
    )
    preprocess(args)
    # shutil.rmtree(input_path.joinpath("XLM-syml"))
    check_number_lines_is(2656)


def test_python_type_hints_fast_pipeline() -> None:
    args = AttrDict(DEFAULT_PARAMETERS)
    args.update(
        {
            "langs": ["python"],
            "mode": "python_type_hints",
            "bpe_mode": "fast",
            "percent_test_valid": 20,
            "fastbpe_code_path": f"{(bpe_path / 'codes').absolute()}",
            "fastbpe_vocab_path": f"{(bpe_path / 'vocab').absolute()}",
            "fastbpe_use_vocab": False,
            "ncodes": 50000,
        }
    )
    preprocess(args)
    expected = input_path / "python.all.dictionary.tok"
    lines = expected.read_text("utf8").splitlines()
    assert len(lines) == 8
    assert lines[0] == "fernandog/Medusa | VAR_0 bool"
    check_number_lines_is(16)
