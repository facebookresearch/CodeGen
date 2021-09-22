# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import argparse
import getpass
import math
import os
import pickle
import random
import re
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import psutil

import numpy as np
import torch
from transformers.models.gpt2.tokenization_gpt2 import bytes_to_unicode

from .data.dictionary import NUM_SPECIAL_TOKENS
from .logger import create_logger

sys.path.append(str(Path(__file__).parents[3]))
print("adding to path", str(Path(__file__).parents[3]))
TREE_SITTER_ROOT = Path(__file__).parents[3].joinpath("tree-sitter")
import codegen_sources.preprocessing.lang_processors.cpp_processor
import codegen_sources.preprocessing.lang_processors.java_processor
import codegen_sources.preprocessing.lang_processors.python_processor
from codegen_sources.preprocessing.lang_processors.lang_processor import LangProcessor
from .logger import create_logger

FALSY_STRINGS = {"off", "false", "0"}
TRUTHY_STRINGS = {"on", "true", "1"}

DUMP_PATH = "/checkpoint/%s/dumped" % getpass.getuser()
dynamic_coeff = [
    "lambda_clm",
    "lambda_mlm",
    "lambda_ae",
    "lambda_mt",
    "lambda_bt",
    "bt_sample_temperature",
    "lambda_classif",
    "lambda_do",
]

EXT = {"python": "py", "java": "java", "cpp": "cpp"}
TOFILL = {"python": "#TOFILL", "java": "//TOFILL", "cpp": "//TOFILL"}

primitive_types = {"short", "int", "long", "float", "double", "boolean", "char"}

MAX_VIRTUAL_MEMORY = 2 * 1024 * 1024 * 1024  # 2 GB


def show_batch(logger, to_print, dico, roberta_mode, example_type):

    """
    log first element of batch.
    x1 and x2 should be of size bs x slen
    """

    logger.info("")
    logger.info(f"========== {example_type} example ==========")
    for label, x in to_print:
        source_sentence = " ".join(
            [dico.id2word[int(w)] for w in x[0] if w != dico.pad_index]
        )
        logger.info(
            f"{label} sent: {restore_segmentation_sentence(source_sentence, roberta_mode)}"
        )
    logger.info("")
    for label, x in to_print:
        source_sentence = " ".join(
            [dico.id2word[int(w)] for w in x[0] if w != dico.pad_index]
        )
        logger.info(f"{label} tok: {source_sentence}")
    logger.info("")


def print_memory(logger, where):
    mem_av_gb = psutil.virtual_memory().available / (1024 ** 3)
    logger.info(f"MEMORY ({where}) : {mem_av_gb}")


def batch_sentences(sentences, pad_index, eos_index):
    """
    Take as input a list of n sentences (torch.LongTensor vectors) and return
    a tensor of size (slen, n) where slen is the length of the longest
    sentence, and a vector lengths containing the length of each sentence.
    """
    # sentences = sorted(sentences, key=lambda x: len(x), reverse=True)
    lengths = torch.LongTensor([len(s) + 2 for s in sentences])
    sent = torch.LongTensor(lengths.max().item(), lengths.size(0)).fill_(pad_index)

    sent[0] = eos_index
    for i, s in enumerate(sentences):
        if lengths[i] > 2:  # if sentence not empty
            sent[1 : lengths[i] - 1, i].copy_(torch.from_numpy(s.astype(np.int64)))
        sent[lengths[i] - 1, i] = eos_index

    return sent, lengths


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


def limit_virtual_memory(max_virtual_memory):
    # We do a soft limit in order to be able to change the limit later if needed
    return f"ulimit -S -v {max_virtual_memory}"


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def return_script_not_found():
    return "script_not_found", None


def eval_state(proc, proc_name):
    try:
        try:
            result, stderr = proc.communicate(timeout=30)
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
        f"{limit_virtual_memory(MAX_VIRTUAL_MEMORY)}; cd {folder} && module load java && javac {name}.java && java {name}",
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
            results_stats[results_list[0][0]] += 1
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


def read_file_lines(hyp_path):
    with open(hyp_path, "r", encoding="utf-8") as f:
        functions = f.readlines()
    return functions


def bool_flag(s):
    """
    Parse boolean arguments from the command line.
    """
    if s.lower() in FALSY_STRINGS:
        return False
    elif s.lower() in TRUTHY_STRINGS:
        return True
    else:
        raise argparse.ArgumentTypeError("Invalid value for a boolean flag!")


