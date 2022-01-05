# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import argparse
from itertools import repeat
from logging import getLogger
from pathlib import Path

import pandas as pd
from submitit import AutoExecutor, LocalExecutor
from tqdm import tqdm
from utils import chunks_df, add_root_to_path

add_root_to_path()
from codegen_sources.model.src.utils import set_MKL_env_vars
from codegen_sources.model.translate import Translator
from codegen_sources.preprocessing.utils import bool_flag
from codegen_sources.test_generation.compute_test_results import compute_test_results

CHUNKSIZE = 2500
SUPPORTED_LANGUAGES = ["python", "cpp"]
primitive_types = {"short", "int", "long", "float", "double", "boolean", "char"}
logger = getLogger()

java_standard_types = {
    "Double",
    "Float",
    "String",
    "Integer",
    "Boolean",
    "Long",
    "Short",
}
java_simple_types = primitive_types | java_standard_types
java_supported_types = (
    java_simple_types
    | {f"{t}[]" for t in java_simple_types}
    | {f"ArrayList<{t}>" for t in java_simple_types}
)


def get_joined_func_tests_df(csv_path, functions_path):
    assert Path(csv_path).is_file(), csv_path
    tests_dataframe = pd.read_csv(csv_path)
    java_functions_path = Path(functions_path)

    # reading functions to DF
    java_functions = [
        func
        for f in java_functions_path.glob("java.0000*.sa.tok")
        for func in open(f).readlines()
    ]
    java_functions = pd.DataFrame(
        {
            "func_ids": [f.split(" | ")[0] for f in java_functions],
            "java_function": [f.split(" | ")[1] for f in java_functions],
        }
    )

    # getting the IDs of the functions. The class name is created from it
    tests_dataframe["func_ids"] = tests_dataframe.TARGET_CLASS.apply(
        lambda x: x.replace("CLASS_", "", 1)
    )
    merged = tests_dataframe.merge(java_functions, how="inner", on="func_ids")
    return merged


def compute_transcoder_translation(
    df,
    output_file,
    model_path,
    bpe_path,
    target_language,
    len_penalty=1.0,
    beam_size=20,
):
    transcoder = Translator(model_path, bpe_path)
    res = [[] for _ in range(beam_size)]
    for i, func in enumerate(df["java_function"]):
        if i % 100 == 0:
            logger.info(f"computed {i} translations / {len(df)}")
        translations = transcoder.translate(
            func,
            "java",
            target_language,
            beam_size=beam_size,
            tokenized=True,
            detokenize=False,
            max_tokens=1024,
            length_penalty=len_penalty,
        )
        for i, res_i in enumerate(translations):
            res[i].append(res_i)

    for i, res_i in enumerate(res):
        df[f"translated_{target_language}_functions_beam_{i}"] = res_i
    df.to_csv(output_file, index=False)


def main(args):
    output_folder = Path(args.output_folder)
    output_folder.mkdir(exist_ok=True, parents=True)
    transcoder_output_folder = "transcoder_outputs"
    output_folder_translations = output_folder.joinpath(transcoder_output_folder)
    if args.local is False:
        logger.info("Executing on cluster")
        cluster = AutoExecutor(output_folder_translations.joinpath("log"))
        cluster.update_parameters(
            cpus_per_task=10,
            gpus_per_node=1,
            mem_gb=300,
            timeout_min=4319,
            constraint="volta32gb",
            partition="learnlab",
        )
    else:
        logger.info("Executing locally")
        cluster = None
    merged_df = get_joined_func_tests_df(args.csv_path, args.functions_path)
    chunks = list(chunks_df(merged_df, CHUNKSIZE))
    output_files = [
        output_folder_translations.joinpath(f"{args.target_language}_chunk_{i}.csv")
        for i in range(len(chunks))
    ]
    assert (
        len(chunks) > 0
    ), f"No chunks created from {args.csv_path } and {args.functions_path}"
    logger.info(f"{len(chunks)} chunks of size {CHUNKSIZE}")
    missing_output_files = output_files
    if not args.rerun:
        indices_to_run = [i for i, p in enumerate(output_files) if not (p.is_file())]
        # indices_to_run = [8]
        logger.info(
            f"Running on the remaining {len(indices_to_run)} among {len(output_files)} files"
        )
        chunks = [chunks[i] for i in indices_to_run]
        missing_output_files = [output_files[i] for i in indices_to_run]
    assert len(chunks) == len(missing_output_files)
    if len(chunks) > 0:
        if cluster is None:
            for c, output_f in zip(chunks, missing_output_files):
                compute_transcoder_translation(
                    c,
                    output_f,
                    args.model_path,
                    args.bpe_path,
                    args.target_language,
                    args.len_penalty,
                )
        else:
            jobs = cluster.map_array(
                compute_transcoder_translation,
                chunks,
                missing_output_files,
                repeat(args.model_path),
                repeat(args.bpe_path),
                repeat(args.target_language),
                repeat(args.len_penalty),
            )
            for j in tqdm(jobs):
                j.result()
    chunks_files = [
        output_folder_translations.joinpath(f"{args.target_language}_chunk_{i}.csv")
        for i in range(len(output_files))
    ]
    output_csv_path = output_folder_translations.joinpath(
        f"{args.target_language}_transcoder_translation.csv"
    )
    pd.concat([pd.read_csv(chunk) for chunk in chunks_files], axis=0).to_csv(
        output_csv_path, index=False
    )

    compute_test_results(
        output_csv_path,
        args.target_language,
        output_folder.joinpath("test_results"),
        local=args.local,
    )


def parse_arguments():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--functions_path", help="path to the input files",
    )
    parser.add_argument(
        "--csv_path", help="path to the input test csv",
    )
    parser.add_argument(
        "--output_folder", help="output path",
    )
    parser.add_argument(
        "--target_language", help="target language. python or cpp", default="python",
    )
    parser.add_argument(
        "--model_path", type=str, help="where the files should be outputed",
    )
    parser.add_argument(
        "--bpe_path", type=str, help="where the files should be outputted",
    )
    parser.add_argument(
        "--len_penalty", type=float, help="Length penalty for generations", default=0.5,
    )
    parser.add_argument(
        "--local",
        type=bool_flag,
        default=True,
        help="True if you want to run the processing pipeline locally, false if want to use submitit.",
    )
    parser.add_argument(
        "--rerun",
        type=bool_flag,
        default=False,
        help="True if you want to run the processing pipeline locally, false if want to use submitit.",
    )
    # parser.add_argument('--filter_several_tests', type=bool_flag, default=True, help='Filter to keep only the examples with at least 2 tests')
    args = parser.parse_args()
    assert Path(args.bpe_path).is_file(), args.bpe_path
    assert Path(args.model_path).is_file()
    assert args.target_language in SUPPORTED_LANGUAGES
    return args


if __name__ == "__main__":
    logger.info("#" * 10 + "Computing Translations" + "#" * 10)
    set_MKL_env_vars()
    args = parse_arguments()
    main(args)
    logger.info("\n" * 2)
