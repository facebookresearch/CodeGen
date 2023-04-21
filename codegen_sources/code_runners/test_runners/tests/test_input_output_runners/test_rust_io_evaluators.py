from pathlib import Path
import os

from codegen_sources.preprocessing.lang_processors import LangProcessor
from codegen_sources.code_runners.test_runners import RustInputOutputEvaluator


rust_processor = LangProcessor.processors["rust"]()


ADDITION_PROGRAM = " ".join(
    rust_processor.tokenize_code(
        """
fn main() {
    let cin = std::io::stdin();
    let mut s = String::new();
    cin.read_line(&mut s).unwrap();
    let values = s
        .split_whitespace()
        .map(|x| x.parse::<i32>())
        .collect::<Result<Vec<i32>, _>>()
        .unwrap();
    assert!(values.len() == 2);
    let var1 = values[0];
    let var2 = values[1];
    println!("{}", var1 + var2);
}"""
    )
)


def test_runner_on_addition_success():
    rust_runner = RustInputOutputEvaluator()
    res, tests, failures, res_list = rust_runner.check_outputs(
        ADDITION_PROGRAM,
        inputs=["1 2", "0 0"],
        outputs=["3\n", "0\n"],
        truncate_errors=None,
    )
    assert res == "success", (res, tests, failures)
    assert tests == 2
    assert failures == 0


def test_runner_on_addition_wrong_output_failure():
    rust_runner = RustInputOutputEvaluator()
    res, tests, failures, res_list = rust_runner.check_outputs(
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
    rust_runner = RustInputOutputEvaluator(compilation_timeout=0.1)
    res, tests, failures, res_list = rust_runner.check_outputs(
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
    rust_runner = RustInputOutputEvaluator(timeout=20)
    test_out_path = Path(__file__).parent.joinpath(
        "test_output_should_not_be_written_rust.out"
    )
    if test_out_path.exists():
        os.remove(test_out_path)
    write_to_file = (
        """use std::fs::File;
use std::io::prelude::*;

fn main() -> std::io::Result<()> {
    let mut file = File::create("%s")?;
    file.write_all(b"Hello, world!")?;
    Ok(())
}
"""
        % test_out_path
    )
    write_to_file = " ".join(rust_processor.tokenize_code(write_to_file))
    res, tests, failures, res_list = rust_runner.check_outputs(
        write_to_file, inputs=[""], outputs=[""], truncate_errors=None
    )
    assert not test_out_path.is_file(), f"{test_out_path} should not have been written"
    assert res == "success", (res, tests, failures)
    assert tests == 1
    assert failures == 0
