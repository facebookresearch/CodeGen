# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from pathlib import Path
import subprocess
from codegen_sources.preprocessing.obfuscation.utils_deobfuscation import (
    OBFUSCATED_PREFIXES,
)
from codegen_sources.preprocessing.bpe_modes.bpe_mode import BPEMode
import re
from logging import getLogger
import fastBPE

FAST = str(Path(__file__).parents[3].joinpath("fastBPE/fast"))

logger = getLogger()


class FastBPEMode(BPEMode):
    """
    apply the BPE with the fast BPE logic
    """

    def __init__(self, vocab_path: str, codes: str, use_vocab: bool = False):
        super().__init__(ext=".bpe", vocab_path=vocab_path, process_strings=True)
        assert vocab_path is None or codes is not None
        if codes is None or codes == "None":
            self.codes = None
            self.vocab_path = None
        else:
            self.codes = Path(codes)
            if self.vocab_path is not None:
                self.vocab_path = Path(vocab_path)
            else:
                self.vocab_path = None
        self.use_vocab = use_vocab

    def learn_bpe_file(self, file: str, ncodes: int):
        if ncodes > 50000:
            logger.warning(
                f"Number of codes is very large: {ncodes}. Usually we chose ncodes < 50000."
            )
        process = subprocess.run(
            f"{FAST} learnbpe {ncodes} {file} > {self.codes} ",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert (
            process.returncode == 0 and Path(f"{self.codes}").is_file
        ), f"failed to learn bpe on {file}, command: {FAST} learnbpe {ncodes} {file} > {self.codes}"

    def get_vocab_file(self, file, nvocab=64000):
        process = subprocess.run(
            f"{FAST} getvocab {file} > {str(self.vocab_path)}.all",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        process2 = subprocess.run(
            f"head -n {nvocab} {str(self.vocab_path)}.all > {str(self.vocab_path)}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert (
            self.vocab_path.is_file
            and process.returncode == 0
            and process2.returncode == 0
        ), f"failed to get vocab for {file}, command: {FAST} getvocab {file} > {str(self.vocab_path)}.all & head -n nvocab {str(self.vocab_path)}.all > {str(self.vocab_path)}"

    def apply_bpe(self, code: str):
        bpe_model = fastBPE.fastBPE(str(self.codes))
        assert isinstance(code, str)
        return " ".join(bpe_model.apply(code.split()))

    def apply_bpe_file(self, file: str, output: str):
        if output is None:
            output = file + self.ext
        vocab = self.vocab_path if self.vocab_path is not None else ""
        process = subprocess.run(
            f"{FAST} applybpe {output} {file} {self.codes} {vocab if self.use_vocab else ''}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert (
            Path(output).is_file and process.returncode == 0
        ), f"failed to apply bpe on {file}, command: \n {FAST} applybpe {output} {file} {self.codes} {vocab if self.use_vocab else ''}"

    def repair_bpe_for_obfuscation_line(self, line: str):
        for prefix in OBFUSCATED_PREFIXES:
            line = re.sub(
                f'{"(@@ )?".join(prefix)}(@@ )?([0-9]+($| ))',
                f"{prefix}\\{len(prefix)+1}",
                line,
            )
            n_replacements = 1
            while n_replacements > 0:
                line, n_replacements = re.subn(
                    f"({prefix}[0-9]+)@@ ([0-9]+)", r"\1\2", line
                )
        return line

    def repair_bpe_for_obfuscation_file(self, file: str, output: str):
        output_file = open(output, "w", encoding="utf-8")
        with open(str(file), "r", encoding="utf-8") as input_file:
            for line in input_file:
                line = self.repair_bpe_for_obfuscation_line(line)
                output_file.write(line)
