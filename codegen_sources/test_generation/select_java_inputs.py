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
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from itertools import repeat
from pathlib import Path

import numpy as np
from submitit import AutoExecutor, LocalExecutor
from tqdm import tqdm

from utils import add_root_to_path

add_root_to_path()
from codegen_sources.model.src.utils import (
    get_java_compilation_errors,
    TREE_SITTER_ROOT,
)
from codegen_sources.preprocessing.lang_processors.java_processor import JavaProcessor
from codegen_sources.preprocessing.utils import bool_flag
from codegen_sources.test_generation.utils import chunks

CHUNKSIZE = 2500

primitive_types = {"short", "int", "long", "float", "double", "boolean", "char"}

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


def uses_ios(codestring):
    return (
        "java.io.File(" in codestring.replace(" ", "")
        or "io.FileWriter" in codestring.replace(" ", "")
        or "zip.ZipFile" in codestring.replace(" ", "")
        or "IOException" in codestring
    )


def extract_return_type_java(f):
    return f.split("(", 1)[0].split()[-2]


def is_simple_standalone_func(func):
    global java_processor
    try:
        args = java_processor.extract_arguments(func)
        return_type = extract_return_type_java(func)
        if all(
            [
                arg.replace("final ", "").replace(" ", "")
                in java_supported_types | {"None"}
                for arg in args[0]
            ]
        ) and return_type in java_supported_types | {"void"}:
            if (
                return_type == "void"
                and not any(
                    [
                        "[]" in arg.replace(" ", "") or "List" in arg or "Array" in arg
                        for arg in args[0]
                    ]
                )
                or java_processor.get_function_name(func).strip() == "main"
            ):
                return False
            if (
                get_java_compilation_errors(
                    java_processor.detokenize_code(func), timeout=120
                )
                == "success"
            ):
                return True
        return False
    except ValueError:
        return False
    except IndexError:
        return False


def select_functions(funcpath):
    executor = ThreadPoolExecutor()
    global java_processor
    java_processor = JavaProcessor(TREE_SITTER_ROOT)
    jobs = []
    with open(funcpath, "r") as f:
        functions = list(set([line.split(" | ", 1)[1] for line in f.readlines()]))
        for func in functions:
            jobs.append(executor.submit(is_simple_standalone_func, func))
    mask = [j.result() for j in jobs]
    return np.array(functions)[mask]


def select_functions_for_file(f_path, output_path):
    selected_functions = select_functions(f_path)
    out_filepath = output_path.joinpath(f_path.name)
    with open(out_filepath, "w") as out_f:
        print(f"Writing {len(selected_functions)} lines to {out_filepath}")
        out_f.writelines(selected_functions)


if __name__ == "__main__":
    print("#" * 10, "Selecting input functions", "#" * 10)
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--input_path", help="path to the input files",
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
        "--rerun",
        type=bool_flag,
        default=False,
        help="True if you want to run the processing pipeline locally, false if want to use submitit.",
    )
    args = parser.parse_args()
    input_path = Path(args.input_path)
    assert input_path.is_dir()
    output_path = Path(args.output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    if args.local is False:
        cluster = AutoExecutor(output_path.joinpath("log"))
        cluster.update_parameters(cpus_per_task=80, mem_gb=300)
        cluster.update_parameters(timeout_min=40)
    else:
        cluster = None
    tok_files_names = "java.[0-9]*.sa.tok"
    tok_files = sorted(list(input_path.glob(tok_files_names)))
    if not args.rerun:
        tok_files = [
            f_path
            for f_path in tok_files
            if not (output_path.joinpath(f_path.name).is_file())
        ]
    if cluster is None:
        for f in tqdm(tok_files):
            select_functions_for_file(f, output_path)
    else:
        jobs = cluster.map_array(
            select_functions_for_file, tok_files, repeat(output_path)
        )
        for j in tqdm(jobs):
            j.result()

    selected_files = sorted(list(output_path.glob(tok_files_names)))

    all_funcs = []
    for f_path in selected_files:
        with open(f_path) as f:
            all_funcs.extend(f.readlines())

    deduped_funcs = list(set(all_funcs))
    deduped_funcs = [f for f in deduped_funcs if not uses_ios(f)]
    deduped_funcs = [
        f'{sha256(f.encode("utf8")).hexdigest()} | {f}' for f in deduped_funcs
    ]

    deduped_funcs_chunks = list(chunks(deduped_funcs, CHUNKSIZE))

    deduped_output_path = output_path.joinpath("deduped")
    deduped_output_path.mkdir(exist_ok=True)
    for i, chunk in enumerate(deduped_funcs_chunks):
        out_file = deduped_output_path.joinpath(f"java.{i:012}.sa.tok")
        with open(out_file, "w", encoding="utf-8", errors="ignore") as out:
            for line in chunk:
                out.write(line.strip())
                out.write("\n")
    print("\n")
