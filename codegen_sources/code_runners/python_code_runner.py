import os
import sys
import typing as tp
from pathlib import Path

from .code_runner import CodeRunner, DEFAULT_TESTS_PATH

PYTHON_ENV = os.environ.copy()
PYTHON_ENV["PATH"] = f"{sys.executable.rstrip('python')}:{PYTHON_ENV['PATH']}"


class PythonCodeRunner(CodeRunner):
    def __init__(
        self,
        tmp_folder: Path = DEFAULT_TESTS_PATH,
        timeout: int = 15,
        num_subfolders: int = 100,
        rand_char_filename: int = 6,
        firejail: bool = True,
    ) -> None:
        super().__init__(
            "python",
            tmp_folder=tmp_folder,
            timeout=timeout,
            num_subfolders=num_subfolders,
            rand_char_filename=rand_char_filename,
            firejail=firejail,
        )

    def init_env(self) -> None:
        super().init_env()
        # add current python env to path
        self.env["PATH"] = f"{sys.executable.rstrip('python')}:{self.env['PATH']}"

    def run(
        self, code: str, script_input: tp.Optional[str] = None
    ) -> tp.Tuple[str, str, int]:
        folder = self._get_tmp_folder()

        file_path = self._write_file(code, folder)
        try:
            out, err, err_code = self._run_command(f"python {file_path}", script_input)
        except KeyboardInterrupt:
            raise
        finally:
            self._clean(folder)
        return out, err, err_code
