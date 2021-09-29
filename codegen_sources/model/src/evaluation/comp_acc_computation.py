# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import subprocess

import json
from concurrent.futures import ProcessPoolExecutor
import sys

import os

from ..utils import (
    REPO_ROOT,
    limit_virtual_memory,
    MAX_VIRTUAL_MEMORY,
    read_file_lines,
    get_java_bin_path,
)

sys.path.append(str(REPO_ROOT))
print("adding to path", str(REPO_ROOT))
TREE_SITTER_ROOT = REPO_ROOT.joinpath("tree-sitter")
import codegen_sources.preprocessing.lang_processors.cpp_processor
import codegen_sources.preprocessing.lang_processors.java_processor
import codegen_sources.preprocessing.lang_processors.python_processor
from codegen_sources.preprocessing.lang_processors.lang_processor import LangProcessor

from codegen_sources.test_generation.test_runners.cpp_test_runner import CppTestRunner
from codegen_sources.test_generation.test_runners.python_test_runner import (
    PythonTestRunner,
)
from codegen_sources.test_generation.evosuite_tests_translators.evosuite_to_python import (
    EvosuiteToPython,
)
from codegen_sources.test_generation.evosuite_tests_translators.evosuite_to_cpp import (
    EvosuiteToCpp,
)

EXT = {"python": "py", "java": "java", "cpp": "cpp"}

TOFILL = {"python": "#TOFILL", "java": "//TOFILL", "cpp": "//TOFILL"}

primitive_types = {"short", "int", "long", "float", "double", "boolean", "char"}

EVOSUITE_TESTS_TRANSCODER_PATH = (
    REPO_ROOT.joinpath("data")
    .joinpath("evosuite_unit_tests")
    .joinpath("transcoder_test_set.json")
)


