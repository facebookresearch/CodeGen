# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import os
import pathlib
import signal
import subprocess
import typing as tp
from pathlib import Path

from .runner_errors import Timeout, CompilationError
from ..model.src.utils import get_java_bin_path

FIREJAIL_PROFILE = Path(__file__).parent.joinpath("firejail_sandbox.profile")
assert FIREJAIL_PROFILE.is_file(), f"Missing firejail profile in {FIREJAIL_PROFILE}"

FIREJAIL_COMMAND = f"firejail --quiet --profile={FIREJAIL_PROFILE}"
MAX_VIRTUAL_MEMORY = 2 * 1024 * 1024 * 1024  # 2 GB


def limit_virtual_memory(max_virtual_memory):
    # We do a soft limit in order to be able to change the limit later if needed
    return f"ulimit -S -v {max_virtual_memory}"


def _handle_timeouts(
    proc: subprocess.Popen, timeout: float
) -> tp.Tuple[bytes, bytes, int]:
    try:
        out, err = proc.communicate(timeout=timeout)
        return out, err, proc.returncode
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)  # send signal to the process group
        except ProcessLookupError:
            pass
        _ = proc.communicate()
        raise Timeout
    except KeyboardInterrupt:
        os.killpg(proc.pid, signal.SIGKILL)
        raise


USELESS_WARNINGS_END = "no version information available (required by /bin/bash)\n"
RUSTC_PATH = pathlib.Path.home().joinpath(".cargo", "bin", "rustc")
GO_IMPORTS_PATH = Path.home().joinpath("go", "bin", "goimports")


def compile_cpp(code_path: Path, compilation_timeout: float, output_path: Path):
    compilation_cmd = f"g++ -o {output_path} {code_path} -lgtest -pthread "
    try:
        proc = subprocess.Popen(
            compilation_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            executable="/bin/bash",
            preexec_fn=os.setsid,
        )
        comp_out, comp_err, ret_code = _handle_timeouts(proc, compilation_timeout)
    except Timeout:
        raise Timeout("Compilation Timeout")
    if proc.returncode != 0:
        raise CompilationError(comp_err.decode(errors="replace"))


def compile_java(code_path: Path, compilation_timeout: float):
    try:
        proc = subprocess.Popen(
            f"cd {code_path.parent} && {os.path.join(get_java_bin_path(), 'javac')} "
            + code_path.name,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            executable="/bin/bash",
        )
        out, err, ret_code = _handle_timeouts(proc, compilation_timeout)
    except Timeout:
        raise Timeout("Compilation Timeout")

    if proc.returncode != 0:
        raise CompilationError(err.decode(errors="replace"))


def compile_rust(code_path: Path, compilation_timeout: float, output_path: Path):
    assert RUSTC_PATH.is_file(), f"rustc not found: {RUSTC_PATH}"
    try:
        proc = subprocess.Popen(
            f"{RUSTC_PATH} -o {output_path} {code_path}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            executable="/bin/bash",
        )
        out, err, ret_code = _handle_timeouts(proc, compilation_timeout)
    except Timeout:
        raise Timeout("Compilation Timeout")

    if proc.returncode != 0:
        raise CompilationError(err.decode(errors="replace"))


def compile_go(
    code_path: Path,
    compilation_timeout: float,
    output_path: Path,
    run_go_imports: bool = True,
):
    ret_code = 1
    try:
        if run_go_imports:
            proc = subprocess.Popen(
                f"{GO_IMPORTS_PATH} -w {code_path}",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                executable="/bin/bash",
            )
            out, err, ret_code = _handle_timeouts(proc, compilation_timeout)
        if not run_go_imports or ret_code == 0:
            proc = subprocess.Popen(
                f"go build -o {output_path} {code_path}",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                executable="/bin/bash",
            )
            out, err, ret_code = _handle_timeouts(proc, compilation_timeout)
    except Timeout:
        raise Timeout("Compilation Timeout")

    if ret_code != 0:
        raise CompilationError(err.decode(errors="replace"))


def clean_err_output(e):
    return str(e).split(USELESS_WARNINGS_END, 1)[-1]
