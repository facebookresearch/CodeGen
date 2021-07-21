# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from codegen_sources.preprocessing.bpe_modes.bpe_mode import BPEMode
from codegen_sources.preprocessing.obfuscation.utils_deobfuscation import (
    OBFUSCATED_PREFIXES,
)

import os
from pathlib import Path
from transformers import RobertaTokenizer
import re
import logging

logger = logging.getLogger()


class RobertaBPEMode(BPEMode):
    """
    apply the BPE with the roberta logic
    """

    def __init__(self) -> None:
        vocab_path = str(
            Path(__file__).parents[3].joinpath("data/bpe/roberta-base-vocab")
        )
        logger.info(
            f"Roberta BPE mode use Roberta pretrained codes and vocab {vocab_path}."
        )
        super().__init__(ext=".bperob", vocab_path=vocab_path, process_strings=False)

    def learn_bpe_file(self, file: str, ncodes: int):
        logger.warning("Roberta BPE codes don't need to be trained. Use default ones.")

    def get_vocab_file(self, file, nvocab=64000):
        logger.warning("Roberta BPE vocab doesn't need to be trained. Use default one.")

    def apply_bpe(self, code: str):
        tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
        lines = code.split("\n")
        return "\n".join(
            [" ".join(tokenizer._tokenize(line.strip())) for line in lines]
        )

    def apply_bpe_file(self, file: str, output: str):
        assert os.path.exists(
            file
        ), f"cannot apply bpe on file {file}, it doesnt exists."
        if output is None:
            output = file.replace(".tok", ".rob-bpe")
        with open(file, encoding="utf-8") as f:
            code = f.read()
        with open(output, "w", encoding="utf-8") as f:
            f.write(self.apply_bpe(code))

    def repair_bpe_for_obfuscation_line(self, line: str):
        line = line.replace("CLASS _ ", "CLASS_")
        line = line.replace("FUN C _ ", "FUNC_")
        line = line.replace("V AR _ ", "VAR_")
        for prefix in OBFUSCATED_PREFIXES:
            n_replacements = 1
            line = line.replace(f"Ġ{prefix}", f"Ġ {prefix}")
            while n_replacements > 0:
                line, n_replacements = re.subn(
                    f"({prefix}[0-9]+) ([0-9]+)", r"\1\2", line
                )
        return line

    def repair_bpe_for_obfuscation_file(self, file: str, output: str):
        output_file = open(output, "w", encoding="utf-8")
        with open(str(file), "r", encoding="utf-8") as input_file:
            for line in input_file:
                line = self.repair_bpe_for_obfuscation_line(line)
                output_file.write(line)