def eval_state(proc, proc_name):
    try:
        try:
            result, stderr = proc.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            c = (
                "kill `ps aux | grep '"
                + proc_name
                + "' | grep -v jupyter | grep -v grep | awk '{print($2)}'`"
            )
            subprocess.run(
                c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            return "timeout", None
        results = result.decode("utf8", errors="replace")
        success, n_test = results.split("#Results:")[-1].split(",")
        if int(success) == int(n_test):
            return "success", None
        else:
            return "failure", result.decode("utf-8", errors="replace")
    except KeyboardInterrupt:
        raise
    except:
        return "error", stderr.decode("utf-8", errors="replace")


def run_python_program(script_path, i):
    proc = subprocess.Popen(
        f"{limit_virtual_memory(MAX_VIRTUAL_MEMORY)}; python {script_path}",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        executable="/bin/bash",
    )
    res = eval_state(proc, f"python {script_path}")
    return res, i


def run_java_program(script_path, i):
    folder = os.path.dirname(script_path)
    name = os.path.basename(script_path).split(".")[0]
    proc = subprocess.Popen(
        f"{limit_virtual_memory(MAX_VIRTUAL_MEMORY)}; cd {folder} &&  {os.path.join(get_java_bin_path(), 'javac')} {name}.java && {os.path.join(get_java_bin_path(), 'java')} {name}",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        executable="/bin/bash",
    )
    res = eval_state(proc, f"java {name}")
    return res, i


def run_cpp_program(script_path, i):
    folder = os.path.dirname(script_path)
    name = os.path.basename(script_path).split(".")[0]
    proc = subprocess.Popen(
        f"{limit_virtual_memory(MAX_VIRTUAL_MEMORY)}; cd {folder} && g++ {name}.cpp -o {name}_cpp && ./{name}_cpp",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        executable="/bin/bash",
    )
    res = eval_state(proc, f"{name}_cpp")
    return res, i


def make_arg_string(argtype, argval):
    if "[" not in argtype:
        return f"{argtype} {argval}"

    dim = argtype.count("[")
    argtype = argtype.replace("[", "").replace("]", "")
    return f'{argtype} {argval} {"[ ]" * dim}'


def convert_filled_arguments(script_model, f, lang, lang_processor, f_name=None):
    assert lang in {"java", "cpp"}
    header = []
    arguments_gold = lang_processor.extract_arguments(script_model)
    return_type_gold = get_return_type(script_model)

    arguments_filled = lang_processor.extract_arguments(f)
    return_type_filled = get_return_type(f)

    if arguments_gold[0] == arguments_filled[0]:
        return None
    if f_name is None:
        f_name = lang_processor.get_function_name(f)

    argument_types_gold = [t.strip() for t in arguments_gold[0]]
    arguments_strings = [
        make_arg_string(arg_type, f"param{i}")
        for i, arg_type in enumerate(argument_types_gold)
    ]
    new_function_lines = [
        f'static {return_type_gold} f_filled({", ".join(arguments_strings)})',
        "{",
    ]

    new_params_strings = []
    for param_index, (param_type_gold, param_type_filled) in enumerate(
        zip(argument_types_gold, arguments_filled[0])
    ):
        param_type_filled = param_type_filled.strip()
        param_type_gold = param_type_gold.strip()
        if param_type_filled == param_type_gold:
            new_params_strings.append(f"param{param_index}")
        elif lang == "cpp":
            if "vector" in param_type_filled:
                if "int" not in argument_types_gold:
                    return None
                ints_indices = [
                    i
                    for i, t in enumerate(argument_types_gold)
                    if t == "int" and i > param_index
                ]
                if any([i > param_index for i in ints_indices]):
                    array_length_arg = min([i for i in ints_indices if i > param_index])
                else:
                    array_length_arg = min(ints_indices)
                new_function_lines.append(
                    f'{param_type_filled.replace("&", "")} vect_param{param_index}(param{param_index}, param{param_index} + param{array_length_arg});'
                )
                new_params_strings.append(f"vect_param{param_index}")
            elif param_type_filled == "string" and "char" in param_type_gold:
                new_function_lines.append(
                    f'{param_type_filled.replace("&", "")} string_param{param_index}(param{param_index});'
                )
                new_params_strings.append(f"string_param{param_index}")
            elif param_type_gold == "string" and "char" in param_type_filled:
                new_function_lines.append(
                    f"char char_arr_param{param_index}[param{param_index}.length() + 1];"
                )
                new_function_lines.append(
                    f"strcopy(char_arr_param{param_index}, param{param_index}.c_str());"
                )
                new_params_strings.append(f"char_arr_param{param_index}")
            else:
                new_params_strings.append(f"({param_type_filled}) param{param_index}")
        elif lang == "java":
            if (
                param_type_filled == "String" and "char" in param_type_gold
            ) or param_type_filled == transform_to_java_object_type(param_type_gold):
                new_params_strings.append(
                    f"{param_type_filled}.valueOf(param{param_index})"
                )
                header.append("#include <cstring>")
            elif param_type_gold == "String":
                new_params_strings.append(f"param{param_index}.toCharArray()")
            else:
                new_params_strings.append(f"({param_type_filled}) param{param_index}")
        else:
            return None

    inner_function_name = "f_filled_inner"
    outer_f_return_string = f'{inner_function_name}({",".join(new_params_strings)})'
    if return_type_filled != return_type_gold:
        outer_f_return_string = f"({return_type_gold}) {outer_f_return_string}"
    new_function_lines += [f"return {outer_f_return_string};", "}"]

    f = lang_processor.detokenize_code(f.replace(f_name, inner_function_name))
    return "\n".join(list(set(header))) + script_model.replace(
        TOFILL[lang], "\n".join([f, "\n"] + new_function_lines)
    )


def submit_evosuite_functions(
    functions_list, id, lang, test_dictionary, roberta_mode=False
):
    assert lang in {"cpp", "python"}, f"{lang} is not supported for evosuite tests"
    if lang == "cpp":
        test_runner = CppTestRunner(timeout=30, compilation_timeout=30)
    else:
        assert lang == "python"
        test_runner = PythonTestRunner(timeout=30)
    lang_processor = LangProcessor.processors[lang](root_folder=TREE_SITTER_ROOT)
    id = id.rstrip()
    if id not in test_dictionary or test_dictionary[id] == "missing":
        return [return_script_not_found()], id
    test = test_dictionary[id]
    results_list = []
    for try_id, f_fill in enumerate(functions_list):
        f = f_fill.rstrip()
        f = (
            lang_processor.detokenize_code(f)
            if not roberta_mode
            else f.replace("#NEWLINE", "\n")
        )
        result = test_runner.get_tests_results(f, test)
        results_list.append((result[0], None))
        if result[0] == "success":
            return results_list, id
    return results_list, id


def submit_functions(
    functions_list,
    id,
    ref,
    lang,
    outfolder,
    script_folder,
    retry_mismatching_types,
    roberta_mode=False,
):
    lang_processor = LangProcessor.processors[lang](root_folder=TREE_SITTER_ROOT)
    results_list = []
    i = id.rstrip()
    for try_id, f_fill in enumerate(functions_list):
        f = f_fill.rstrip()
        script_model_path = os.path.join(script_folder, f"{lang}/{i}.{EXT[lang]}")
        if os.path.exists(script_model_path):
            script_model = open(script_model_path, "r", encoding="utf-8").read()
            try:
                f_name = lang_processor.get_function_name(f)
                f = f.replace(f_name, "f_filled")
            except:
                results_list.append(("error", "Could not replace function name"))
            if f_fill == ref:
                results_list.append(("success", "identical to gold"))
                return results_list, i
            f = (
                lang_processor.detokenize_code(f)
                if not roberta_mode
                else f.replace("#NEWLINE", "\n")
            )
            script = script_model.replace(TOFILL[lang], f)
            if lang == "python":
                script = f"import numpy as np \nimport math\nfrom math import *\nimport collections\nfrom collections import *\nimport heapq\nimport itertools\nimport random\nimport sys\n\n{script}"
            script_path = f"{outfolder}/{i}.{EXT[lang]}"
            open(script_path, "w", encoding="utf-8").write(script)
            run_pg = globals()[f"run_{lang}_program"]
            result, _ = run_pg(script_path, i)
            if result[0] == "success":
                results_list.append(result)
                return results_list, i
            elif retry_mismatching_types and lang in {"cpp", "java"}:
                try:
                    script_transform_args = convert_filled_arguments(
                        script_model, f_fill, lang, lang_processor, f_name=f_name
                    )
                except KeyboardInterrupt:
                    raise
                except:
                    script_transform_args = None

                if script_transform_args is not None:
                    open(script_path, "w", encoding="utf-8").write(
                        script_transform_args
                    )
                    run_pg = globals()[f"run_{lang}_program"]
                    result2, _ = run_pg(script_path, i)
                    if result2[0] == "success":
                        results_list.append(result2)
                        return results_list, i
                    else:
                        result = (
                            result2[0],
                            "".join(
                                [
                                    result[1] if result[1] else "",
                                    f"|| second run handling types mismatch: ## function ## {script_transform_args} ## output ## {result2[1]}",
                                ]
                            ),
                        )

            results_list.append(result)
        else:
            return [return_script_not_found()], i
    return results_list, i


def eval_function_output(
    ref_path,
    hyp_paths,
    id_path,
    lang2,
    outfolder,
    script_folder,
    retry_mismatching_types,
    roberta_mode,
    evosuite_functions=False,
    evosuite_tests=None,
):
    functions = list(zip(*[read_file_lines(path) for path in hyp_paths]))
    ids = read_file_lines(id_path)
    refs = read_file_lines(ref_path)
    assert len(functions) == len(ids), f"{len(functions), len(ids)}"
    assert len(functions) == len(refs), f"{len(functions), len(refs)}"
    lang = lang2.split("_")[0]
    jobs = []
    executor = ProcessPoolExecutor()
    for f, i, r in zip(functions, ids, refs):
        if evosuite_functions:
            jobs.append(
                executor.submit(
                    submit_evosuite_functions,
                    f,
                    i,
                    lang,
                    evosuite_tests[lang],
                    roberta_mode,
                )
            )
        else:
            jobs.append(
                executor.submit(
                    submit_functions,
                    f,
                    i,
                    r,
                    lang,
                    outfolder,
                    script_folder,
                    retry_mismatching_types,
                    roberta_mode,
                )
            )

    results_stats = {
        "success": 0,
        "failure": 0,
        "error": 0,
        "timeout": 0,
        "script_not_found": 0,
        "identical_gold": 0,
    }
    results = ["" for _ in range(len(ids))]
    for job in jobs:
        results_list, i = job.result()
        nb_success = sum([r[0] == "success" for r in results_list])
        nb_identical = sum(
            [r[0] == "success" and r[1] == "identical to gold" for r in results_list]
        )
        assert nb_success <= 1, "Should stop after first success"
        if nb_success > 0:
            results_stats["success"] += 1
            if nb_identical > 0:
                results_stats["identical_gold"] += 1
        else:
            results_stats[results_list[0][0]] = (
                results_stats.get(results_list[0][0], 0) + 1
            )
        results[ids.index(i + "\n")] = []
        for result, stderr in results_list:
            if stderr is not None:
                stderr = stderr.replace("\n", " ")
            else:
                stderr = "None"
            results[ids.index(i + "\n")].append(f"{result} : {stderr}")

    results_stats["total"] = len(functions)
    results_stats["total_evaluated"] = (
        len(functions) - results_stats["script_not_found"]
    )
    results_stats = {k: results_stats[k] for k in sorted(results_stats.keys())}

    return results_stats, results


def load_evosuite_transcoder_tests():
    cpp_test_translator = EvosuiteToCpp()
    python_test_translator = EvosuiteToPython()
    tests = {"java": {}, "java_scaffolding": {}, "python": {}, "cpp": {}}
    with open(EVOSUITE_TESTS_TRANSCODER_PATH, "r") as f:
        for l in f:
            json_line = json.loads(l)
            if json_line["tests_strings"] == "missing":
                continue
            tests["java"][json_line["TARGET_CLASS"]] = json_line["tests_strings"]
            tests["java_scaffolding"][json_line["TARGET_CLASS"]] = json_line[
                "scaffoldings_strings"
            ]
            python_test = python_test_translator.translate(json_line["tests_strings"])
            if not python_test_filter(python_test):
                continue
            tests["python"][json_line["TARGET_CLASS"]] = python_test

            cpp_test = cpp_test_translator.translate(json_line["tests_strings"])
            tests["cpp"][json_line["TARGET_CLASS"]] = cpp_test
    return tests


def python_test_filter(python_test):
    return (
        python_test.count("try ") == 0
        and python_test.count("catch(") == 0
        and python_test.count("assert ") > 0
    )


def return_script_not_found():
    return "script_not_found", None


def transform_to_java_object_type(t):
    if t not in primitive_types:
        return t
    if t == "int":
        return "Integer"
    if t == "char":
        return "Character"
    return t.capitalize()


def get_return_type(tokenized_java):
    return tokenized_java.split("(")[0].split()[-2]
