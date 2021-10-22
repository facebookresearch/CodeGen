# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import subprocess
from pathlib import Path, PosixPath

import os

import signal

import shutil

import uuid
from random import randint

NUM_SUBFOLDERS = 100

FIREJAIL_PROFILE = Path(__file__).parent.joinpath("firejail_sandbox.profile")
assert FIREJAIL_PROFILE.is_file()
SUPPORTED_LANGUAGES_FOR_TESTS = {"python", "cpp", "java"}


class CompilationError(Exception):
    pass


class TestRuntimeError(Exception):
    pass


class MissingTest(Exception):
    pass


class InvalidTest(Exception):
    pass


class Timeout(Exception):
    pass


class EvosuiteTestRunner:
    def __init__(
        self,
        tmp_folder=Path(
            Path.home().joinpath("data/CodeGen/automatic_tests/tmp_tests_folder")
        ),
        timeout=15,
    ):
        self.timeout = timeout
        # subfolders to avoid having any folder containing too many files
        random_sub_folder = randint(0, NUM_SUBFOLDERS)
        self.tmp_folder = Path(f"{str(tmp_folder)}_sub_{random_sub_folder}")
        self.tmp_folder.mkdir(exist_ok=True, parents=True)

    def get_tests_results(
        self,
        function: str,
        test: str,
        classname=None,
        scaffolding: str = None,
        truncate_errors=150,
    ):
        """Runs tests and returns success, number of tests, number of failures"""
        per_class_folder = uuid.uuid4()
        random_sub_folder = randint(0, NUM_SUBFOLDERS)
        tmp_path = self.tmp_folder.joinpath(
            f"sub_{random_sub_folder}/tmp_{per_class_folder}"
        )
        tmp_path.mkdir(exist_ok=True, parents=True)

        res = None
        try:
            proc, tmp_path = self._run_tests(
                function, test, tmp_path, classname, scaffolding
            )
            out, err = self._handle_timeouts(proc, timeout=self.timeout)
        except MissingTest:
            res = ("missing_test", 0, 0)
        except InvalidTest:
            res = ("invalid_test", 0, 0)
        except CompilationError as e:
            res = (
                "compilation",
                0,
                str(e)[:truncate_errors],
            )
        except Timeout as e:
            res = ("timeout", 0, str(e)[:truncate_errors])
        finally:
            self.cleanup_tmp_folder(tmp_path)
            if res is not None:
                return res
        try:
            res = self._eval_proc_state(out, err)
        except TestRuntimeError:
            return "runtime", 0, 0
        return res

    def _handle_timeouts(self, proc, timeout):
        try:
            return proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)  # send signal to the process group
            _ = proc.communicate()
            raise Timeout
        except KeyboardInterrupt:
            os.killpg(proc.pid, signal.SIGKILL)
            raise

    def _run_tests(
        self,
        function: str,
        test: str,
        tmp_path: PosixPath,
        classname: str = None,
        scaffolding: str = None,
    ):
        raise NotImplementedError(
            "_run_tests should be implemented in inheriting class"
        )

    def _eval_proc_state(self, out, err):
        raise NotImplementedError(
            "_eval_proc_state should be implemented in inheriting class"
        )

    def cleanup_tmp_folder(self, tmp_path: PosixPath):
        assert str(self.tmp_folder) in str(tmp_path) and str(tmp_path) != str(
            self.tmp_folder
        ), f"cannot safely clean tmp folder {tmp_path}"
        if not tmp_path.exists():
            return
        shutil.rmtree(tmp_path, ignore_errors=True)


def clean_firejail(out):
    return out.replace("\nParent is shutting down, bye...\n", "")