def initialize_exp(params):
    """
    Initialize the experience:
    - dump parameters
    - create a logger
    """
    # dump parameters
    get_dump_path(params)
    pickle.dump(params, open(os.path.join(params.dump_path, "params.pkl"), "wb"))

    # get running command
    command = ["python", sys.argv[0]]
    for x in sys.argv[1:]:
        if x.startswith("--"):
            assert '"' not in x and "'" not in x
            command.append(x)
        else:
            assert "'" not in x
            if re.match("^[a-zA-Z0-9_]+$", x):
                command.append("%s" % x)
            else:
                command.append("'%s'" % x)
    command = " ".join(command)
    params.command = command + ' --exp_id "%s"' % params.exp_id

    # check experiment name
    assert len(params.exp_name.strip()) > 0

    # create a logger
    logger = create_logger(
        os.path.join(params.dump_path, "train.log"),
        rank=getattr(params, "global_rank", 0),
    )
    logger.info("============ Initialized logger ============")
    logger.info(
        "\n".join("%s: %s" % (k, str(v)) for k, v in sorted(dict(vars(params)).items()))
    )
    logger.info("The experiment will be stored in %s\n" % params.dump_path)
    logger.info("Running command: %s" % command)
    logger.info("")
    return logger


def get_dump_path(params):
    """
    Create a directory to store the experiment.
    """
    dump_path = DUMP_PATH if params.dump_path == "" else params.dump_path
    assert len(params.exp_name) > 0

    # create the sweep path if it does not exist
    sweep_path = os.path.join(dump_path, params.exp_name)
    if not os.path.exists(sweep_path):
        subprocess.Popen("mkdir -p %s" % sweep_path, shell=True).wait()

    # create an ID for the job if it is not given in the parameters.
    # if we run on the cluster, the job ID is the one of Chronos.
    # otherwise, it is randomly generated
    if params.exp_id == "":
        chronos_job_id = os.environ.get("CHRONOS_JOB_ID")
        slurm_job_id = os.environ.get("SLURM_JOB_ID")
        assert chronos_job_id is None or slurm_job_id is None
        exp_id = chronos_job_id if chronos_job_id is not None else slurm_job_id
        if exp_id is None:
            chars = "abcdefghijklmnopqrstuvwxyz0123456789"
            while True:
                exp_id = "".join(random.choice(chars) for _ in range(10))
                if not os.path.isdir(os.path.join(sweep_path, exp_id)):
                    break
        else:
            assert exp_id.isdigit()
        params.exp_id = exp_id

    # create the dump folder / update parameters
    params.dump_path = os.path.join(sweep_path, params.exp_id)
    if not os.path.isdir(params.dump_path):
        subprocess.Popen("mkdir -p %s" % params.dump_path, shell=True).wait()


def to_cuda(*args):
    """
    Move tensors to CUDA.
    """
    return [None if x is None else x.cuda() for x in args]


def restore_segmentation_sentence(sentence, roberta_mode):
    """
    Take a sentence segmented with BPE and restore it to its original segmentation.
    """
    if roberta_mode:
        return restore_roberta_segmentation_sentence(sentence)
    else:
        return sentence.replace("@@ ", "")


def restore_segmentation(path, roberta_mode=False, single_line=False):
    """
    Take a file segmented with BPE and restore it to its original segmentation.
    """
    assert os.path.isfile(path)
    if not roberta_mode:
        restore_fastBPE_segmentation(path)
    else:
        return restore_roberta_segmentation(path, single_line=single_line)


def restore_roberta_segmentation(path, single_line=False):
    with open(path, "r", encoding="utf-8", errors="replace") as input_file:
        text_inputs = input_file.read().split("\n")
    output = restore_roberta_segmentation_string(text_inputs, single_line)
    with open(path, "w") as output_path:
        output_path.write(output)


def restore_roberta_segmentation_string(text_inputs, single_line=False):
    if isinstance(text_inputs, str):
        text_inputs = text_inputs.splitlines()
    output_lines = [
        restore_roberta_segmentation_sentence(line, single_line=single_line)
        for line in text_inputs
    ]
    return "\n".join(output_lines)


def restore_roberta_segmentation_sentence(line, single_line=False):
    byte_encoder = bytes_to_unicode()
    byte_decoder = {v: k for k, v in byte_encoder.items()}
    text = line.replace(" ", "")
    res = bytearray([byte_decoder.get(c, 0) for c in text]).decode("utf-8", errors="replace")
    return res.replace("\n", "#NEWLINE") if single_line else res


