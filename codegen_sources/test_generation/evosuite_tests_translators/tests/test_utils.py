# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import difflib
import subprocess
from pathlib import Path

import uuid

import os

folder_path = Path(__file__).parent
JAVA_PATH = folder_path.joinpath("resources/java_evosuite_tests")
PYTHON_PATH = folder_path.joinpath("resources/expected_python_translations")
CPP_PATH = folder_path.joinpath("resources/expected_cpp_translations")


def translation_testing(examples_list, translator, should_apply_black=False):
    for input_test, expected_translation in examples_list:
        actual = translator.translate(input_test)
        if should_apply_black:
            actual = apply_black(actual)
        diff_tester(expected_translation, actual)


def apply_black(code: str):
    filepath = f"/tmp/python_code_{uuid.uuid4()}.py"
    with open(filepath, "w") as tmp_file:
        tmp_file.write(code)
    subprocess.run(
        f"black {filepath}", shell=True,
    )
    with open(filepath, "r") as tmp_file_in:
        output = tmp_file_in.read()
    os.remove(filepath)
    return output


def diff_tester(expected, res, split="\n"):
    expected = split.join([x.rstrip() for x in expected.split(split)])
    res = split.join([x.rstrip() for x in res.split(split)])
    d = difflib.Differ()
    if expected != res:
        print("Expected:")
        print(expected)
        print("#" * 50)
        print("Got:")
        print(res)
        print("#" * 50)
        diff = d.compare(expected.split(split), res.split(split))
        for line in diff:
            print(line)
        assert expected == res


def read_inputs(filename, target_lang):
    java_path = JAVA_PATH.joinpath(filename).with_suffix(".java").absolute()
    with open(java_path, "r") as java_file:
        input_test = java_file.read()
    if target_lang == "python":
        with open(
            PYTHON_PATH.joinpath(filename).with_suffix(".py"), "r"
        ) as python_file:
            expected_translation = python_file.read()
    elif target_lang == "cpp":
        with open(CPP_PATH.joinpath(filename).with_suffix(".cpp"), "r") as python_file:
            expected_translation = python_file.read()
    else:
        raise ValueError(f"target_lang {target_lang} not supported")
    return input_test, expected_translation
