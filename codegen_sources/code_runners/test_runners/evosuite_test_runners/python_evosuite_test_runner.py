# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import sys
from pathlib import Path

from codegen_sources.preprocessing.lang_processors import LangProcessor
from ...code_runner import RUN_ROOT_DIR
from ...runner_errors import (
    TestRuntimeError,
    CompilationError,
    InvalidTest,
)
from ..unittest_runner import UnitTestRunner

python_processor = LangProcessor.processors["python"]()


class PythonEvosuiteTestRunner(UnitTestRunner):
    def __init__(
        self,
        tmp_folder=Path(
            RUN_ROOT_DIR.joinpath("automatic_tests/tmp_tests_folder/python")
        ),
        timeout=15,
        num_subfolders=100,
        rand_char_filename=6,
    ):
        super().__init__(
            "python",
            tmp_folder=tmp_folder,
            timeout=timeout,
            num_subfolders=num_subfolders,
            rand_char_filename=rand_char_filename,
        )

    def init_env(self):
        super().init_env()
        self.env["PATH"] = f"{sys.executable.rstrip('python')}:{self.env['PATH']}"

    def _run_tests(
        self, function: str, test: str, tmp_path: Path,
    ):
        if "#TOFILL" not in test:
            raise InvalidTest("Missing #TOFILL")
        try:
            f_name = python_processor.get_function_name(function)
        except (ValueError, IndexError):
            raise CompilationError("No function definition")
        function = python_processor.detokenize_code(
            function.replace(f" {f_name.strip()} ", " f_filled ")
        )

        filled_test = test.replace("#TOFILL", function)
        test_path = self._write_file(filled_test, tmp_path)

        assert test_path.is_file()

        out, err, code = self._run_command(f"python {test_path}")
        return out, err, code

    def _eval_proc_state(self, out, err):
        stderr = self.clean_firejail(err)
        res_line = stderr.splitlines()
        if len(res_line) <= 2 or not (
            res_line[-1].startswith("OK") or res_line[-1].startswith("FAILED")
        ):
            raise TestRuntimeError(stderr)
        assert res_line[-3].startswith("Ran ")
        number_of_tests = int(res_line[-3].replace("Ran ", "").split(" ")[0])
        res_line = res_line[-1]
        if res_line.startswith("OK"):
            return "success", number_of_tests, 0
        else:
            assert res_line.startswith("FAILED (errors=") or res_line.startswith(
                "FAILED (failures="
            )
            number_failures = int(res_line.split("=")[-1].replace(")", ""))
            return "failure", number_of_tests, number_failures
