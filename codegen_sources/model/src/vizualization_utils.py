# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

import torch

from .constants import REF, OUT, HYPO, IR, SOURCE
from .utils import get_programming_language_name, read_file_lines, TOK_AVOID_NEWLINE

LTensor = torch.LongTensor

REPO_ROOT = Path(__file__).parents[3].absolute()
sys.path.append(str(REPO_ROOT))
print("adding to path", str(REPO_ROOT))
from codegen_sources.preprocessing.lang_processors import LangProcessor, IRProcessor


def vizualize_translated_files(
    lang1_processor,
    lang2_processor,
    src_file,
    hyp_file,
    ids,
    ref_file=None,
    out_file=None,
    irs_file=None,
    page_width: int = 250,
    tokenization_mode="fastbpe",
):
    if tokenization_mode != "fastbpe":
        lang1_processor = lang2_processor = None
    each_width = page_width // 4 - 4 if irs_file is None else (page_width // 5 - 4)
    if isinstance(lang1_processor, str):
        lang1_processor = LangProcessor.processors[
            get_programming_language_name(lang1_processor)
        ]()
    if isinstance(lang2_processor, str):
        lang2_processor = LangProcessor.processors[
            get_programming_language_name(lang2_processor)
        ]()
    ir_processor = None
    if irs_file:
        ir_processor = IRProcessor()
    src_viz = str(Path(src_file).with_suffix(".vizualize.txt"))
    hyp_viz = str(
        Path(re.sub("beam\d", "", hyp_file[0])).with_suffix(".vizualize.txt.tmp")
    )
    if ref_file is None:
        ref_viz = str(Path("ref_tmp").with_suffix(".vizualize.txt"))
    else:
        ref_viz = str(Path(ref_file).with_suffix(".vizualize.txt"))
    if irs_file is not None:
        ir_viz = str(Path(irs_file).with_suffix(".vizualize.txt"))
    else:
        ir_viz = None

    if out_file is None:
        out_viz = str(Path("out_tmp").with_suffix(".vizualize.txt"))
    else:
        out_viz = str(
            Path(re.sub("beam\d", "", out_file[0])).with_suffix(".vizualize.txt")
        )

    hyp_lines = list(
        zip(*[read_file_lines(path) for path in hyp_file])
    )  # test_size * beam_size
    ids = (
        open(ids, "r", encoding="utf-8").readlines()
        if ids is not None
        else [""] * len(hyp_lines)
    )
    beam_size = len(hyp_lines[0])

    with open(src_file, encoding="utf-8") as f:
        src_lines = f.readlines()  # test_size

    if ref_file is not None:
        with open(ref_file, encoding="utf-8") as f:
            ref_lines = f.readlines()  # test_size
    else:
        ref_lines = ["" for _ in range(len(src_lines))]

    if irs_file is None:
        irs_lines = [""] * len(src_lines)
    else:
        with open(irs_file, encoding="utf-8") as f:
            irs_lines = f.readlines()  # test_size

    if out_file is not None:
        out_lines = list(
            zip(*[read_file_lines(path) for path in out_file])
        )  # test_size * beam_size
    else:
        out_lines = [
            ["" for _ in range(len(hyp_lines[0]))] for _ in range(len(src_lines))
        ]

    to_show = [
        (SOURCE, src_viz),
        (IR, ir_viz),
        (HYPO, hyp_viz),
        (REF, ref_viz),
        (OUT, out_viz),
    ]
    to_show = [x for x in to_show if x[1]]
    file_writers = {
        header: open(str(path), "w", encoding="utf-8") for header, path in to_show
    }
    try:
        for header, writer in file_writers.items():
            writer.write(
                f"========================{header}============================\n"
            )

        for src, ir, hyps, ref, outs, i in zip(
            src_lines, irs_lines, hyp_lines, ref_lines, out_lines, ids
        ):
            for header, writer in file_writers.items():
                writer.write(
                    "=========================================================\n"
                )
                writer.write(f"{i}")
                writer.write("--\n")
            try:
                if lang1_processor:
                    src = overflow_fill(
                        lang1_processor.detokenize_code(src), each_width
                    )
                src = src.replace(TOK_AVOID_NEWLINE, "\n")

                file_writers[SOURCE].write(src)
            except KeyboardInterrupt:
                raise
            except:
                src = overflow_fill(src, each_width)
                file_writers[SOURCE].write(src)
            if IR in file_writers:
                try:
                    if lang1_processor:
                        assert ir_processor, "ir_procesor not defined"
                        ir = overflow_fill(ir_processor.detokenize_code(ir), each_width)

                    file_writers[IR].write(ir)
                except KeyboardInterrupt:
                    raise
                except:
                    ir = overflow_fill(ir, each_width)
                    file_writers[IR].write(ir)

            try:
                if lang2_processor:
                    ref = overflow_fill(
                        lang2_processor.detokenize_code(ref), each_width
                    )
                ref = ref.replace(TOK_AVOID_NEWLINE, "\n")
                file_writers[REF].write(ref)
            except KeyboardInterrupt:
                raise
            except:
                ref = overflow_fill(ref, each_width)
                file_writers[REF].write(ref)

            for i in range(beam_size):
                hyp = hyps[i]
                out = outs[i]
                try:
                    if lang2_processor:
                        hyp = overflow_fill(
                            lang2_processor.detokenize_code(hyp), each_width
                        )
                    hyp = hyp.replace(TOK_AVOID_NEWLINE, "\n")
                    file_writers[HYPO].write(hyp)
                except KeyboardInterrupt:
                    raise
                except:
                    hyp = overflow_fill(hyp, each_width)
                    file_writers[HYPO].write(hyp)

                out = overflow_fill(out, each_width - 4)
                file_writers[OUT].write(out)

                if i == 0:
                    maximum = max(
                        len(src.split("\n")),
                        len(hyp.split("\n")),
                        len(ref.split("\n")),
                        len(out.split("\n")),
                        len(ir.split("\n")),
                    )

                    for i in range(len(src.split("\n")), maximum):
                        file_writers[SOURCE].write("\n")
                    if IR in file_writers:
                        for i in range(len(ir.split("\n")), maximum):
                            file_writers[IR].write("\n")

                    for i in range(len(hyp.split("\n")), maximum):
                        file_writers[HYPO].write("\n")
                    for i in range(len(ref.split("\n")), maximum):
                        file_writers[REF].write("\n")
                    for i in range(len(out.split("\n")), maximum):
                        file_writers[OUT].write("\n")
                else:
                    maximum = max(len(hyp.split("\n")), len(out.split("\n")))
                    for i in range(maximum - 1):
                        file_writers[SOURCE].write("\n")
                        file_writers[REF].write("\n")
                        if IR in file_writers:
                            file_writers[IR].write("\n")
                    for i in range(len(hyp.split("\n")), maximum):
                        file_writers[HYPO].write("\n")
                    for i in range(len(out.split("\n")), maximum):
                        file_writers[OUT].write("\n")
                for writer in file_writers.values():
                    writer.write("-\n")
            for writer in file_writers.values():
                writer.write("--\n\n")
    finally:
        for writer in file_writers.values():
            writer.close()

    command = f"pr -w {page_width} -m -t {src_viz} {ir_viz if ir_viz else ''} {ref_viz} {hyp_viz} {out_viz} > {hyp_viz[:-4]}"
    subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).wait()
    os.remove(src_viz)
    if src_viz != ref_viz:
        os.remove(ref_viz)
    if ir_viz is not None and Path(ir_viz).is_file():
        os.remove(ir_viz)
    os.remove(hyp_viz)
    os.remove(out_viz)


def vizualize_do_files(lang1, src_file, ref_file, hyp_file):
    lang1_processor = LangProcessor.processors[get_programming_language_name(lang1)]()
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


def overflow_fill(s, max_width):
    return "\n".join([textwrap.fill(l, max_width) for l in s.splitlines()])
