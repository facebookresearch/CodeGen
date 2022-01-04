# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
# Translate sentences from the input stream.
# The model will be faster is sentences are sorted by length.
# Input sentences must have the same tokenization and BPE codes than the ones used in the model.
#

import argparse
from logging import getLogger
from pathlib import Path

import fastBPE
import numpy as np
import pandas as pd

from utils import get_beam_size, add_root_to_path

add_root_to_path()
from codegen_sources.model.preprocess import XLM_preprocess

SOURCE_LANG = "java"

FAILURE = "failure"

logger = getLogger()


def get_arguments():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--input_df", help="path to the input files",
    )
    parser.add_argument(
        "--output_folder", type=str, help="where the files should be outputed",
    )
    parser.add_argument(
        "--langs",
        type=list,
        nargs="+",
        help="List of target langs",
        default=["python", "cpp"],
    )
    parser.add_argument(
        "--bpe_path", type=str, help="where the files should be outputed",
    )
    parser.add_argument(
        "--bpe_vocab", type=str, help="where the files should be outputed",
    )
    args = parser.parse_args()
    return args


def main(input_path, output_folder, langs, bpe_model, bpe_vocab):
    input_path = Path(input_path)
    input_dfs_paths = {
        lang: input_path.joinpath(f"test_results_{lang}_df.csv") for lang in langs
    }
    test_results_dfs = {
        lang: pd.read_csv(path) for lang, path in input_dfs_paths.items()
    }
    test_results_dfs = select_tests_several_asserts(test_results_dfs)
    for ref_l in langs[1:]:
        assert len(test_results_dfs[ref_l]) == len(
            test_results_dfs[langs[0]]
        ), f"length of input {len(test_results_dfs[ref_l])} for {ref_l} while it is {len(test_results_dfs[langs[0]])} for {langs[0]}"
        assert (
            test_results_dfs[ref_l][f"{SOURCE_LANG}_function"]
            == test_results_dfs[langs[0]][f"{SOURCE_LANG}_function"]
        ).all(), f"Dataframes order for {ref_l} and {langs[0]} do not match"

    langs = sorted(langs)
    assert len(langs) == len(set(langs)), langs

    output_folder = Path(output_folder)
    output_folder.mkdir(exist_ok=True, parents=True)

    number_examples = len(test_results_dfs[langs[0]])
    for ref_l in langs[1:]:
        assert number_examples == len(
            test_results_dfs[langs[0]]
        ), f"length of input {number_examples} for {ref_l} while it is {len(test_results_dfs[langs[0]])} for {langs[0]}"
        assert (
            test_results_dfs[ref_l][f"{SOURCE_LANG}_function"]
            == test_results_dfs[langs[0]][f"{SOURCE_LANG}_function"]
        ).all(), f"Dataframes order for {ref_l} and {langs[0]} do not match"

    langs = sorted(langs)
    assert len(langs) == len(set(langs)), langs

    output_folder = Path(output_folder)
    output_folder.mkdir(exist_ok=True, parents=True)

    first_successful_code = {
        lang: get_first_success(test_results_dfs[lang], lang) for lang in langs
    }

    for lang in langs:
        successful_translations_df = test_results_dfs[lang][
            pd.Series(first_successful_code[lang]).apply(lambda x: x != FAILURE)
        ]
        successful_translations_df["first_successful_translation"] = [
            c for c in first_successful_code[lang] if c != FAILURE
        ]
        logger.info(
            f"{SOURCE_LANG}-{lang}: {len(successful_translations_df)} among {number_examples} ({len(successful_translations_df) / number_examples:.1%})"
        )
        print(
            f"{SOURCE_LANG}-{lang}: {len(successful_translations_df)} among {number_examples} ({len(successful_translations_df) / number_examples:.1%})"
        )
        write_bpe_files(
            output_folder,
            successful_translations_df["java_function"],
            successful_translations_df["first_successful_translation"],
            SOURCE_LANG,
            lang,
            bpe_model=bpe_model,
        )

    for lang1 in langs:
        for lang2 in langs[langs.index(lang1) + 1 :]:
            # the only parallel data we have is when the tests are successful for both languages
            successful_pairs = [
                (c1, c2)
                for c1, c2 in zip(
                    first_successful_code[lang1], first_successful_code[lang2]
                )
                if c1 != FAILURE and c2 != FAILURE
            ]
            print(
                f"{lang1}-{lang2}: {len(successful_pairs)} among {number_examples} ({len(successful_pairs) / number_examples:.1%})"
            )
            write_bpe_files(
                output_folder,
                [c1 for c1, c2 in successful_pairs],
                [c2 for c1, c2 in successful_pairs],
                lang1,
                lang2,
                bpe_model=bpe_model,
            )
    for file_path in Path(output_folder).glob("*.bpe"):
        XLM_preprocess(
            str(bpe_vocab), str(file_path), str(file_path).replace(".bpe", ".pth")
        )


