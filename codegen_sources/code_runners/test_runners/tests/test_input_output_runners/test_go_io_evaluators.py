from pathlib import Path
import os

from codegen_sources.preprocessing.lang_processors import LangProcessor
from codegen_sources.code_runners.test_runners import GoInputOutputEvaluator


go_processor = LangProcessor.processors["go"]()


ADDITION_PROGRAM = " ".join(
    go_processor.tokenize_code(
        """
func main() {
    var a, b int
    fmt.Scanf("%d %d", &a, &b)
    fmt.Print(a + b)
}"""
    )
)


def test_runner_on_addition_success():
    go_runner = GoInputOutputEvaluator()
    res, tests, failures, res_list = go_runner.check_outputs(
        ADDITION_PROGRAM,
        inputs=["1 2", "0 0"],
        outputs=["3\n", "0\n"],
        truncate_errors=None,
    )
    assert res == "success", (res, tests, failures)
    assert tests == 2
    assert failures == 0


def test_runner_on_addition_without_go_imports_fails():
    go_runner = GoInputOutputEvaluator(run_go_imports=False)
    res, tests, failures, res_list = go_runner.check_outputs(
        ADDITION_PROGRAM,
        inputs=["1 2", "0 0"],
        outputs=["3\n", "0\n"],
        truncate_errors=None,
    )
    assert res.startswith("compilation:"), (res, tests, failures)
    assert tests == 2
    assert failures == 2


def test_runner_on_addition_wrong_output_failure():
    go_runner = GoInputOutputEvaluator()
    res, tests, failures, res_list = go_runner.check_outputs(
        ADDITION_PROGRAM,
        inputs=["1 2", "0 0"],
        outputs=["3\n", "1\n"],
        truncate_errors=None,
    )
    assert res == "failure: actual 0 vs expected 1", (res, tests, failures, res_list)
    assert tests == 2
    assert failures == 1
    assert res_list[-1] == "failure: actual 0 vs expected 1"


def test_compilation_timeout():
    go_runner = GoInputOutputEvaluator(compilation_timeout=0.1)
    res, tests, failures, res_list = go_runner.check_outputs(
        ADDITION_PROGRAM,
        inputs=["1 2", "0 0"],
        outputs=["3\n", "0\n"],
        truncate_errors=None,
    )
    assert res == "compilation timeout: Compilation Timeout", (res, tests, failures)
    assert tests == 2
    assert failures == 2


def test_firejail_keeps_from_writing():
    if os.environ.get("CI", False):
        return
    go_runner = GoInputOutputEvaluator(timeout=20)
    test_out_path = Path(__file__).parent.joinpath(
        "test_output_should_not_be_written_go.out"
    )
    if test_out_path.exists():
        os.remove(test_out_path)
    write_to_file = (
        """
package main
import (
    "os"
)

func main() {
    f, _ := os.Create("%s")
    f.WriteString("Hello World")
}
"""
        % test_out_path
    )
    write_to_file = " ".join(go_processor.tokenize_code(write_to_file))
    res, tests, failures, res_list = go_runner.check_outputs(
        write_to_file, inputs=[""], outputs=[""], truncate_errors=None
    )
    assert not test_out_path.is_file(), f"{test_out_path} should not have been written"
    assert res == "success", (res, tests, failures)
    assert tests == 1
    assert failures == 0
