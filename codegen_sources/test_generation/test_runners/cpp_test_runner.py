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
    FIREJAIL_PROFILE,
    Timeout,
)
from ...model.src.utils import (
    TREE_SITTER_ROOT,
    limit_virtual_memory,
    MAX_VIRTUAL_MEMORY,
)
from ...preprocessing.lang_processors.lang_processor import LangProcessor

NB_TESTS_STRING = "[==========] "

FAILED_STRING = "FAILED TEST"

PASSED_STRING = "[  PASSED  ]"

TOFILL = "//TOFILL"

sys.path.append(str(Path(__file__).parents[3]))
print("adding to path", str(Path(__file__).parents[3]))


cpp_processor = LangProcessor.processors["cpp"](root_folder=TREE_SITTER_ROOT)


class CppTestRunner(EvosuiteTestRunner):
    def __init__(
        self,
        tmp_folder=Path(
            Path.home().joinpath("data/CodeGen/automatic_tests/tmp_tests_folder/cpp")
        ),
        timeout=15,
        compilation_timeout=30,
    ):
        super().__init__(tmp_folder=tmp_folder, timeout=timeout)
        self.compilation_timeout = compilation_timeout

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
        ), f"Scaffolding should be None for cpp tests, was {scaffolding}"
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
        test_path = self.write_test(filled_test, classname, tmp_path)

        assert test_path.is_file()
        compilation_cmd = (
            f"g++ -o {test_path.with_suffix('')} {test_path} -lgtest -pthread "
        )
        try:
            proc = subprocess.Popen(
                compilation_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                executable="/bin/bash",
                preexec_fn=os.setsid,
            )
            comp_out, comp_err = self._handle_timeouts(proc, self.compilation_timeout)
        except Timeout:
            raise Timeout("Compilation Timeout")
        if proc.returncode != 0:
            raise CompilationError(comp_err.decode(errors="replace"))

        test_cmd = (
            f"{limit_virtual_memory(MAX_VIRTUAL_MEMORY)}; "
            f"firejail --profile={FIREJAIL_PROFILE} {test_path.with_suffix('')}"
        )
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
        res_line = out.decode("utf-8", errors="replace").splitlines()
        if len(res_line) <= 2 or not (
            res_line[-1].startswith(PASSED_STRING) or FAILED_STRING in res_line[-1]
        ):
            raise TestRuntimeError("\n".join(res_line))
        nb_tests_line = [l for l in res_line if l.startswith(NB_TESTS_STRING)]
        assert len(nb_tests_line) > 0
        nb_tests_line = nb_tests_line[-1]
        number_of_tests = int(
            nb_tests_line.replace(NB_TESTS_STRING, "").split(" ")[0].strip()
        )
        res_line = res_line[-1]
        if res_line.startswith(PASSED_STRING):
            return "success", number_of_tests, 0
        else:
            assert FAILED_STRING in res_line
            number_failures = int(res_line.split()[0])
            return "failure", number_of_tests, number_failures

    @staticmethod
    def write_test(test, classname, out_folder):
        if classname is None:
            classname = "a"
        test_path = out_folder.joinpath(f"test_{classname}.cpp")
        with open(test_path, "w", encoding="utf-8") as o:
            o.write(test)
        return test_path
