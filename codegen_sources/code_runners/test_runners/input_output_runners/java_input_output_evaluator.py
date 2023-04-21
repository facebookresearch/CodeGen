# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import os
from pathlib import Path

from ...code_runner import RUN_ROOT_DIR
from ....model.src.utils import get_java_bin_path
from ....preprocessing.lang_processors import JavaProcessor
from .input_output_evaluator import InputOutputEvaluator
from ...utils import FIREJAIL_COMMAND, MAX_VIRTUAL_MEMORY, limit_virtual_memory
from ...utils import compile_java

java_processor = JavaProcessor()


class JavaInputOutputEvaluator(InputOutputEvaluator):
    def __init__(
        self,
        tmp_folder=Path(RUN_ROOT_DIR.joinpath("automatic_tests/tmp_tests_folder/java")),
        timeout: float = 15,
        compilation_timeout: float = 30,
        num_subfolders=100,
        rand_char_filename=6,
    ):
        super().__init__(
            "java",
            tmp_folder=tmp_folder,
            timeout=timeout,
            num_subfolders=num_subfolders,
            rand_char_filename=rand_char_filename,
        )
        self.compilation_timeout = compilation_timeout
        self.env = os.environ.copy()

    def init_env(self):
        super().init_env()
        self.env["PATH"] = f"{get_java_bin_path()}:{self.env['PATH']}"

    def _compile_program(self, program_path):
        bin_path = program_path.with_suffix(".class")
        compile_java(Path(program_path), self.compilation_timeout)
        return bin_path

    @staticmethod
    def _process(code):
        return java_processor.detokenize_code(code)

    def _run_program(
        self, executable_path: Path, input_val: str,
    ):
        test_cmd = f"{os.path.join(get_java_bin_path(), 'java')} {executable_path.name.replace('.class', '')}"
        return self._run_command(
            test_cmd, input_val, env_preparation=f"cd {executable_path.parent}"
        )
