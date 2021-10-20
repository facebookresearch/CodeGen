# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import pytest

from codegen_sources.preprocessing.lang_processors.java_processor import JavaProcessor
from pathlib import Path

from codegen_sources.preprocessing.lang_processors.tokenization_utils import (
    process_string,
    tokenize_string,
    detokenize_string,
)

processor = JavaProcessor(root_folder=Path(__file__).parents[4].joinpath("tree-sitter"))

TESTS = []
TESTS.append(
    (
        "lalala! this: is a string lala?",
        [
            "lalala",
            "!",
            "▁",
            "this",
            ":",
            "▁",
            "is",
            "▁",
            "a",
            "▁",
            "string",
            "▁",
            "lala",
            "?",
        ],
    )
)
TESTS.append(("isn't it nice?", ["isn", "'", "t", "▁", "it", "▁", "nice", "?"]))


def test_java_tokenizer_discarding_comments():
    for i, (x, y) in enumerate(TESTS):
        y_ = tokenize_string(x)
        if y_ != y:
            line_diff = [
                j for j, (line, line_) in enumerate(zip(y, y_)) if line != line_
            ]
            line_diff = line_diff[-1] if len(line_diff) > 0 else -1
            raise Exception(
                f"Difference at {line_diff}\nExpected:\n==========\n{y}\nbut found:\n==========\n{y_}"
            )


def test_string_tokenization_invertible():
    for i, (x, y) in enumerate(TESTS):
        y_ = tokenize_string(x)
        x_ = detokenize_string(y_)
        if x_ != x:
            line_diff = [
                j for j, (line, line_) in enumerate(zip(x, x_)) if line != line_
            ]
            line_diff = line_diff[-1] if len(line_diff) > 0 else -1
            raise Exception(
                f"Difference at {line_diff}\nExpected:\n==========\n{x}\nbut found:\n==========\n{x_}"
            )
