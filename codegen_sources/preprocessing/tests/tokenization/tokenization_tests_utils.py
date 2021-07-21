# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import difflib


def tokenizer_test(test_examples, processor, keep_comments):
    for i, (x, y) in enumerate(test_examples):
        y_ = processor.tokenize_code(x, keep_comments=keep_comments)
        if y_ != y:
            line_diff = [
                j for j, (line, line_) in enumerate(zip(y, y_)) if line != line_
            ]
            line_diff = line_diff[-1] if len(line_diff) > 0 else -1
            raise Exception(
                f"Difference at {line_diff}\nExpected:\n==========\n{y}\nbut found:\n==========\n{y_}"
            )


def detokenize_invertible(test_examples, processor):
    for i, (x, _) in enumerate(test_examples):
        print(x)
        print(processor.tokenize_code(x, keep_comments=False))
        x_ = processor.detokenize_code(processor.tokenize_code(x, keep_comments=False))
        if x_.strip() != x.strip():
            raise Exception(
                f"Expected:\n==========\n{x.strip()}\nbut found:\n==========\n{x_.strip()}"
            )


def detokenize_non_invertible(test_examples, processor):
    for i, (x, y) in enumerate(test_examples):
        y_ = processor.detokenize_code(processor.tokenize_code(x, keep_comments=False))
        if y_ != y:
            lenght = min(len(y_), len(y))
            char_message = ""
            for j in range(lenght):
                if y_[j] != y[j]:
                    char_message = (
                        f"expected character '{y[j]}' at index {j} but found '{y_[j]}'"
                    )
            if char_message == "":
                char_message = f"expected length {len(y)}, found {len(y_)}"
            raise Exception(
                f"Expected:\n==========\n{y}\nbut found:\n==========\n{y_} \n==========\n{char_message}"
            )


def tokenize_twice(test_examples, processor, keep_comments=False):
    for i, (x, _) in enumerate(test_examples):
        tokenized_once = processor.tokenize_code(x, keep_comments=keep_comments)
        tokenized_twice = processor.tokenize_code(
            processor.detokenize_code(tokenized_once), keep_comments=keep_comments
        )
        if tokenized_once != tokenized_twice:
            lenght = min(len(tokenized_twice), len(tokenized_once))
            char_message = ""
            for j in range(lenght):
                if tokenized_twice[j] != tokenized_once[j]:
                    char_message = f"expected token '{tokenized_once[j]}' at index {j} but found '{tokenized_twice[j]}'"
            if char_message == "":
                char_message = f"expected length {len(tokenized_once)}, found {len(tokenized_twice)}"
            raise Exception(
                f"Expected:\n==========\n{tokenized_once}\nbut found:\n==========\n{tokenized_twice} \n==========\n{char_message}"
            )


def compare_funcs(actual, expected):
    d = difflib.Differ()
    if expected != actual:
        print("Expected:")
        print(expected)
        print("#" * 50)
        print("Got:")
        print(actual)
        print("#" * 50)
        diff = d.compare(expected, actual)
        for line in diff:
            print(line)
        raise Exception(
            f"Differences between\n========== Expected:\n{expected}\n========== \n and actual :\n{actual}"
        )