def restore_fastBPE_segmentation(path):
    restore_cmd = "sed -i -r 's/(@@ )|(@@ ?$)//g' %s"
    subprocess.Popen(restore_cmd % path, shell=True).wait()


def parse_lambda_config(params):
    """
    Parse the configuration of lambda coefficient (for scheduling).
    x = "3"                  # lambda will be a constant equal to x
    x = "0:1,1000:0"         # lambda will start from 1 and linearly decrease to 0 during the first 1000 iterations
    x = "0:0,1000:0,2000:1"  # lambda will be equal to 0 for the first 1000 iterations, then will linearly increase to 1 until iteration 2000
    """

    # for lambda_classif possibility to have one lambda per pair of language, so split per languages fisrt
    global dynamic_coeff
    if len(params.classif_steps) > 0:
        x = getattr(params, "lambda_classif")
        split = [s.split("::") for s in x.split("/")]
        assert all(len(s) == 2 or len(s) == 1 for s in split)
        assert all(
            tuple(s[0].split("-")) in params.classif_steps for s in split if len(s) == 2
        )
        assert sum([1 if len(s) == 1 else 0 for s in split]) < 2
        general_lambda = "1"
        for s in split:
            if len(s) == 1:
                general_lambda = s[0]
                break
        lambda_by_step = {s[0]: s[1] for s in split if len(s) == 2}
        for step in params.classif_steps:
            step = "-".join(step)
            if step in lambda_by_step:
                setattr(
                    params,
                    "lambda_classif" + "_" + step.replace("-", "_"),
                    lambda_by_step[step],
                )
            else:
                setattr(
                    params,
                    "lambda_classif" + "_" + step.replace("-", "_"),
                    general_lambda,
                )
            dynamic_coeff.append("lambda_classif" + "_" + step.replace("-", "_"))

        dynamic_coeff.remove("lambda_classif")

    for name in dynamic_coeff:
        x = getattr(params, name)
        split = x.split(",")
        if len(split) == 1:
            setattr(params, name, float(x))
            setattr(params, name + "_config", None)
        else:
            split = [s.split(":") for s in split]
            assert all(len(s) == 2 for s in split)
            assert all(k.isdigit() for k, _ in split)
            assert all(
                int(split[i][0]) < int(split[i + 1][0]) for i in range(len(split) - 1)
            )
            setattr(params, name, float(split[0][1]))
            setattr(params, name + "_config", [(int(k), float(v)) for k, v in split])


def get_lambda_value(config, n_iter):
    """
    Compute a lambda value according to its schedule configuration.
    """
    ranges = [
        i for i in range(len(config) - 1) if config[i][0] <= n_iter < config[i + 1][0]
    ]
    if len(ranges) == 0:
        assert n_iter >= config[-1][0]
        return config[-1][1]
    assert len(ranges) == 1
    i = ranges[0]
    x_a, y_a = config[i]
    x_b, y_b = config[i + 1]
    return y_a + (n_iter - x_a) * float(y_b - y_a) / float(x_b - x_a)


def update_lambdas(params, n_iter):
    """
    Update all lambda coefficients.
    """
    for name in dynamic_coeff:
        config = getattr(params, name + "_config")
        if config is not None:
            setattr(params, name, get_lambda_value(config, n_iter))


def set_sampling_probs(data, params):
    """
    Set the probability of sampling specific languages / language pairs during training.
    """
    coeff = params.lg_sampling_factor
    if coeff == -1:
        return
    assert coeff > 0

    # monolingual data
    params.mono_list = [k for k, v in data["mono_stream"].items() if "train" in v]
    if len(params.mono_list) > 0:
        probs = np.array(
            [1.0 * len(data["mono_stream"][lang]["train"]) for lang in params.mono_list]
        )
        probs /= probs.sum()
        probs = np.array([p ** coeff for p in probs])
        probs /= probs.sum()
        params.mono_probs = probs

    # parallel data
    params.para_list = [k for k, v in data["para"].items() if "train" in v]
    if len(params.para_list) > 0:
        probs = np.array(
            [
                1.0 * len(data["para"][(l1, l2)]["train"])
                for (l1, l2) in params.para_list
            ]
        )
        probs /= probs.sum()
        probs = np.array([p ** coeff for p in probs])
        probs /= probs.sum()
        params.para_probs = probs


