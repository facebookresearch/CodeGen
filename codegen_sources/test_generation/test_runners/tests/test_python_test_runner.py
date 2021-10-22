# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from pathlib import Path

import os

from codegen_sources.test_generation.test_runners.python_test_runner import (
    PythonTestRunner,
)
from codegen_sources.model.src.utils import TREE_SITTER_ROOT
from codegen_sources.preprocessing.lang_processors.lang_processor import LangProcessor

python_processor = LangProcessor.processors["python"](root_folder=TREE_SITTER_ROOT)


TEST_SIGMOID = """import numpy as np
import math
from math import *
import collections
from collections import *
import heapq
import itertools
import random
import unittest



#TOFILL

class CLASS_f72b28220d38d38dc0dd570d2e44b3e4f4bc0dbe6db07624d40924a60e481f65(unittest.TestCase):

  def test0(self):
      double0 = f_filled(0.0)
      assert abs(0.5 -  double0) <=  1.0E-4


  def test1(self):
      double0 = f_filled((-49379.6829442))
      print(double0)
      assert abs(0.0 -  double0) <=  1.0E-4



if __name__ == '__main__':
    unittest.main()"""


def test_runner_on_sigmoid_math_fails():
    python_runner = PythonTestRunner()
    sigmoid = """def sigmoid ( input ) :
    return 1.0 / ( 1.0 + ( math.exp ( - input ) ) )"""
    sigmoid = " ".join(python_processor.tokenize_code(sigmoid))
    res, tests, failures = python_runner.get_tests_results(sigmoid, TEST_SIGMOID)
    assert res == "failure"
    assert tests == 2
    assert failures == 1


def test_runner_on_sigmoid_np_success():
    python_runner = PythonTestRunner()
    sigmoid = """def sigmoid ( input ) :
    return 1.0 / ( 1.0 + ( np.exp ( - input ) ) )"""
    sigmoid = " ".join(python_processor.tokenize_code(sigmoid))
    res, tests, failures = python_runner.get_tests_results(sigmoid, TEST_SIGMOID)
    assert res == "success"
    assert tests == 2
    assert failures == 0


def test_runner_on_sigmoid_np_timeout():
    python_runner = PythonTestRunner(timeout=1)
    sigmoid = """def sigmoid ( input ) :
    import time
    time.sleep(10)
"""
    sigmoid = " ".join(python_processor.tokenize_code(sigmoid))
    res, tests, failures = python_runner.get_tests_results(sigmoid, TEST_SIGMOID)
    assert res == "timeout"
    assert tests == 0
    assert failures == ""


def test_firejail_keeps_from_writing():
    if os.environ.get("CI", False):
        return

    python_runner = PythonTestRunner(timeout=20)
    test_out_path = Path(__file__).parent.joinpath(
        "test_output_should_not_be_written.out"
    )
    if test_out_path.exists():
        os.remove(test_out_path)

    sigmoid = f"""def write_in_file ( input ) :
    with open("{test_out_path}", "w") as out_file:
        out_file.write("hello")
"""
    sigmoid = " ".join(python_processor.tokenize_code(sigmoid))
    res, tests, failures = python_runner.get_tests_results(sigmoid, TEST_SIGMOID)
    assert not test_out_path.is_file(), f"{test_out_path} should not have been written"
    assert res == "failure"
    assert tests == 2
    assert failures == 2


def test_failures():
    python_runner = PythonTestRunner()
    test = """import numpy as np 
import math
from math import *
import collections
from collections import *
import heapq
import itertools
import random
import sys
import unittest



#TOFILL




class CLASS_1143a612514aceab440e7ae2afc4dcdddb4332091f8c971668711956db699122(unittest.TestCase):

  def test0(self):
      intArray0 = [0] * 8;
      int0 = f_filled(intArray0, 9185)
      assert (-1) ==  int0
  

  def test1(self):
      intArray0 = [0] * 8;
      intArray0[0] = 45539;
      int0 = f_filled(intArray0, 0)
      assert 1 ==  int0
  

  def test2(self):
      intArray0 = [0] * 1;
      intArray0[0] = 1;
      int0 = f_filled(intArray0, 1)
      assert 0 ==  int0
  


if __name__ == '__main__':
    unittest.main()"""
    function = "def findinlist ( list , value ) : NEW_LINE INDENT for i in range ( len ( list ) ) : NEW_LINE INDENT if list [ i ] == value : NEW_LINE INDENT return i NEW_LINE DEDENT DEDENT return None NEW_LINE DEDENT"
    res, tests, failures = python_runner.get_tests_results(function, test)
    assert res == "failure"
    assert tests == 3
    assert failures == 1
