# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from pathlib import Path
import codegen_sources.utils.typing as tp

TMP_EXT = ".tmp"


class BPEMode:
    """
    the base BPE mode logic for running apply_bpe and repair_bpe
    """

    # TODO add restore BPE of XLM utils into that class
    def __init__(
        self, ext: str, vocab_path: tp.Optional[tp.PathLike], process_strings: bool
    ) -> None:
        self.ext = ext
        self.vocab_path = None if vocab_path is None else Path(vocab_path)
        self.process_strings = process_strings

    def learn_bpe_file(self, file: str, ncodes: int) -> None:
        raise NotImplementedError

    def apply_bpe(self, code: str) -> str:
        raise NotImplementedError

    def apply_bpe_file(self, file: tp.PathLike, output: tp.PathLike) -> None:
        raise NotImplementedError

    @staticmethod
    def repair_bpe_for_obfuscation_line(line: str) -> str:
        raise NotImplementedError

    def repair_bpe_for_obfuscation_file(
        self, file: tp.PathLike, output: tp.PathLike
    ) -> None:
        raise NotImplementedError
