# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from codegen_sources.preprocessing.tests.obfuscation.utils import diff_tester
from codegen_sources.preprocessing.lang_processors.python_processor import (
    PythonProcessor,
)

processor = PythonProcessor()


def test_obfuscation_var_definition():
    input_program = """import os
class Factorial:
    def factorial(self, n, path):
        res, res2, res3 = 1, 1, 1
        for i in range(n):
            res *= (i + 1)
        with open(os.path.join(path, 'res'), 'w') as f:
            f.write(str(res))
        return res
        """
    res, dico = processor.obfuscate_code(input_program)
    expected = """
import os

class CLASS_0():

    def FUNC_0(VAR_0, VAR_1, VAR_2):
        (VAR_3, VAR_4, VAR_5) = (1, 1, 1)
        for VAR_6 in range(VAR_1):
            VAR_3 *= (VAR_6 + 1)
        with open(os.path.join(VAR_2, 'res'), 'w') as VAR_7:
            VAR_7.write(str(VAR_3))
        return VAR_3
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Factorial | FUNC_0 factorial | VAR_0 self | VAR_1 n | VAR_2 path | VAR_3 res | VAR_4 res2 | VAR_5 res3 | VAR_6 i | VAR_7 f",
        dico,
        split=" | ",
    )


def test_obfuscation_recursive_method():
    input_program = """class Factorial:
    def factorial(self, n):
        if n == 1:
            return 1
        return n * self.factorial(n-1)
"""
    res, dico = processor.obfuscate_code(input_program)
    expected = """class CLASS_0():

    def FUNC_0(VAR_0, VAR_1):
        if (VAR_1 == 1):
            return 1
        return (VAR_1 * VAR_0.FUNC_0((VAR_1 - 1)))
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Factorial | FUNC_0 factorial | VAR_0 self | VAR_1 n", dico, split=" | "
    )


def test_obfuscation_class_attributes():
    input_program = """class Factorial:
        def __init__(self, number):
            self.n = number

        def factorial(self):
            if self.n == 1:
                return 1
            return self.n * self.factorial(self.n-1)
    """
    res, dico = processor.obfuscate_code(input_program)
    expected = """class CLASS_0():

    def __init__(VAR_0, VAR_1):
        VAR_0.VAR_2 = VAR_1

    def FUNC_0(VAR_3):
        if (VAR_3.VAR_2 == 1):
            return 1
        return (VAR_3.VAR_2 * VAR_3.FUNC_0((VAR_3.VAR_2 - 1)))
    """
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Factorial | FUNC_0 factorial | VAR_0 self | VAR_1 number | VAR_2 n | VAR_3 self",
        dico,
        split=" | ",
    )


def test_obfuscation_imported_var():
    input_program = """from something import stuff
def factorial(n):
    if n == 1:
        return stuff
    return n * factorial(n-1)
    """
    res, dico = processor.obfuscate_code(input_program)
    expected = """from something import stuff

def FUNC_0(VAR_0):
    if (VAR_0 == 1):
        return stuff
    return (VAR_0 * FUNC_0((VAR_0 - 1)))
    """
    diff_tester(expected.strip(), res.strip())
    diff_tester("FUNC_0 factorial | VAR_0 n", dico, split=" | ")


def test_function_scope():
    input_program = """
def factorial(n):
    if n == 1:
        return n
    return n * factorial(n-1)

def sum(n):
    if n == 1:
        return n
    return n + sum(n-1)
    """
    res, dico = processor.obfuscate_code(input_program)
    expected = """
def FUNC_0(VAR_0):
    if (VAR_0 == 1):
        return VAR_0
    return (VAR_0 * FUNC_0((VAR_0 - 1)))

def FUNC_1(VAR_1):
    if (VAR_1 == 1):
        return VAR_1
    return (VAR_1 + FUNC_1((VAR_1 - 1)))
    """
    diff_tester(expected.strip(), res.strip())
    diff_tester("FUNC_0 factorial | FUNC_1 sum | VAR_0 n | VAR_1 n", dico, split=" | ")
