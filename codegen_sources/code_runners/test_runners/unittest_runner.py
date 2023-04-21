# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import typing as tp
from pathlib import Path

from ..runner_errors import (
    TestRuntimeError,
    CompilationError,
    InvalidTest,
    MissingTest,
    Timeout,
)
from codegen_sources.code_runners.code_runner import CodeRunner, RUN_ROOT_DIR
from ..utils import clean_err_output


class UnitTestRunner(CodeRunner):
    def __init__(
        self,
        lang,
        tmp_folder=Path(RUN_ROOT_DIR.joinpath("automatic_tests/tmp_tests_folder")),
        timeout=15,
        num_subfolders=100,
        rand_char_filename=6,
    ):
        super().__init__(lang, tmp_folder, timeout, num_subfolders, rand_char_filename)

    def get_tests_results(
        self, function: str, test: str, truncate_errors=150,
    ):
        """Runs tests and returns success, number of tests, number of failures"""
        tmp_path = self._get_tmp_folder()

        res = None
        err = None
        out = None
        try:
            out, err, ret_code = self._run_tests(function, test, tmp_path)
        except MissingTest:
            res = ("missing_test", 0, "")
        except InvalidTest:
            res = ("invalid_test", 0, "")
        except CompilationError as e:
            res = (
                "compilation",
                0,
                str(clean_err_output(e))[:truncate_errors],
            )
        except Timeout as e:
            res = ("timeout", 0, str(clean_err_output(e))[:truncate_errors])
        finally:
            self._clean(tmp_path)
            if res is not None:
                return res
        try:
            res = self._eval_proc_state(out, err)  # type: ignore
        except TestRuntimeError:
            return "runtime", 0, ""
        return res

    def _run_tests(
        self, function: str, test: str, tmp_path: Path,
    ):
        raise NotImplementedError(
            "_run_tests should be implemented in inheriting class"
        )

    def _eval_proc_state(self, out: str, err: str) -> tp.Tuple[str, int, int]:
        """
        Takes out and err outputs
        returns success or error code, total number of tests, number of failures
        """
        raise NotImplementedError(
            "_eval_proc_state should be implemented in inheriting class"
        )
