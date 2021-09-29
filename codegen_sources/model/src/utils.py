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
from pathlib import Path, PosixPath

import psutil

import numpy as np
import torch
from transformers.models.gpt2.tokenization_gpt2 import bytes_to_unicode

from .data.dictionary import NUM_SPECIAL_TOKENS

REPO_ROOT = Path(__file__).parents[3].absolute()
sys.path.append(str(REPO_ROOT))
print("adding to path", str(REPO_ROOT))
TREE_SITTER_ROOT = Path(__file__).parents[3].joinpath("tree-sitter")
import codegen_sources.preprocessing.lang_processors.cpp_processor
import codegen_sources.preprocessing.lang_processors.java_processor
import codegen_sources.preprocessing.lang_processors.python_processor
from codegen_sources.test_generation.test_runners.evosuite_test_runners import (
    SUPPORTED_LANGUAGES_FOR_TESTS,
)
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
    "lambda_st",
    "bt_sample_temperature",
    "st_sample_temperature",
    "st_sample_cache_ratio",
    "st_beam_size",
    "lambda_classif",
    "lambda_do",
    "st_min_asserts",
    "st_min_mutation_score",
]

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


def limit_virtual_memory(max_virtual_memory):
    # We do a soft limit in order to be able to change the limit later if needed
    return f"ulimit -S -v {max_virtual_memory}"


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


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
    text = "".join(line.replace(" ", ""))
    res = bytearray([byte_decoder[c] for c in text]).decode("utf-8", errors="replace")
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


def safe_index(l, elmt):
    try:
        return l.index(elmt)
    except ValueError:
        return None


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
            length_j = lengths[j].max() if len(lengths.shape) == 2 else lengths[j]
            for k in range(1, length_j):
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


def get_programming_language_name(lang):
    if lang in SUPPORTED_LANGUAGES_FOR_TESTS:
        return lang
    elif lang.split("_")[0] in SUPPORTED_LANGUAGES_FOR_TESTS:
        return lang.split("_")[0]
    else:
        raise ValueError(
            f"The language {lang} is not supported for unit tests self-training. "
            f"The supported languages are {SUPPORTED_LANGUAGES_FOR_TESTS}"
        )


def get_java_compilation_errors(code, timeout=20):
    file = write_java_function(code)
    comp_cmd = f"{limit_virtual_memory(MAX_VIRTUAL_MEMORY)}; {os.path.join(get_java_bin_path(), 'javac')} {file}"
    timed_out = False
    try:
        proc = subprocess.run(
            comp_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            executable="/bin/bash",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "timeout"
    file.unlink()
    classfile = file.with_suffix(".class")
    assert (
        timed_out or proc.returncode != 0 or classfile.is_file()
    ), "compilation succeeded but .class file does not exist"
    assert "tmp_folder" in str(file.parent), file.parent
    for compiled_f in file.parent.glob("*"):
        compiled_f.unlink()
    file.parent.rmdir()
    if timed_out:
        return "timeout"
    return "success" if proc.returncode == 0 else proc.stderr.decode()


def write_java_function(f: str, out_path: PosixPath = Path("/tmp/java_functions/")):
    rand_folder = str(random.getrandbits(64))
    classname = f"JAVA_FUNC"
    tmp_folder = out_path.joinpath(f"tmp_folder_{rand_folder}")
    out_file = tmp_folder.joinpath(classname + ".java")
    tmp_folder.mkdir(parents=True, exist_ok=True)
    java_processor = LangProcessor.processors["java"](root_folder=TREE_SITTER_ROOT)

    with open(out_file, "w") as writefile:
        writefile.write(
            """
import java.util.*;
import java.util.stream.*;
import java.lang.*;
import javafx.util.Pair;
"""
        )
        writefile.write("public class " + classname + "{\n")
        code = f.replace("\r", "")
        writefile.write(java_processor.detokenize_code(code))
        writefile.write("}\n")
    return out_file


def get_java_bin_path():
    JAVA_HOME = "/public/apps/java/jdk/1.8.0_131/bin/"
    if Path(JAVA_HOME).is_dir():
        return JAVA_HOME
    else:
        return ""
