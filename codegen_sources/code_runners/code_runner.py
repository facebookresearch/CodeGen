import os
import shutil
import string
import subprocess
import typing as tp
import uuid
from pathlib import Path
from random import randint, choices
from subprocess import Popen

from .utils import (
    FIREJAIL_COMMAND,
    MAX_VIRTUAL_MEMORY,
    limit_virtual_memory,
    _handle_timeouts,
)
from ..model.src.constants import EXT

RUN_ROOT_DIR = Path.home().absolute() / "data/CodeGen/code_evaluation"
DEFAULT_TESTS_PATH = RUN_ROOT_DIR.joinpath("tmp_tests_folder")
print(f"Using {DEFAULT_TESTS_PATH} for temporary files.")


class CodeRunner:
    def __init__(
        self,
        lang: str,
        tmp_folder: Path = DEFAULT_TESTS_PATH,
        timeout: float = 15,
        num_subfolders: int = 100,
        rand_char_filename: int = 6,
        firejail: bool = True,
        limit_memory: bool = True,
    ) -> None:
        self.lang = lang
        self.timeout = timeout
        self.num_subfolders = num_subfolders
        self.rand_char_filename = rand_char_filename

        # subfolders to avoid having any folder containing too many files
        random_sub_folder = randint(0, self.num_subfolders)
        self.tmp_folder = Path(f"{str(tmp_folder)}_sub_{random_sub_folder}")
        self.tmp_folder.mkdir(exist_ok=True, parents=True)
        self.firejail = firejail
        self.limit_memory = limit_memory
        self.init_env()

    def init_env(self) -> None:
        self.env = os.environ.copy()

    def run(self, code: str) -> tp.Tuple[str, str, int]:
        """runs code and returns out, err, errcode"""
        raise ValueError("Not implemented")

    def _run_command(
        self,
        command: str,
        script_input: tp.Optional[str] = None,
        env_preparation: tp.Optional[str] = None,
    ) -> tp.Tuple[str, str, int]:
        """
        Runs a command, using optional script inputs and env preparation commands
        Uses safety parameters (memory limit, firejail) according to object attributes
        """
        preparation_cmd = f"{env_preparation} ; " if env_preparation is not None else ""
        pipe_input = f"echo '{script_input}' | " if script_input is not None else ""

        limit_memory_cmd = (
            f"{limit_virtual_memory(MAX_VIRTUAL_MEMORY)} ; "
            if self.limit_memory
            else ""
        )
        firejail_cmd = FIREJAIL_COMMAND if self.firejail else ""

        command = (
            f"{preparation_cmd} {limit_memory_cmd} "
            f"{pipe_input} {firejail_cmd} {command}"
        )
        proc = Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            executable="/bin/bash",
            preexec_fn=os.setsid,
            env=self.env,
        )
        out, err, code = _handle_timeouts(proc, timeout=self.timeout)
        return out.decode(errors="replace"), err.decode(errors="replace"), code

    def _clean(self, tmp_path: Path) -> None:
        """Cleans temporary folder used to run code"""
        assert str(self.tmp_folder) in str(tmp_path) and str(tmp_path) != str(
            self.tmp_folder
        ), f"cannot safely clean tmp folder {tmp_path}"
        if not tmp_path.exists():
            return
        shutil.rmtree(tmp_path, ignore_errors=True)

    def _get_tmp_folder(self) -> Path:
        """Gets temporary folder path for writing files to executes"""
        per_class_folder = uuid.uuid4()
        random_sub_folder = randint(0, self.num_subfolders)
        tmp_path = self.tmp_folder.joinpath(
            f"sub_{random_sub_folder}/tmp_{per_class_folder}"
        )
        tmp_path.mkdir(exist_ok=True, parents=True)
        return tmp_path

    def _write_file(
        self, code: str, out_folder: Path, filename: tp.Optional[str] = None
    ) -> Path:
        """
        Writes file to disk.
        If filename is None, a random filename will be chosen.
        It returns the path to the created file.
        """
        if filename is None:
            filename = "".join(choices(string.ascii_letters, k=self.rand_char_filename))
        test_path = out_folder.joinpath(f"{filename}{EXT[self.lang]}")
        with open(test_path, "w", encoding="utf-8") as o:
            o.write(code)
        return test_path

    @staticmethod
    def clean_firejail(out):
        return out.replace("\nParent is shutting down, bye...\n", "")
