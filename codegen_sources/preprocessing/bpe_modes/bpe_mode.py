# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

TMP_EXT = ".tmp"


class BPEMode:
    """
    the base BPE mode logic for running apply_bpe and repair_bpe
    """

    # TODO add restore BPE of XLM utils into that class
    def __init__(self, ext: str, vocab_path: str, process_strings: bool) -> None:
        self.ext = ext
        self.vocab_path = vocab_path
        self.process_strings = process_strings

    def learn_bpe_file(self, file: str, ncodes: int) -> None:
        raise NotImplementedError

    def apply_bpe(self, code: str) -> str:
        raise NotImplementedError

    def apply_bpe_file(self, file: str, output: str) -> None:
        raise NotImplementedError

    def repair_bpe_for_obfuscation_line(self, line: str) -> str:
        raise NotImplementedError

    def repair_bpe_for_obfuscation_file(self, file: str, output: str) -> None:
        raise NotImplementedError