def concat_batches(
    x1, len1, lang1_id, x2, len2, lang2_id, pad_idx, eos_idx, reset_positions
):
    """
    Concat batches with different languages.
    """
    assert reset_positions is False or lang1_id != lang2_id
    lengths = len1 + len2
    if not reset_positions:
        lengths -= 1
    slen, bs = lengths.max().item(), lengths.size(0)

    x = x1.new(slen, bs).fill_(pad_idx)
    x[: len1.max().item()].copy_(x1)
    positions = torch.arange(slen)[:, None].repeat(1, bs).to(x1.device)
    langs = x1.new(slen, bs).fill_(lang1_id)

    for i in range(bs):
        l1 = len1[i] if reset_positions else len1[i] - 1
        x[l1 : l1 + len2[i], i].copy_(x2[: len2[i], i])
        if reset_positions:
            positions[l1:, i] -= len1[i]
        langs[l1:, i] = lang2_id

    assert (x == eos_idx).long().sum().item() == (4 if reset_positions else 3) * bs

    return x, lengths, positions, langs


def truncate(x, lengths, max_len, eos_index):
    """
    Truncate long sentences.
    """
    if lengths.max().item() > max_len:
        x = x[:max_len].clone()
        lengths = lengths.clone()
        for i in range(len(lengths)):
            if lengths[i] > max_len:
                lengths[i] = max_len
                x[max_len - 1, i] = eos_index
    return x, lengths


def shuf_order(langs, params=None, n=5):
    """
    Randomize training order.
    """
    if len(langs) == 0:
        return []

    if params is None:
        return [langs[i] for i in np.random.permutation(len(langs))]

    # sample monolingual and parallel languages separately
    mono = []
    para = []
    for l in langs:
        assert len(l) > 0
        if len(l) == 1 or l[1] is None:
            mono.append(l[0])
        else:
            para.append(l)

    # uniform / weighted sampling
    if params.lg_sampling_factor == -1:
        p_mono = None
        p_para = None
    else:
        p_mono = np.array([params.mono_probs[params.mono_list.index(k)] for k in mono])
        p_para = np.array(
            [params.para_probs[params.para_list.index(tuple(sorted(k)))] for k in para]
        )
        p_mono = p_mono / p_mono.sum()
        p_para = p_para / p_para.sum()

    s_mono = (
        [
            mono[i]
            for i in np.random.choice(
                len(mono), size=min(n, len(mono)), p=p_mono, replace=True
            )
        ]
        if len(mono) > 0
        else []
    )
    s_para = (
        [
            para[i]
            for i in np.random.choice(
                len(para), size=min(n, len(para)), p=p_para, replace=True
            )
        ]
        if len(para) > 0
        else []
    )

    assert len(s_mono) + len(s_para) > 0
    return [(lang, None) for lang in s_mono] + s_para


