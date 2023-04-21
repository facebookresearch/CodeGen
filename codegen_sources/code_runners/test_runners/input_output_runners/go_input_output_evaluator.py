# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from pathlib import Path

from .input_output_evaluator import InputOutputEvaluator
from ...code_runner import RUN_ROOT_DIR
from ....preprocessing.lang_processors.go_processor import GoProcessor
from ... import compile_go

go_processor = GoProcessor()


class GoInputOutputEvaluator(InputOutputEvaluator):
    def __init__(
        self,
        tmp_folder=Path(RUN_ROOT_DIR.joinpath("automatic_tests/tmp_tests_folder/go")),
        timeout: float = 15,
        compilation_timeout: float = 30,
        num_subfolders=100,
        rand_char_filename=6,
        run_go_imports=True,
    ):
        super().__init__(
            "go",
            tmp_folder=tmp_folder,
            timeout=timeout,
            num_subfolders=num_subfolders,
            rand_char_filename=rand_char_filename,
        )
        self.run_go_imports = run_go_imports
        self.compilation_timeout = compilation_timeout

    def _compile_program(self, program_path):
        bin_path = program_path.with_suffix("")
        compile_go(
            Path(program_path), self.compilation_timeout, bin_path, self.run_go_imports
        )
        return bin_path

    @staticmethod
    def _process(code):
        return go_processor.detokenize_code(code)
