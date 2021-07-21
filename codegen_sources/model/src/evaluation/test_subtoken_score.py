# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

from .subtoken_score import (
    subtoken_counts,
    subtoken_score_on_lines,
    subtoken_score_on_lines_subtoken_level,
)


def test_same_strings_perfect_match():
    precise_tokens, proposed_tokens, gt_tokens = subtoken_counts(
        "linesCount", "linesCount"
    )
    assert precise_tokens == proposed_tokens == gt_tokens == 2


def test_inverted_tokens_perfect_match():
    precise_tokens, proposed_tokens, gt_tokens = subtoken_counts(
        "countLines", "linesCount"
    )
    assert precise_tokens == proposed_tokens == gt_tokens == 2


def test_different_cases_perfect_match():
    precise_tokens, proposed_tokens, gt_tokens = subtoken_counts(
        "lines_count", "linesCount"
    )
    assert precise_tokens == proposed_tokens == gt_tokens == 2


def test_extra_token_perfect_recall():
    precise_tokens, proposed_tokens, gt_tokens = subtoken_counts(
        "emptyLinesCount", "linesCount"
    )
    assert precise_tokens == gt_tokens == 2
    assert proposed_tokens == 3


def test_missing_token_perfect_precision():
    precise_tokens, proposed_tokens, gt_tokens = subtoken_counts("count", "linesCount")
    assert precise_tokens == proposed_tokens == 1
    assert gt_tokens == 2


def test_empty_proposed_low_recall():
    precise_tokens, proposed_tokens, gt_tokens = subtoken_counts("", "linesCount")
    assert precise_tokens == proposed_tokens == 0
    assert gt_tokens == 2


def test_full_subtoken_score():
    res_dict = subtoken_score_on_lines(
        [["VAR_1 linesCount | VAR_2 words"]], ["VAR_1 countLines | VAR_2 uniqueWords"]
    )

    assert res_dict["precision"] == 1.0, res_dict
    assert abs(res_dict["recall"] - 0.75) < 0.0001, res_dict
    assert abs(res_dict["F1"] - 0.83333333) < 0.0001, res_dict


def test_extra_tokens():
    res_dict = subtoken_score_on_lines(
        [["VAR_1 linesCount | VAR_2 words | VA RandomStuff"]],
        ["VAR_1 countLines | VAR_2 uniqueWords"],
    )

    assert res_dict["precision"] == 1.0, res_dict
    assert abs(res_dict["recall"] - 0.75) < 0.0001, res_dict
    assert abs(res_dict["F1"] - 0.83333333) < 0.0001, res_dict


def test_full_subtoken_score_subtoken_level():
    res_dict = subtoken_score_on_lines_subtoken_level(
        ["VAR_1 linesCount | VAR_2 words"], ["VAR_1 countLines | VAR_2 uniqueWords"]
    )

    assert res_dict["precision"] == 1.0, res_dict
    assert abs(res_dict["recall"] - 0.75) < 0.0001, res_dict
    assert abs(res_dict["F1"] - 0.85714285) < 0.0001, res_dict


def test_full_subtoken_score_low_precision():
    res_dict = subtoken_score_on_lines(
        [["VAR_1 linesCount | VAR_2 sentences"]],
        ["VAR_1 countLines | VAR_2 uniqueWords"],
    )

    assert (
        res_dict["precision"] == res_dict["recall"] == res_dict["F1"] == 0.5
    ), res_dict
    assert res_dict["exact_match"] == 0, res_dict


def test_full_subtoken_score_snakecase_vs_camlcase():
    res_dict = subtoken_score_on_lines(
        [["VAR_1 lines_count | VAR_2 sentences"]],
        ["VAR_1 countLines | VAR_2 uniqueWords"],
    )

    assert (
        res_dict["precision"] == res_dict["recall"] == res_dict["F1"] == 0.5
    ), res_dict
    assert res_dict["exact_match"] == 0, res_dict


def test_full_subtoken_score_case_insensitive():
    res_dict = subtoken_score_on_lines([["VAR_1 Lines_count"]], ["VAR_1 CountLines"])

    assert (
        res_dict["precision"] == res_dict["recall"] == res_dict["F1"] == 1.0
    ), res_dict


def test_full_subtoken_score_takes_best_beam():
    res_dict = subtoken_score_on_lines(
        [["VAR_1 linesCount | VAR_2 sentences", "VAR_1 linesCount | VAR_2 words"]],
        ["VAR_1 countLines | VAR_2 uniqueWords"],
    )

    assert res_dict["precision"] == 1.0, res_dict
    assert abs(res_dict["recall"] - 0.75) < 0.0001, res_dict
    assert abs(res_dict["F1"] - 0.83333333) < 0.0001, res_dict