def vizualize_translated_files(
    lang1, lang2, src_file, hyp_file, ids, ref_file=None, out_file=None
):
    lang1_processor = LangProcessor.processors[lang1.split("_")[0]](
        root_folder=TREE_SITTER_ROOT
    )
    lang2_processor = LangProcessor.processors[lang2.split("_")[0]](
        root_folder=TREE_SITTER_ROOT
    )
    src_viz = str(Path(src_file).with_suffix(".vizualize.txt"))
    hyp_viz = str(
        Path(re.sub("beam\d", "", hyp_file[0])).with_suffix(".vizualize.txt.tmp")
    )
    if ref_file is None:
        ref_viz = str(Path("ref_tmp").with_suffix(".vizualize.txt"))
    else:
        ref_viz = str(Path(ref_file).with_suffix(".vizualize.txt"))
    if out_file is None:
        out_viz = str(Path("out_tmp").with_suffix(".vizualize.txt"))
    else:
        out_viz = str(
            Path(re.sub("beam\d", "", out_file[0])).with_suffix(".vizualize.txt")
        )

    ids = open(ids, "r", encoding="utf-8").readlines()

    hyp_lines = list(
        zip(*[read_file_lines(path) for path in hyp_file])
    )  # test_size * beam_size
    beam_size = len(hyp_lines[0])

    with open(src_file, encoding="utf-8") as f:
        src_lines = f.readlines()  # test_size

    if ref_file is not None:
        with open(ref_file, encoding="utf-8") as f:
            ref_lines = f.readlines()  # test_size
    else:
        ref_lines = ["" for _ in range(len(src_lines))]

    if out_file is not None:
        out_lines = list(
            zip(*[read_file_lines(path) for path in out_file])
        )  # test_size * beam_size
    else:
        out_lines = [
            ["" for n in range(len(hyp_lines[0]))] for l in range(len(src_lines))
        ]

    with open(src_viz, "w", encoding="utf-8") as src_vizf:
        with open(hyp_viz, "w", encoding="utf-8") as hyp_vizf:
            with open(ref_viz, "w", encoding="utf-8") as ref_vizf:
                with open(out_viz, "w", encoding="utf-8") as out_vizf:
                    src_vizf.write(
                        "========================SOURCE============================\n"
                    )
                    hyp_vizf.write(
                        "=========================HYPO=============================\n"
                    )
                    ref_vizf.write(
                        "==========================REF=============================\n"
                    )
                    out_vizf.write(
                        "==========================OUT=============================\n"
                    )

                    for src, hyps, ref, outs, i in zip(
                        src_lines, hyp_lines, ref_lines, out_lines, ids
                    ):
                        src_vizf.write(
                            "=========================================================\n"
                        )
                        hyp_vizf.write(
                            "=========================================================\n"
                        )
                        ref_vizf.write(
                            "=========================================================\n"
                        )
                        out_vizf.write(
                            "=========================================================\n"
                        )
                        src_vizf.write(f"{i}")
                        hyp_vizf.write(f"{i}")
                        ref_vizf.write(f"{i}")
                        out_vizf.write(f"{i}")
                        src_vizf.write("--\n")
                        hyp_vizf.write("--\n")
                        ref_vizf.write("--\n")
                        out_vizf.write("--\n")

                        try:
                            src = lang1_processor.detokenize_code(src)
                            src_vizf.write(src)
                        except:
                            src = "".join(
                                [
                                    c if (i + 1) % 50 != 0 else c + "\n"
                                    for i, c in enumerate(src)
                                ]
                            )
                            src_vizf.write(src)

                        try:
                            ref = lang2_processor.detokenize_code(ref)
                            ref_vizf.write(ref)
                        except:
                            ref = "".join(
                                [
                                    c if (i + 1) % 50 != 0 else c + "\n"
                                    for i, c in enumerate(ref)
                                ]
                            )
                            ref_vizf.write(ref)

                        for i in range(beam_size):
                            hyp = hyps[i]
                            out = outs[i]
                            try:
                                hyp = lang2_processor.detokenize_code(hyp)
                                hyp_vizf.write(hyp)
                            except:
                                hyp = "".join(
                                    [
                                        c if (i + 1) % 50 != 0 else c + "\n"
                                        for i, c in enumerate(hyp)
                                    ]
                                )
                                hyp_vizf.write(hyp)

                            out = "".join(
                                [
                                    c if (i + 1) % 50 != 0 else c + "\n"
                                    for i, c in enumerate(out)
                                ]
                            )
                            out_vizf.write(out)

                            if i == 0:
                                maximum = max(
                                    len(src.split("\n")),
                                    len(hyp.split("\n")),
                                    len(ref.split("\n")),
                                    len(out.split("\n")),
                                )
                                for i in range(len(src.split("\n")), maximum):
                                    src_vizf.write("\n")
                                for i in range(len(hyp.split("\n")), maximum):
                                    hyp_vizf.write("\n")
                                for i in range(len(ref.split("\n")), maximum):
                                    ref_vizf.write("\n")
                                for i in range(len(out.split("\n")), maximum):
                                    out_vizf.write("\n")
                            else:
                                maximum = max(
                                    len(hyp.split("\n")), len(out.split("\n"))
                                )
                                for i in range(maximum - 1):
                                    src_vizf.write("\n")
                                for i in range(maximum - 1):
                                    ref_vizf.write("\n")
                                for i in range(len(hyp.split("\n")), maximum):
                                    hyp_vizf.write("\n")
                                for i in range(len(out.split("\n")), maximum):
                                    out_vizf.write("\n")
                            src_vizf.write("-\n")
                            hyp_vizf.write("-\n")
                            ref_vizf.write("-\n")
                            out_vizf.write("-\n")

                        src_vizf.write("--\n\n")
                        hyp_vizf.write("--\n\n")
                        ref_vizf.write("--\n\n")
                        out_vizf.write("--\n\n")

    command = (
        f"pr -w 250 -m -t {src_viz} {ref_viz} {hyp_viz} {out_viz} > {hyp_viz[:-4]}"
    )
    subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).wait()

    os.remove(src_viz)
    os.remove(ref_viz)
    os.remove(hyp_viz)
    os.remove(out_viz)


