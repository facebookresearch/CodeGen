# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from pathlib import Path

import os

from codegen_sources.test_generation.test_runners.cpp_test_runner import CppTestRunner
from codegen_sources.model.src.utils import TREE_SITTER_ROOT
from codegen_sources.preprocessing.lang_processors.lang_processor import LangProcessor

cpp_processor = LangProcessor.processors["cpp"](root_folder=TREE_SITTER_ROOT)


TEST_SIGMOID = """#include <iostream>
#include <cstdlib>
#include <string>
#include <vector>
#include <fstream>
#include <iomanip>
#include <bits/stdc++.h>
#include "gtest/gtest.h"

using namespace std;



//TOFILL


  TEST(EvoSuiteTest, test0){
      double double0 = f_filled(0.0);
      ASSERT_NEAR (0.5, double0, 1.0E-4);
  }


  TEST(EvoSuiteTest, test1){
      double double0 = f_filled((-49379.6829442));
      ASSERT_NEAR (0.0, double0, 1.0E-4);
  }


int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}"""


def test_runner_on_sigmoid_success():
    cpp_runner = CppTestRunner()
    sigmoid = """double sigmoid ( double input ){
    return 1.0 / ( 1.0 + ( exp ( - input ) ) );
    }"""
    sigmoid = " ".join(cpp_processor.tokenize_code(sigmoid))
    res, tests, failures = cpp_runner.get_tests_results(sigmoid, TEST_SIGMOID)
    assert res == "success", (res, tests, failures)
    assert tests == 2
    assert failures == 0


def test_runner_on_bad_sigmoid_fails():
    cpp_runner = CppTestRunner()
    sigmoid = """double sigmoid ( double input ){
    return 0.5;
    }"""
    sigmoid = " ".join(cpp_processor.tokenize_code(sigmoid))
    res, tests, failures = cpp_runner.get_tests_results(sigmoid, TEST_SIGMOID)
    assert res == "failure", (res, tests, failures)
    assert tests == 2
    assert failures == 1


def test_runner_on_bad_sigmoid_compilation_error():
    cpp_runner = CppTestRunner()
    sigmoid = """double sigmoid ( double input ){
        return 1.0 / ( 1.0 + ( exp ( - input ) ) )
    }"""
    sigmoid = " ".join(cpp_processor.tokenize_code(sigmoid))
    res, tests, failures = cpp_runner.get_tests_results(sigmoid, TEST_SIGMOID)
    assert res == "compilation", (res, tests, failures)
    assert tests == 0
    assert isinstance(failures, str)


def test_runner_on_sigmoid_np_timeout():
    cpp_runner = CppTestRunner(timeout=1)
    sigmoid = """double sigmoid ( double input ){
    sleep(10);
    return 1;
    }
"""
    sigmoid = " ".join(cpp_processor.tokenize_code(sigmoid))
    res, tests, failures = cpp_runner.get_tests_results(sigmoid, TEST_SIGMOID)
    assert res == "timeout", (res, tests, failures)
    assert tests == 0
    assert isinstance(failures, str)


def test_firejail_keeps_from_writing():
    if os.environ.get("CI", False):
        return
    cpp_runner = CppTestRunner(timeout=20)
    test_out_path = Path(__file__).parent.joinpath(
        "test_output_should_not_be_written_cpp.out"
    )
    if test_out_path.exists():
        os.remove(test_out_path)
    sigmoid = f"""double write_in_file ( double input ){{
        ofstream myfile;
        myfile.open ("{test_out_path}");
        myfile << "hello" << endl;
        return 1;
    }}
"""
    sigmoid = " ".join(cpp_processor.tokenize_code(sigmoid))
    res, tests, failures = cpp_runner.get_tests_results(sigmoid, TEST_SIGMOID)
    assert not test_out_path.is_file(), f"{test_out_path} should not have been written"
    assert res == "failure", (res, tests, failures)
    assert tests == 2
    assert failures == 2


TEST_LATTITUDE = """#include <iostream>
#include <cstdlib>
#include <string>
#include <vector>
#include <fstream>
#include <iomanip>
#include <bits/stdc++.h>
#include "gtest/gtest.h"

using namespace std;



//TOFILL





  TEST(EvoSuiteTest, test0){
      double double0 = f_filled(0.5);
      ASSERT_NEAR (0.0, double0, 1.0E-4);
  }

  TEST(EvoSuiteTest, test1){
      double double0 = f_filled(0.0);
      ASSERT_NEAR (85.0511287798066, double0, 1.0E-4);
  }

  TEST(EvoSuiteTest, test2){
      double double0 = f_filled(21003.854);
      ASSERT_NEAR ((-90.0), double0, 1.0E-4);
  }



int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}"""


def test_runner_on_lattitude_success():
    cpp_runner = CppTestRunner()
    lattitude = "double getLatitudeFromY ( double inY ) { double n = M_PI * ( 1 - 2 * inY ) ; return 180 / M_PI * atan ( 0.5 * ( exp ( n ) - exp ( - n ) ) ) ; }"
    lattitude = " ".join(cpp_processor.tokenize_code(lattitude))
    res, tests, failures = cpp_runner.get_tests_results(lattitude, TEST_LATTITUDE)
    assert res == "success", (res, tests, failures)
    assert tests == 3
    assert failures == 0
