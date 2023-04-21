# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from pathlib import Path

from .input_output_evaluator import InputOutputEvaluator
from ...code_runner import RUN_ROOT_DIR
from ....preprocessing.lang_processors.cpp_processor import CppProcessor
from ...utils import compile_cpp

cpp_processor = CppProcessor()


class CppInputOutputEvaluator(InputOutputEvaluator):
    def __init__(
        self,
        tmp_folder=Path(RUN_ROOT_DIR.joinpath("automatic_tests/tmp_tests_folder/cpp")),
        timeout: float = 15,
        compilation_timeout: float = 30,
        num_subfolders=100,
        rand_char_filename=6,
    ):
        super().__init__(
            "cpp",
            tmp_folder=tmp_folder,
            timeout=timeout,
            num_subfolders=num_subfolders,
            rand_char_filename=rand_char_filename,
        )
        self.compilation_timeout = compilation_timeout

    def _compile_program(self, program_path):
        bin_path = program_path.with_suffix("")
        compile_cpp(Path(program_path), self.compilation_timeout, bin_path)
        return bin_path

    @staticmethod
    def _process(code):
        return cpp_processor.detokenize_code(code)
