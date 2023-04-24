# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from pathlib import Path
import typing as tp

from codegen_sources.model.src.evaluation.comp_acc_computation import (
    submit_functions,
    init_eval_scripts_folder,
    EVAL_SCRIPT_FOLDER,
)
from codegen_sources.preprocessing.lang_processors import LangProcessor

EVAL_SCRIPTS_ = "/tmp/eval_scripts/"
Path(EVAL_SCRIPTS_).mkdir(parents=True, exist_ok=True)


class Params:
    def __init__(self) -> None:
        self.eval_scripts_root = EVAL_SCRIPTS_
        self.eval_scripts_folders: tp.Dict[tp.Tuple[str, str, str], str] = {}


params = Params()


def test_submit_correct_function():
    lang1 = "cpp"
    lang2 = "cpp"
    data_set = "valid"
    hyp = """int numberOfTriangle ( int n ) {
    return 2 * pow ( 3 , n ) - 1 ;
  }"""
    ref = """int numberOfTriangles ( int n ) {
        int ans = 2 * ( pow ( 3 , n ) ) - 1 ;
        return ans ;
      }"""

    init_eval_scripts_folder(data_set, lang1, lang2, params)
    id = "NUMBER_TRIANGLES_N_MOVES_1"
    results_list, i = submit_functions(
        [hyp],
        id,
        ref,
        lang="cpp",
        outfolder=params.eval_scripts_folders[(lang1, lang2, data_set)],
        script_folder=EVAL_SCRIPT_FOLDER[data_set],
        retry_mismatching_types=False,
    )

    assert results_list == [("success", None)], results_list
    assert i == id, f"{i} != {id}"


def test_submit_correct_function_bug():
    lang1 = "cpp"
    lang2 = "cpp"
    data_set = "valid"
    ref = "int numberOfTriangles ( int n ) { int ans = 2 * ( pow ( 3 , n ) ) - 1 ; return ans ; }"

    hyp = "int numberOfTriangle( int n ) { return 2 * pow ( 3 , n ) - 1 ; }"

    # hyp = " ".join(lang_processor.tokenize_code(hyp))
    # ref = " ".join(lang_processor.tokenize_code(ref))
    init_eval_scripts_folder(data_set, lang1, lang2, params)
    id = "NUMBER_TRIANGLES_N_MOVES_1"
    results_list, i = submit_functions(
        [hyp],
        id,
        ref,
        lang="cpp",
        outfolder=params.eval_scripts_folders[(lang1, lang2, data_set)],
        script_folder=EVAL_SCRIPT_FOLDER[data_set],
        retry_mismatching_types=False,
    )

    assert results_list == [("success", None)], results_list
    assert i == id, f"{i} != {id}"
