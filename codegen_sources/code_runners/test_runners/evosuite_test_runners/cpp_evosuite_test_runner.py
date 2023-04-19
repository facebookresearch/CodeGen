# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from pathlib import Path

from codegen_sources.preprocessing.lang_processors import LangProcessor
from ...code_runner import RUN_ROOT_DIR
from ...utils import compile_cpp
from ...runner_errors import (
    TestRuntimeError,
    CompilationError,
    InvalidTest,
)
from ..unittest_runner import UnitTestRunner
import typing as tp

NB_TESTS_STRING = "[==========] "

FAILED_STRING = "FAILED TEST"

PASSED_STRING = "[  PASSED  ]"

TOFILL = "//TOFILL"


cpp_processor = LangProcessor.processors["cpp"]()


class CppEvosuiteTestRunner(UnitTestRunner):
    def __init__(
        self,
        tmp_folder=Path(RUN_ROOT_DIR.joinpath("automatic_tests/tmp_tests_folder/cpp")),
        timeout=15,
        compilation_timeout=30,
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

    def _run_tests(
        self, function: str, test: str, tmp_path: Path,
    ):
        if TOFILL not in test:
            raise InvalidTest(f"Missing {TOFILL}")
        try:
            f_name = cpp_processor.get_function_name(function)
        except (ValueError, IndexError):
            raise CompilationError("No function definition")
        function = cpp_processor.detokenize_code(
            function.replace(f" {f_name.strip()} ", " f_filled ")
        )

        filled_test = test.replace(TOFILL, function)
        test_path = self._write_file(filled_test, tmp_path)

        assert test_path.is_file()
        bin_path = test_path.with_suffix("")
        compile_cpp(
            code_path=test_path,
            compilation_timeout=self.compilation_timeout,
            output_path=bin_path,
        )
        test_cmd = str(bin_path)
        return self._run_command(test_cmd)

    def _eval_proc_state(self, out: str, err: str) -> tp.Tuple[str, int, int]:
        """
        Takes out and err outputs
        returns success or error code, total number of tests, number of failures
        """
        res_line = out.splitlines()
        if len(res_line) <= 2 or not (
            res_line[-1].startswith(PASSED_STRING) or FAILED_STRING in res_line[-1]
        ):
            raise TestRuntimeError("\n".join(res_line))
        nb_tests_lines = [l for l in res_line if l.startswith(NB_TESTS_STRING)]
        assert len(nb_tests_lines) > 0
        nb_tests_line = nb_tests_lines[-1]
        number_of_tests = int(
            nb_tests_line.replace(NB_TESTS_STRING, "").split(" ")[0].strip()
        )
        res_last_line = res_line[-1]
        if res_last_line.startswith(PASSED_STRING):
            return "success", number_of_tests, 0
        else:
            assert FAILED_STRING in res_last_line
            number_failures = int(res_last_line.split()[0])
            return "failure", number_of_tests, number_failures
