# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from pathlib import Path

import sentencepiece as spm  # type: ignore

from codegen_sources.preprocessing.tests.obfuscation.utils import diff_tester

MODEL_PATH = (
    Path(__file__)
    .parents[4]
    .joinpath(
        "data",
        "bpe",
        "sentencepiece",
        "sentencepiece_64k",
        "spm_model_64k_1M_whitespace_only_pieces.model",
    )
    .absolute()
)
sp = spm.SentencePieceProcessor(model_file=str(MODEL_PATH))

FUNC_EX = """from src.tokenize import _tok
@decorated
def func1(a):
    assert isinstance(a, int)
    a+=1
    return a"""


def test_sp_tokenizer() -> None:
    pieces = sp.encode_as_pieces(FUNC_EX)
    diff_tester(
        " ".join(
            [
                "▁from",
                "▁src",
                ".",
                "tokenize",
                "▁import",
                "▁_",
                "tok",
                "<0x0A>",
                "@",
                "decorated",
                "<0x0A>",
                "def",
                "▁func",
                "1",
                "(",
                "a",
                "):",
                "<0x0A>",
                "▁▁▁▁assert",
                "▁isinstance",
                "(",
                "a",
                ",",
                "▁int",
                ")",
                "<0x0A>",
                "▁▁▁▁a",
                "+=",
                "1",
                "<0x0A>",
                "▁▁▁▁return",
                "▁a",
            ]
        ),
        " ".join(pieces),
        split="<0x0A>",
    )


def test_sp_tokenizer_invertible() -> None:
    assert sp.decode(sp.encode(FUNC_EX)) == FUNC_EX
