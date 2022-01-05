# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import argparse
import pickle
from concurrent.futures.process import ProcessPoolExecutor
from itertools import repeat
from pathlib import Path

import numpy as np
import pandas as pd
from submitit import AutoExecutor, LocalExecutor
from tqdm import tqdm

import sys


root_path = Path(__file__).absolute().parents[2]
print(f"adding {root_path} to path")
sys.path.append(str(root_path))

from codegen_sources.model.src.logger import create_logger
from codegen_sources.preprocessing.utils import bool_flag
from codegen_sources.test_generation.evosuite_tests_translators.evosuite_to_cpp import (
    EvosuiteToCpp,
)
from codegen_sources.test_generation.evosuite_tests_translators.evosuite_to_python import (
    EvosuiteToPython,
)
from codegen_sources.test_generation.test_runners.cpp_test_runner import CppTestRunner
from codegen_sources.test_generation.test_runners.python_test_runner import (
    PythonTestRunner,
)
from codegen_sources.test_generation.utils import (
    chunks,
    compute_results_one_test,
    get_beam_size,
)

logger = create_logger(None, 0)
CHUNKSIZE_TEST_RESULTS = 2000


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


def compute_all_tests_results(tests, functions, test_runner, output_path=None):
    executor = ProcessPoolExecutor()
    assert len(tests) == len(
        functions
    ), f"tests of length {len(tests)} while functions are of length {len(functions)}"
    jobs = [
        executor.submit(compute_results_one_test, t, fs, test_runner, 150)
        for t, fs in zip(tests, functions)
    ]
    res = []
    for i, job in enumerate(jobs):
        res.append(job.result())
        if i % 100 == 0:
            logger.info(f"computed results for {i} tests over {len(tests)}")
            logger.info(f"Successes: {sum([r[0][0] == 'success' for r in res])}")
            logger.info(f"timeouts: {sum([r[0][0] == 'timeout' for r in res])}")
        # print(res[-1])
    if output_path is not None:
        with open(output_path, "wb") as f:
            pickle.dump(res, f)
    return res


def translate_tests(java_tests, translator):
    executor = ProcessPoolExecutor()
    return list(executor.map(safe_translate_test, repeat(translator), java_tests))


def safe_translate_test(test_translator, code):
    try:
        return test_translator.translate(code)
    except AssertionError as e:
        return f"AssertionError : {e}"
    except TypeError as e:
        return f"TypeError : {e}"


def compute_test_results(
    translations_csv_path, target_language, output_folder, local, rerun=False
):
    logger.info("#" * 10 + "Computing Test Results" + "#" * 10)
    output_folder.mkdir(exist_ok=True, parents=True)
    logger.info(
        f"Computing test results for language {target_language} in {translations_csv_path}\n Results will be outputed in {output_folder}"
    )
    input_df = pd.read_csv(translations_csv_path)
    if target_language == "python":
        test_runner = PythonTestRunner()
        test_translator = EvosuiteToPython()
    else:
        assert target_language == "cpp"
        test_runner = CppTestRunner(compilation_timeout=30)
        test_translator = EvosuiteToCpp()
    translated_func_col = f"translated_{target_language}_functions_beam_"
    beam_size = get_beam_size(input_df, translated_func_col)
    translated_functions = np.array(
        [input_df[f"{translated_func_col}{i}"].values for i in range(beam_size)]
    ).transpose()
    assert len(translated_functions) == len(
        input_df
    ), f"{translated_functions.shape} / {len(input_df)}"
    assert translated_functions.shape[1] == beam_size
    logger.info(
        f"computing output for {len(translated_functions)} tests and {beam_size} functions per test"
    )

    logger.info(f"Translating Tests")
    translated_tests = translate_tests(input_df.tests_strings.values, test_translator)
    assert len(translated_tests) == len(input_df)
    input_df[f"{target_language}_translated_tests"] = translated_tests
    logger.info(
        f"Finished translating {len(translated_tests)} tests to {target_language}"
    )

    if local is False:
        cluster = AutoExecutor(output_folder.joinpath("log"))
        cluster.update_parameters(
            cpus_per_task=40, mem_gb=300, partition="learnlab",
        )
        cluster.update_parameters(timeout_min=500)
    else:
        cluster = None
    tests_chunks = list(chunks(translated_tests, CHUNKSIZE_TEST_RESULTS))
    func_chuncs = list(chunks(translated_functions, CHUNKSIZE_TEST_RESULTS))
    logger.info(f"{len(tests_chunks)} chunks of size {len(tests_chunks[0])}")
    assert len(tests_chunks) == len(func_chuncs)
    chunk_output_paths = [
        output_folder.joinpath(f"{target_language}_chunk_{i}.pkl")
        for i in range(len(tests_chunks))
    ]
    missing_output_files = chunk_output_paths
    if not rerun:
        indices_to_run = [
            i for i, p in enumerate(chunk_output_paths) if not (p.is_file())
        ]
        logger.info(
            f"Running on the remaining {len(indices_to_run)} among {len(chunk_output_paths)} files"
        )
        tests_chunks = [tests_chunks[i] for i in indices_to_run]
        func_chuncs = [func_chuncs[i] for i in indices_to_run]
        missing_output_files = [chunk_output_paths[i] for i in indices_to_run]

    if cluster is None:
        for tc, fc, output in zip(tests_chunks, func_chuncs, missing_output_files):
            compute_all_tests_results(tc, fc, test_runner, output)
    else:
        jobs = cluster.map_array(
            compute_all_tests_results,
            tests_chunks,
            func_chuncs,
            repeat(test_runner),
            missing_output_files,
        )
        for j in tqdm(jobs):
            _ = j.result()

    results = []
    for p in chunk_output_paths:
        with open(p, "rb") as pickle_file:
            results.append(pickle.load(pickle_file))
    results = [code for r in results for code in r]

    for i in range(beam_size):
        input_df[f"test_results_{target_language}_{i}"] = [res[i] for res in results]
    outpath = output_folder.joinpath(f"test_results_{target_language}_df.csv")
    logger.info(f"Writing results in {outpath}")
    input_df.to_csv(outpath, index=False)
    logger.info("\n" * 2)


def parse_arguments():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--translations_csv_path", help="path to the input files",
    )
    parser.add_argument(
        "--output_path", type=str, help="where the files should be outputed",
    )
    parser.add_argument(
        "--local",
        type=bool_flag,
        default=True,
        help="True if you want to run the processing pipeline locally, false if want to use submitit.",
    )
    parser.add_argument(
        "--target_language", help="target language. python or cpp", default="python",
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    compute_test_results(
        args.translations_csv_path,
        args.target_language,
        Path(args.output_path),
        args.local,
    )