def vizualize_do_files(lang1, src_file, ref_file, hyp_file):
    lang1_processor = LangProcessor.processors[lang1.split("_")[0]](
        root_folder=TREE_SITTER_ROOT
    )
    src_viz = str(Path(src_file).with_suffix(".vizualize.txt"))
    hyp_viz = str(
        Path(re.sub("beam\d", "", hyp_file[0])).with_suffix(".vizualize.txt.tmp")
    )
    ref_viz = str(Path(ref_file).with_suffix(".vizualize.txt"))

    hyp_lines = list(
        zip(*[read_file_lines(path) for path in hyp_file])
    )  # test_size * beam_size
    beam_size = len(hyp_lines[0])

    with open(src_file, encoding="utf-8") as f:
        src_lines = f.readlines()  # test_size

    with open(ref_file, encoding="utf-8") as f:
        ref_lines = f.readlines()  # test_size

    with open(src_viz, "w", encoding="utf-8") as src_vizf:
        with open(hyp_viz, "w", encoding="utf-8") as hyp_vizf:
            with open(ref_viz, "w", encoding="utf-8") as ref_vizf:
                src_vizf.write(
                    "========================SOURCE============================\n"
                )
                hyp_vizf.write(
                    "=========================HYPO=============================\n"
                )
                ref_vizf.write(
                    "==========================REF=============================\n"
                )

                for src, hyps, ref in zip(src_lines, hyp_lines, ref_lines):
                    src_vizf.write(
                        "=========================================================\n"
                    )
                    hyp_vizf.write(
                        "=========================================================\n"
                    )
                    ref_vizf.write(
                        "=========================================================\n"
                    )
                    try:
                        src = lang1_processor.detokenize_code(src)
                        src_vizf.write(src)
                    except:
                        src = "".join(
                            [
                                c if (i + 1) % 50 != 0 else c + "\n"
                                for i, c in enumerate(src)
                            ]
                        )
                        src_vizf.write(src)

                    ref = ref.replace("|", "\n").strip()
                    ref_vizf.write(ref)

                    for i in range(beam_size):
                        hyp = hyps[i]
                        hyp = hyp.replace("|", "\n").strip()
                        hyp_vizf.write(hyp)
                        if i == 0:
                            maximum = max(
                                len(src.split("\n")),
                                len(hyp.split("\n")),
                                len(ref.split("\n")),
                            )
                            for i in range(len(src.split("\n")), maximum):
                                src_vizf.write("\n")
                            for i in range(len(hyp.split("\n")), maximum):
                                hyp_vizf.write("\n")
                            for i in range(len(ref.split("\n")), maximum):
                                ref_vizf.write("\n")
                        else:
                            maximum = max(
                                len(src.split("\n")),
                                len(hyp.split("\n")),
                                len(ref.split("\n")),
                            )
                            for i in range(maximum - 1):
                                src_vizf.write("\n")
                            for i in range(maximum - 1):
                                ref_vizf.write("\n")
                            for i in range(len(hyp.split("\n")), maximum):
                                hyp_vizf.write("\n")
                        src_vizf.write("-\n")
                        hyp_vizf.write("-\n")
                        ref_vizf.write("-\n")

                    src_vizf.write("--\n\n")
                    hyp_vizf.write("--\n\n")
                    ref_vizf.write("--\n\n")

    command = f"pr -w 250 -m -t {src_viz} {ref_viz} {hyp_viz} > {hyp_viz[:-4]}"
    subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).wait()

    os.remove(src_viz)
    os.remove(ref_viz)
    os.remove(hyp_viz)


def set_MKL_env_vars():
    for k in ["MKL_THREADING_LAYER", "MKL_SERVICE_FORCE_INTEL"]:
        print(f"{k}: {os.environ.get(k)}")
        if os.environ.get(k) is None:
            print(f"Setting {k} to GNU")
            os.environ[k] = "GNU"


def word_shuffle(x, l, params, rng=None):
    """
    Randomly shuffle input words.
    """
    if params.word_shuffle == 0:
        return x, l

    # define noise word scores
    noise = rng.uniform(0, params.word_shuffle, size=(x.size(0) - 1, x.size(1)))
    noise[0] = -1  # do not move start sentence symbol

    assert params.word_shuffle > 1
    x2 = x.clone()
    for i in range(l.size(0)):
        # generate a random permutation
        scores = np.arange(l[i] - 1) + noise[: l[i] - 1, i]
        permutation = scores.argsort()
        # shuffle words
        x2[: l[i] - 1, i].copy_(x2[: l[i] - 1, i][torch.from_numpy(permutation)])
    return x2, l


