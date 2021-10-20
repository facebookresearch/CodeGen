# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from codegen_sources.preprocessing.utils import split_arguments


def test_parentheses_split_args():
    input_str = "((1,2,3), (4,5), (1,2,3), new int[] {(-1), 0, 0}, intArray0)"
    res = split_arguments(input_str)
    expected = [
        "(1,2,3)",
        " (4,5)",
        " (1,2,3)",
        " new int[] {(-1), 0, 0}",
        " intArray0",
    ]
    assert res == expected, f"got \n{res} instead of \n{expected}"
    input_str = "(1,2,3), (4,5), (1,2,3), new int[] {(-1), 0, 0}, intArray0"

    res = split_arguments(input_str)
    assert res == expected, f"got \n{res} instead of \n{expected}"
    input_str = "(1,2,3), (4,5), (1,2,3)"
    res = split_arguments(input_str)
    expected = [
        "(1,2,3)",
        " (4,5)",
        " (1,2,3)",
    ]
    assert res == expected, f"got \n{res} instead of \n{expected}"
    input_str = "((1,2,3), (4,5), (1,2,3))"
    res = split_arguments(input_str)

    assert res == expected, f"got \n{res} instead of \n{expected}"


def test_strings_split_args():
    input_str = '("ni(TvJz:uAhKZ", "ABC")'
    res = split_arguments(input_str)
    expected = ['"ni(TvJz:uAhKZ"', ' "ABC"']
    assert res == expected, f"got \n{res} instead of \n{expected}"

    input_str = '("ni(TvJz:uAhKZ\\" ", "ABC")'
    res = split_arguments(input_str)
    expected = ['"ni(TvJz:uAhKZ\\" "', ' "ABC"']
    assert res == expected, f"got \n{res} instead of \n{expected}"


def test_strings_split_escaped_backslash():
    input_str = "'\\\\', char0"
    res = split_arguments(input_str)
    expected = ["'\\\\'", " char0"]
    assert res == expected, f"got \n{res} instead of \n{expected}"