def select_tests_several_asserts(test_results_dfs):
    tests_several_asserts = test_results_dfs["python"].python_translated_tests.apply(
        lambda x: x.count("assert ") > 1
    )

    test_results_dfs = {
        lang: df[tests_several_asserts].reset_index(drop=True)
        for lang, df in test_results_dfs.items()
    }
    new_length = len(test_results_dfs["python"])
    logger.info(
        f"removed {len(tests_several_asserts) - new_length} tests with only one assert ({1 - new_length / len(tests_several_asserts):.2%})"
    )
    return test_results_dfs


def get_first_success(test_results, language):
    beam_size = get_beam_size(
        test_results, results_columns=f"translated_{language}_functions_beam_"
    )
    test_results_columns = [f"test_results_{language}_{i}" for i in range(beam_size)]
    translations_columns = [
        f"translated_{language}_functions_beam_{beam}" for beam in range(beam_size)
    ]
    for col in test_results_columns:
        test_results[col] = test_results[col].apply(lambda x: eval(x))
    translations = np.array(
        [test_results[col] for col in translations_columns]
    ).transpose()
    logger.info("getting the first successful function")
    tests_results = np.array(
        [test_results[col] for col in test_results_columns]
    ).transpose((1, 0, 2))
    code = []
    min_successful_len = float("inf")
    for translations_i, result_i in zip(translations, tests_results):
        any_successful = False
        for translated_code, res in zip(translations_i, result_i):
            if res[0] == "success":
                if not any_successful:
                    code.append(translated_code)
                    min_successful_len = len(translated_code)
                    any_successful = True
                elif len(translated_code) < min_successful_len:
                    min_successful_len = len(translated_code)
                    code[-1] = translated_code
        if not any_successful:
            code.append(FAILURE)
    assert len(code) == len(test_results)
    first_successful_code = code
    return first_successful_code


def write_bpe_files(output_folder, lang1_funcs, lang2_funcs, lang1, lang2, bpe_model):
    if not lang1 < lang2:
        lang1, lang2 = lang2, lang1
        lang1_funcs, lang2_funcs = lang2_funcs, lang1_funcs
    lang1_funcs = bpe_model.apply([f.strip() for f in lang1_funcs])
    lang2_funcs = bpe_model.apply([f.strip() for f in lang2_funcs])
    output_files = {
        lang1: [
            open(
                output_folder.joinpath(
                    f"train.{lang1}_sa-{lang2}_sa.{lang1}_sa.{i}.bpe"
                ),
                "w",
            )
            for i in range(8)
        ],
        lang2: [
            open(
                output_folder.joinpath(
                    f"train.{lang1}_sa-{lang2}_sa.{lang2}_sa.{i}.bpe"
                ),
                "w",
            )
            for i in range(8)
        ],
    }
    output_files_all = {
        lang1: open(
            output_folder.joinpath(f"train.{lang1}_sa-{lang2}_sa.{lang1}_sa.bpe"), "w"
        ),
        lang2: open(
            output_folder.joinpath(f"train.{lang1}_sa-{lang2}_sa.{lang2}_sa.bpe"), "w"
        ),
    }
    for i, (c1, c2) in enumerate(zip(lang1_funcs, lang2_funcs)):
        c1 = c1.strip()
        c2 = c2.strip()
        output_files_all[lang1].write(c1)
        output_files_all[lang1].write("\n")

        output_files_all[lang2].write(c2)
        output_files_all[lang2].write("\n")

        output_files[lang1][i % 8].write(c1)
        output_files[lang1][i % 8].write("\n")

        output_files[lang2][i % 8].write(c2)
        output_files[lang2][i % 8].write("\n")

    for o in output_files[lang1] + output_files[lang2]:
        o.close()


if __name__ == "__main__":
    args = get_arguments()
    bpe_model = fastBPE.fastBPE(args.bpe_path)
    main(Path(args.input_df), args.output_folder, args.langs, bpe_model, args.bpe_vocab)
