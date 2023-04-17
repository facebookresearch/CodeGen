# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import pytest
import codegen_sources.preprocessing.lang_processors as lp
from codegen_sources.preprocessing.obfuscation import utils_deobfuscation
from codegen_sources.preprocessing.tests.obfuscation.utils import diff_tester


processors = (lp.PythonProcessor(), lp.PythonTreeSitterProcessor())
with_both_processors = pytest.mark.parametrize("processor", processors)

# # # # # Type obfuscation


def test_type_obfuscation() -> None:
    processor = processors[1]
    input_program = """from pathlib import Path
import typing as tp

global_var: tp.List[str] = []

class Something:
    '''accentué'''
    class_var: int = 12
    def __init__(self, something: tp.Union[str,
                                           Path]) -> None:
        self.uninitialized_var: int
        self.var: dict = {}
        self.var[0] = 12

   async def func(self, input_: str = None) -> tp.List[str]:
       self.uninitialized_var = 2
       self.func(None)
       return ["aaa"]

    @classmethod
    def myself(cls, other) -> "Something":
        return self

    def fail(cls, other: tp.Optional[str] = None, stuff: str| None = None):
        return self
"""
    res, dico = processor.obfuscate_types(input_program)
    expected = """from pathlib import Path


global_var: VAR_0 = []

class Something:
    '''accentué'''
    class_var: VAR_1 = 12
    def __init__(self, something: VAR_2) -> None:
        self.uninitialized_var: VAR_3
        self.var: VAR_4 = {}
        self.var[0] = 12

   async def func(self, input_: VAR_5 = None) -> VAR_6:
       self.uninitialized_var = 2
       self.func(None)
       return ["aaa"]

    @classmethod
    def myself(cls, other) -> VAR_7:
        return self

    def fail(cls, other: VAR_8 = None, stuff: VAR_9 = None):
        return self
"""
    diff_tester(expected.strip(), res.strip())
    expected_types = [
        "List [ str ]",
        "int",
        "Union [ Path , str ]",
        "int",
        "Dict [ str , Any ]",
        "Optional [ str ]",
        "List [ str ]",
        "Something",
        "Optional [ str ]",
        "Optional [ str ]",
    ]
    expected_dict = " | ".join(f"VAR_{k} {x}" for k, x in enumerate(expected_types))
    diff_tester(
        expected_dict, dico, split=" | ",
    )
    as_dict = utils_deobfuscation.read_dict(expected_dict)
    assert as_dict["VAR_2"] == "Union [ Path , str ]"


# # # # # Name obfuscation


@with_both_processors
def test_obfuscation_var_definition(processor: lp.LangProcessor) -> None:
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


@with_both_processors
def test_obfuscation_recursive_method(processor: lp.LangProcessor) -> None:
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


@with_both_processors
def test_obfuscation_class_attributes(processor: lp.LangProcessor) -> None:
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


@with_both_processors
def test_obfuscation_imported_var(processor: lp.LangProcessor) -> None:
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


@with_both_processors
def test_function_scope(processor: lp.LangProcessor) -> None:
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