def word_dropout(x, l, params, rng):
    """
    Randomly drop input words.
    """
    if params.word_dropout == 0:
        return x, l
    assert 0 < params.word_dropout < 1

    # define words to drop
    eos = params.eos_index
    assert (x[0] == eos).sum() == l.size(0)
    keep = rng.rand(x.size(0) - 1, x.size(1)) >= params.word_dropout
    keep[0] = 1  # do not drop the start sentence symbol

    sentences = []
    lengths = []
    for i in range(l.size(0)):
        assert x[l[i] - 1, i] == eos
        words = x[: l[i] - 1, i].tolist()
        # randomly drop words from the input
        new_s = [w for j, w in enumerate(words) if keep[j, i]]
        # we need to have at least one word in the sentence (more than the start / end sentence symbols)
        if len(new_s) == 1:
            new_s.append(words[np.random.randint(1, len(words))])
        new_s.append(eos)
        assert len(new_s) >= 3 and new_s[0] == eos and new_s[-1] == eos
        sentences.append(new_s)
        lengths.append(len(new_s))
    # re-construct input
    l2 = torch.LongTensor(lengths)
    x2 = torch.LongTensor(l2.max(), l2.size(0)).fill_(params.pad_index)
    for i in range(l2.size(0)):
        x2[: l2[i], i].copy_(torch.LongTensor(sentences[i]))
    return x2, l2


def word_blank(x, l, params, rng):
    """
    Randomly blank input words.
    """
    if params.word_blank == 0:
        return x, l
    assert 0 < params.word_blank < 1

    # define words to blank
    eos = params.eos_index
    assert (x[0] == eos).sum() == l.size(0)
    keep = rng.rand(x.size(0) - 1, x.size(1)) >= params.word_blank
    keep[0] = 1  # do not blank the start sentence symbol

    sentences = []
    for i in range(l.size(0)):
        assert x[l[i] - 1, i] == eos
        words = x[: l[i] - 1, i].tolist()
        # randomly blank words from the input
        new_s = [w if keep[j, i] else params.mask_index for j, w in enumerate(words)]
        new_s.append(eos)
        assert len(new_s) == l[i] and new_s[0] == eos and new_s[-1] == eos
        sentences.append(new_s)
    # re-construct input
    x2 = torch.LongTensor(l.max(), l.size(0)).fill_(params.pad_index)
    for i in range(l.size(0)):
        x2[: l[i], i].copy_(torch.LongTensor(sentences[i]))
    return x2, l


def span_masking(x, len, params, max_vocab, rng, torch_rng):
    if params.mask_length_dist is None:
        return word_blank(x, len, params, rng)
    else:
        sentences = [
            mask_spans(x[:l, i], params, max_vocab, torch_rng)
            for i, l in zip(range(x.size(1)), len)
        ]
        newlen = torch.LongTensor([s.size(0) for s in sentences])
        sent = torch.LongTensor(newlen.max().item(), newlen.size(0)).fill_(
            params.pad_index
        )
        sent[0] = params.eos_index
        for i, s in enumerate(sentences):
            if newlen[i] > 2:  # if sentence not empty
                sent[0 : newlen[i], i] = s
            sent[newlen[i] - 1, i] = params.eos_index
        return sent, newlen


