# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
# Translate sentences from the input stream.
# The model will be faster is sentences are sorted by length.
# Input sentences must have the same tokenization and BPE codes than the ones used in the model.
#

import sys
from pathlib import Path

ROOT_PATH = Path(__file__).absolute().parents[2]


def chunks_df(df, n):
    """Yield successive n-sized chunks from df"""
    for i in range(0, len(df), n):
        yield df.iloc[i : i + n]


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def compute_results_one_test(test, translations, test_runner, truncate_errors=150):
    # executor = ThreadPoolExecutor(max_workers=5)
    # return list(executor.map(test_runner.get_tests_results, translations, repeat(test)))
    return [
        test_runner.get_tests_results(code, test=test, truncate_errors=truncate_errors)
        for code in translations
    ]


def get_beam_size(input_df, results_columns="translated_python_functions_beam_"):
    beam_size = 0
    while f"{results_columns}{beam_size}" in input_df:
        beam_size += 1
    return beam_size


def add_root_to_path():
    print(f"adding {ROOT_PATH} to path")
    sys.path.append(str(ROOT_PATH))
