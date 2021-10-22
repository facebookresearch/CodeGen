# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import os
import subprocess
import sys
import uuid
from pathlib import Path, PosixPath
from subprocess import Popen

from .evosuite_test_runners import (
    EvosuiteTestRunner,
    TestRuntimeError,
    CompilationError,
    InvalidTest,
    clean_firejail,
    FIREJAIL_PROFILE,
)
from ...model.src.utils import (
    TREE_SITTER_ROOT,
    limit_virtual_memory,
    MAX_VIRTUAL_MEMORY,
)
from ...preprocessing.lang_processors.lang_processor import LangProcessor

sys.path.append(str(Path(__file__).parents[3]))
print("adding to path", str(Path(__file__).parents[3]))


python_processor = LangProcessor.processors["python"](root_folder=TREE_SITTER_ROOT)


class PythonTestRunner(EvosuiteTestRunner):
    def __init__(
        self,
        tmp_folder=Path(
            Path.home().joinpath("data/CodeGen/automatic_tests/tmp_tests_folder/python")
        ),
        timeout=15,
    ):

        super().__init__(tmp_folder=tmp_folder, timeout=timeout)

    def _run_tests(
        self,
        function: str,
        test: str,
        tmp_path: PosixPath,
        classname: str = None,
        scaffolding: str = None,
    ):
        assert (
            scaffolding is None
        ), f"Scaffolding should be None for python tests, was {scaffolding}"
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
        test_path = self.write_test(filled_test, classname, tmp_path)

        assert test_path.is_file()

        test_cmd = f"{limit_virtual_memory(MAX_VIRTUAL_MEMORY)}; firejail --profile={FIREJAIL_PROFILE} python {test_path}"
        test_proc = Popen(
            test_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            executable="/bin/bash",
            preexec_fn=os.setsid,
        )
        return test_proc, tmp_path

    def _eval_proc_state(self, out, err):
        stderr = err.decode("utf-8", errors="replace")
        stderr = clean_firejail(stderr)
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

    @staticmethod
    def write_test(test, classname, out_folder):
        if classname is None:
            classname = "a"
        test_path = out_folder.joinpath(f"python_test_{classname}.py")
        with open(test_path, "w", encoding="utf-8") as o:
            o.write(test)
        return test_path
