from pathlib import Path

import os

from codegen_sources.preprocessing.lang_processors import LangProcessor
from codegen_sources.code_runners.test_runners import CppInputOutputEvaluator

cpp_processor = LangProcessor.processors["cpp"]()


ADDITION_PROGRAM = " ".join(
    cpp_processor.tokenize_code(
        """#include <iostream>

using namespace std;
int main() {
  int a, b;
  cin >> a >> b;
  cout << a + b << endl;
}"""
    )
)


def test_runner_on_addition_success():
    cpp_runner = CppInputOutputEvaluator()
    res, tests, failures, res_list = cpp_runner.check_outputs(
        ADDITION_PROGRAM,
        inputs=["1 2", "0 0"],
        outputs=["3\n", "0\n"],
        truncate_errors=None,
    )
    assert res == "success", (res, tests, failures)
    assert tests == 2
    assert failures == 0


def test_compilation_error():
    cpp_runner = CppInputOutputEvaluator()
    res, tests, failures, res_list = cpp_runner.check_outputs(
        ADDITION_PROGRAM.replace("int a", "a"),
        inputs=["1 2", "0 0"],
        outputs=["3\n", "0\n"],
        truncate_errors=None,
    )
    assert res.startswith("compilation"), (res, tests, failures)
    assert tests == 2
    assert failures == 2


def test_runner_on_addition_wrong_output_failure():
    cpp_runner = CppInputOutputEvaluator()
    res, tests, failures, res_list = cpp_runner.check_outputs(
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
    cpp_runner = CppInputOutputEvaluator(compilation_timeout=0.1)
    res, tests, failures, res_list = cpp_runner.check_outputs(
        ADDITION_PROGRAM,
        inputs=["1 2", "0 0"],
        outputs=["3\n", "0\n"],
        truncate_errors=None,
    )
    assert res == "compilation timeout: Compilation Timeout", (res, tests, failures)
    assert tests == 2
    assert failures == 2


def test_runtime_timeout():
    cpp_runner = CppInputOutputEvaluator(timeout=1)
    res, tests, failures, res_list = cpp_runner.check_outputs(
        "#include <unistd.h>\n"
        + ADDITION_PROGRAM.replace("main ( ) {", "main ( ) { sleep( 10 ) ;"),
        inputs=["1 2"],
        outputs=["3\n"],
        truncate_errors=None,
    )
    assert res == "timeout: ", (res, tests, failures)
    assert tests == 1
    assert failures == 1


def test_firejail_keeps_from_writing():
    if os.environ.get("CI", False):
        return
    cpp_runner = CppInputOutputEvaluator(timeout=20)
    test_out_path = Path(__file__).parent.joinpath(
        "test_output_should_not_be_written_cpp.out"
    )
    if test_out_path.exists():
        os.remove(test_out_path)
    write_to_file = (
        """#include <iostream>
#include <fstream>

using namespace std;
int main() {
        ofstream myfile;
        myfile.open ("%s");
        myfile << "hello" << endl;
        return 1;
    }
"""
        % test_out_path
    )
    write_to_file = " ".join(cpp_processor.tokenize_code(write_to_file))
    res, tests, failures, res_list = cpp_runner.check_outputs(
        write_to_file, inputs=[""], outputs=[""], truncate_errors=None
    )
    assert not test_out_path.is_file(), f"{test_out_path} should not have been written"
    assert res == "success", (res, tests, failures)
    assert tests == 1
    assert failures == 0
