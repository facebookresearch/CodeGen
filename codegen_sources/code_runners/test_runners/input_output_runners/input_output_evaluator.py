# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import typing as tp
from pathlib import Path

from ...code_runner import CodeRunner, RUN_ROOT_DIR
from ...runner_errors import MissingTest, CompilationError, Timeout, TestRuntimeError
from ...utils import clean_err_output
from ...utils import FIREJAIL_COMMAND, MAX_VIRTUAL_MEMORY, limit_virtual_memory
import codegen_sources.preprocessing.lang_processors.java_processor


class InputOutputEvaluator(CodeRunner):
    def __init__(
        self,
        lang,
        tmp_folder=Path(RUN_ROOT_DIR.joinpath("automatic_tests/tmp_tests_folder")),
        timeout: float = 15,
        num_subfolders=100,
        rand_char_filename=6,
    ):
        super().__init__(lang, tmp_folder, timeout, num_subfolders, rand_char_filename)

    def check_outputs(
        self,
        program: str,
        inputs: tp.List[str],
        outputs: tp.List[str],
        truncate_errors=150,
    ):
        """Runs programs and checks how often the output is as expected"""
        assert len(inputs) == len(outputs)
        tmp_path = self._get_tmp_folder()
        classname = None
        if self.lang == "java":
            classname = codegen_sources.preprocessing.lang_processors.java_processor.JavaProcessor.get_class_name(
                tokenized_java=program
            )
        program_path = self._write_file(
            self._process(program), tmp_path, filename=classname
        )
        res = None
        executable_path: tp.Optional[Path] = None
        try:
            executable_path = self._compile_program(program_path)
        except MissingTest:
            res = "missing_test"
        except CompilationError as e:
            e = clean_err_output(e)
            res = f"compilation: {clean_err_output(str(e))[:truncate_errors]}"
        except Timeout as e:
            e = clean_err_output(e)
            res = f"compilation timeout: {clean_err_output(str(e))[:truncate_errors]}"
        if res is not None:
            self._clean(tmp_path)
            return res, len(inputs), len(inputs), [res]

        results = []
        assert executable_path is not None
        assert executable_path.is_file()
        for _input, _output in zip(inputs, outputs):
            out, err, ret_code = None, None, None
            res = None
            try:
                out, err, ret_code = self._run_program(executable_path, _input)
            except Timeout as e:
                res = f"timeout: {clean_err_output(str(e))[:truncate_errors]}"
            if res is None:
                try:
                    res = self._eval_output(out, err, ret_code, _output)
                except TestRuntimeError:
                    res = "runtime"
            results.append(res)
        self._clean(tmp_path)
        num_failures = len([res for res in results if not res.startswith("success")])

        if len([r for r in results if r.startswith("runtime")]) > 0:
            short_result = [r for r in results if r.startswith("runtime")][0]
        elif len([r for r in results if r.startswith("failure")]) > 0:
            short_result = [r for r in results if r.startswith("failure")][0]
        elif len([r for r in results if r.startswith("timeout")]) > 0:
            short_result = [r for r in results if r.startswith("timeout")][0]
        else:
            assert num_failures == 0, results
            short_result = "success"
        return short_result, len(inputs), num_failures, results

    def _run_program(
        self, executable_path: Path, input_val: str,
    ):
        test_cmd = str(executable_path)
        return self._run_command(test_cmd, input_val)

    def _eval_output(self, out, err, ret_code, output: str):
        actual = out.strip()
        if actual == output.strip():
            return "success"
        else:
            if ret_code != 0:
                return f"runtime: {err.decode('utf8')}"
            else:
                return f"failure: actual {actual} vs expected {output.strip()}"

    @staticmethod
    def _process(code: str):
        raise NotImplementedError(
            "_process_code should be implemented in inheriting class"
        )

    def _compile_program(self, program_path):
        raise NotImplementedError(
            "_compile_program should be implemented in inheriting class"
        )
