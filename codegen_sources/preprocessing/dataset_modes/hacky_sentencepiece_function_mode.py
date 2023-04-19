# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
from itertools import chain
from logging import getLogger
from pathlib import Path

import codegen_sources
import codegen_sources.utils.typing as tp
from codegen_sources.preprocessing.dataset_modes.dataset_mode import (
    DatasetMode,
    DATASET_SPLITS,
)
from codegen_sources.preprocessing.lang_processors import LangProcessor
from codegen_sources.preprocessing.obfuscation.utils_deobfuscation import REPLACE_DICT
from codegen_sources.preprocessing.timeout import timeout
from codegen_sources.preprocessing.utils import (
    is_valid_file,
    create_symlink,
)
import sentencepiece as spm  # type: ignore

# TODO: add sentencepiece as a BPEMode instead

# SP_PATH = "/checkpoint/broz/data/sentencepiece_model_training/spm_model_64k_1M_whitespace_only_pieces_2"
# SP_PATH = "/checkpoint/broz/data/sentencepiece_model_training/spm_model_32k_1M_whitespace_only_pieces_2"
SP_PATH = (
    Path(codegen_sources.__file__).resolve().parents[1]
    / "data"
    / "bpe"
    / "sentencepiece"
    / "sentencepiece_32k_v2"
)

MONOLINGUAL_SUFFIXES = ["sa", "cl"]
logger = getLogger()
MODEL_PATH = SP_PATH / "model"
sp = spm.SentencePieceProcessor(model_file=str(MODEL_PATH))  # type: ignore


class SentencePieceFunctionMode(DatasetMode):
    """
    """

    def __init__(
        self,
        folder,
        languages,
        bpe,
        processed_lines: tp.Optional[tp.Set] = None,
        nb_train_split: int = 8,
        keep_comments: bool = False,
        repo_split: bool = True,
    ):
        super().__init__(
            suffixes=MONOLINGUAL_SUFFIXES,
            folder=folder,
            languages=languages,
            bpe=bpe,
            parallel_dataset=False,
            processed_lines=processed_lines,
            nb_train_split=nb_train_split,
            keep_comments=keep_comments,
            repo_split=repo_split,
        )
        self.bpe.vocab_path = SP_PATH / "vocab"

    def extract_data_for_line(
        self,
        line_id: str,
        json_line: dict,
        process_strings: bool,
        lang_processor: LangProcessor,
    ):
        default_return = line_id, None, None
        if "content" not in json_line:
            return default_return
        content = json_line["content"]
        content = content.replace("\r", "")
        for k, v in REPLACE_DICT.items():
            content = content.replace(k, v)

        try:
            f_standalone, f_class = lang_processor.extract_functions(
                content, tokenized=False
            )
            tokenize = sp.encode_as_pieces  # type: ignore
            f_standalone = [" ".join(tokenize(x)) for x in f_standalone]
            f_class = [" ".join(tokenize(x)) for x in f_class]

        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write(
                f"error {type(e)} {e} tokenizing and extracting functions\n"
            )
            return default_return
        return (
            line_id,
            json_line["repo_name"],
            {"sa": f_standalone, "cl": f_class},
        )

    def _learn_bpe(
        self, ncodes: int, executor: tp.Optional[tp.ExecutorLike] = None
    ) -> None:
        return

    def _get_vocab(self, executor: tp.Optional[tp.ExecutorLike] = None) -> None:
        return

    def apply_bpe(
        self,
        executor: tp.OptExecutor = None,
        local_parallelism: tp.Optional[int] = None,
    ) -> None:
        # BPE already applied at tokenization time
        for f in chain(
            *[
                self.folder.glob(f"{lang}.{split}.*.*tok")
                for split in DATASET_SPLITS
                for lang in self.languages
            ]
        ):
            if not is_valid_file(f):
                logger.warning(f"{f} is not a valid file, cannot to apply BPE on it.")
            elif not is_valid_file(f.with_suffix(self.bpe.ext)):
                logger.info(f"Symlinks instead of BPE on {f} ...")
                create_symlink(f, f.with_suffix(".bpe"))
        logger.info("BPE done.")