def mask_spans(x, params, max_vocab, torch_rng):
    """
    Randomly masks spans or replaces with random words
    """
    assert x[0].item() == x[-1].item() == params.eos_index
    assert (x != params.pad_index).all().item()
    source_length = len(x)
    num_to_mask = math.ceil(source_length * params.word_blank)
    lengths = torch.multinomial(
        params.mask_length_dist_probas,
        num_to_mask,
        replacement=True,
        generator=torch_rng,
    )
    if lengths.sum() > num_to_mask:
        cum_length = torch.cumsum(lengths, 0)

        # Trim to masking budget
        i = 0
        while cum_length[i] < num_to_mask:
            i += 1
        lengths[i] = num_to_mask - (0 if i == 0 else cum_length[i - 1])
        num_to_mask = i + 1
        lengths = lengths[:num_to_mask]

    # Handle 0-length mask (inserts) separately
    lengths = lengths[lengths > 0]
    num_inserts = num_to_mask - lengths.size(0)
    num_to_mask -= num_inserts
    if num_to_mask == 0:
        return insert_tokens(x, num_inserts, params, max_vocab, torch_rng)

    # indices to mask without start or end symbol
    indices = torch.randperm(source_length - 2, generator=torch_rng)[:num_to_mask] + 1
    assert source_length - 1 not in indices
    assert 0 not in indices
    mask_random = (
        torch.FloatTensor(num_to_mask).uniform_(generator=torch_rng) < params.word_rand
    )

    to_keep = torch.ones(source_length, dtype=torch.bool)
    # keep first index, but replace it with [MASK] or random token
    probs = torch.multinomial(
        params.pred_probs, len(indices), replacement=True, generator=torch_rng
    )
    _x_real = x[indices]
    _x_rand = _x_real.clone().random_(params.n_words)
    _x_mask = _x_real.clone().fill_(params.mask_index)
    _x = (
        _x_mask * (probs == 0).long()
        + _x_real * (probs == 1).long()
        + _x_rand * (probs == 2).long()
    )

    x[indices] = _x

    assert len(lengths.size()) == 1
    assert lengths.size() == indices.size()
    lengths -= 1
    while indices.size(0) > 0:
        assert lengths.size() == indices.size()
        lengths -= 1
        uncompleted = (lengths >= 0) & (indices < source_length - 1)
        indices = indices[uncompleted] + 1
        mask_random = mask_random[uncompleted]
        lengths = lengths[uncompleted]
        # delete token
        to_keep[indices] = 0
    to_keep[0] = 1
    to_keep[-1] = 1

    x = x[to_keep]
    if num_inserts > 0:
        x = insert_tokens(x, num_inserts, params, max_vocab, torch_rng)

    assert x[0].item() == x[-1].item() == params.eos_index
    return x


def insert_tokens(x, n, params, max_vocab, torch_rng):
    num_tokens = len(x)

    # insert in a position which is not the first or the last one
    noise_indices = torch.randperm(num_tokens + n - 2, generator=torch_rng)[:n] + 1
    noise_mask = torch.zeros(size=(num_tokens + n,), dtype=torch.bool)

    noise_mask[noise_indices] = 1
    num_random = (
        torch.FloatTensor(n).uniform_(generator=torch_rng) < params.word_rand
    ).sum()

    result = torch.LongTensor(n + num_tokens).fill_(-1)

    result[noise_indices[num_random:]] = params.mask_index
    result[noise_indices[:num_random]] = torch.randint(
        low=NUM_SPECIAL_TOKENS, high=max_vocab, size=(num_random,), generator=torch_rng
    )
    result[~noise_mask] = x
    assert (result >= 0).all()
    return result


def add_noise(words, lengths, params, max_vocab, rng=None, torch_rng=None):
    """
    Add noise to the encoder input.
    """
    if rng is None:
        rng = np.random.RandomState()
    words, lengths = word_shuffle(words, lengths, params=params, rng=rng)
    words, lengths = word_dropout(words, lengths, params, rng=rng)
    words, lengths = span_masking(
        words, lengths, params, max_vocab, rng=rng, torch_rng=torch_rng
    )
    return words, lengths


def convert_to_text(batch, lengths, dico, params, generate_several_reps=False):
    """
    Convert a batch of sentences to a list of text sentences.
    """
    batch = batch.cpu().numpy()
    lengths = lengths.cpu().numpy()

    assert (
        len(batch.shape) == 2 or len(batch.shape) == 3
    ), f"generated batch shape was {batch.shape} while it should be in dimension 2 or 3"
    nb_repetitions = 1
    if len(batch.shape) == 2:
        slen, bs = batch.shape
        assert (batch[0] == params.eos_index).sum() == bs
        assert (batch == params.eos_index).sum() == 2 * bs
    else:
        slen, nb_repetitions, bs = batch.shape
        assert (batch == params.eos_index).sum() == 2 * bs * nb_repetitions
        assert (batch[0] == params.eos_index).sum() == bs * nb_repetitions, print(
            f"The values were {(batch[0] == params.eos_index).sum()} and  {bs * nb_repetitions}"
        )
    assert lengths.max() == slen and lengths.shape[0] == bs, print(
        lengths.max(), slen, lengths.shape[0], bs
    )
    sentences = []

    for j in range(bs):
        sentences.append([])
        for rep in range(nb_repetitions):
            words = []
            for k in range(1, lengths[j]):
                next_element = (
                    batch[k, j] if len(batch.shape) == 2 else batch[k, rep, j]
                )
                if next_element == params.eos_index:
                    break
                words.append(dico[next_element])
            sentences[j].append(" ".join(words))
    if generate_several_reps:
        return sentences
    else:
        return [s[0] for s in sentences]
