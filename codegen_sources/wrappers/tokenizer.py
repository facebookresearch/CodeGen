# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import os
from typing import List

import fastBPE
import torch
from transformers import RobertaTokenizer

from codegen_sources.model.src.utils import restore_roberta_segmentation_string
from pathlib import Path
from codegen_sources.preprocessing.lang_processors.cpp_processor import CppProcessor
from codegen_sources.preprocessing.lang_processors.java_processor import JavaProcessor
from codegen_sources.preprocessing.lang_processors.python_processor import (
    PythonProcessor,
)
from codegen_sources.preprocessing.lang_processors.lang_processor import LangProcessor
from codegen_sources.preprocessing.lang_processors.tokenization_utils import (
    tokenize_string,
    detokenize_string,
)

JAVA_BPE_CODES = str(
    Path(__file__).parents[2].joinpath("data/bpe/cpp-java-python/codes")
)
PYTHON_BPE_CODES = JAVA_BPE_CODES


class Tokenizer:
    def __init__(
        self,
        lang,
        bpe_model,
        dico_word2id,
        dico_id2word,
        max_vocab=-1,
        max_len_single_sentence=1024,
        bos_token="</s>",
        eos_token="</s>",
        cls_token="</s>",
        sep_token="</s>",
        roberta_mode=False,
    ):

        assert all(dico_word2id[v] == k for k, v in dico_id2word.items())
        self.lang = lang
        self.bpe_model = bpe_model
        self.dico_id2word = dico_id2word
        self.dico_word2id = dico_word2id
        self.bos_token = bos_token
        self.bos_token_id = self.dico_word2id[self.bos_token]
        self.eos_token = eos_token
        self.eos_token_id = self.dico_word2id[self.eos_token]
        self.cls_token = cls_token
        self.cls_token_id = self.dico_word2id[self.cls_token]
        self.sep_token = sep_token
        self.sep_token_id = self.dico_word2id[self.sep_token]
        self.pad_token = "<pad>"
        self.pad_token_id = self.dico_word2id[self.pad_token]
        self.unk_token = "<unk>"
        self.unk_token_id = self.dico_word2id[self.unk_token]
        self.max_vocab = max_vocab
        self.max_len_single_sentence = max_len_single_sentence
        self.roberta_mode = roberta_mode
        self.roberta_tokenizer = RobertaTokenizer.from_pretrained("roberta-base")

        self.lang_precessor = LangProcessor.processors[self.lang](
            root_folder=Path(__file__).parents[2].joinpath("tree-sitter")
        )

        if max_vocab > 0:
            assert max_vocab > 1000, f"max vocab is too small"
            for i in range(max_vocab, len(dico_id2word)):
                dico_id2word[i] = self.unk_token

    def tokenize(self, input: str, is_text=False, keep_comments=True) -> List[str]:
        if is_text and not self.roberta_mode:
            code = " ".join(tokenize_string(input))
        else:
            try:
                code = " ".join(
                    self.lang_precessor.tokenize_code(
                        input,
                        keep_comments=keep_comments,
                        process_strings=not self.roberta_mode,
                    )
                )
            except ValueError as e:
                # warnings.warn(f"Error tokenizing code {input} ### {e}")
                code = input
        try:
            code = (
                " ".join(self.roberta_tokenizer.tokenize(code))
                if self.roberta_mode
                else self.bpe_model.apply([code])[0]
            )
        except UnicodeEncodeError:
            code = code.encode("utf-8", errors="replace").decode()
            code = (
                " ".join(self.roberta_tokenizer.tokenize(code))
                if self.roberta_mode
                else self.bpe_model.apply([code])[0]
            )

        if len(code) == 0:
            return []
        code = code.split(" ")
        return code

    def convert_tokens_to_ids(self, tokens: List[str]) -> List[int]:
        ids = [
            self.dico_word2id[token]
            if token in self.dico_word2id.keys()
            else self.unk_token_id
            for token in tokens
        ]
        return ids

    def decode(
        self,
        ids: List[int],
        clean_up_tokenization_spaces=False,
        one_line=None,
        text=False,
    ) -> str:
        code = " ".join([self.dico_id2word[i] for i in ids])
        if self.roberta_mode:
            code = restore_roberta_segmentation_string(code)
        else:
            code = code.replace("@@ ", "")  # restore bpe
        if text:
            return detokenize_string(code)
        code = self.lang_precessor.detokenize_code(code)
        if one_line or one_line is None:
            code = code.replace("\n", "").replace("  ", " ")
        return code

    @classmethod
    def _from_pretrained(self, model_path):
        assert os.path.exists(
            model_path
        ), f"cannot reloaded dictionnary for tokenizer, {model_path} doesnt exist."
        reloaded = torch.load(model_path)
        assert "dico_id2word" in reloaded.keys()
        assert "dico_word2id" in reloaded.keys()
        assert (
            "params" in reloaded.keys()
            and "max_vocab" in reloaded["params"].keys()
            and "max_len" in reloaded["params"].keys()
        )
        return (
            reloaded["dico_word2id"],
            reloaded["dico_id2word"],
            reloaded["params"]["max_vocab"],
            reloaded["params"]["max_len"],
        )


class JavaTokenizer(Tokenizer):
    def __init__(
        self,
        bpe_model,
        dico_word2id,
        dico_id2word,
        max_vocab=-1,
        max_len_single_sentence=1024,
        bos_token="</s>",
        eos_token="</s>",
        cls_token="</s>",
        sep_token="</s>",
    ):
        super().__init__(
            "java",
            bpe_model,
            dico_word2id,
            dico_id2word,
            max_vocab,
            max_len_single_sentence,
            bos_token,
            eos_token,
            cls_token,
            sep_token,
            roberta_mode=False,
        )

    @classmethod
    def from_pretrained(self, model_path, do_lower_case=False, cache_dir=None):
        dico_word2id, dico_id2word, max_vocab, max_len = super()._from_pretrained(
            model_path
        )
        bpe_model = fastBPE.fastBPE(JAVA_BPE_CODES)
        return JavaTokenizer(
            bpe_model=bpe_model,
            dico_word2id=dico_word2id,
            dico_id2word=dico_id2word,
            max_vocab=max_vocab,
            max_len_single_sentence=max_len,
        )


class PythonTokenizer(Tokenizer):
    def __init__(
        self,
        bpe_model,
        dico_word2id,
        dico_id2word,
        max_vocab=-1,
        max_len_single_sentence=1024,
        bos_token="</s>",
        eos_token="</s>",
        cls_token="</s>",
        sep_token="</s>",
    ):
        super().__init__(
            "python",
            bpe_model,
            dico_word2id,
            dico_id2word,
            max_vocab,
            max_len_single_sentence,
            bos_token,
            eos_token,
            cls_token,
            sep_token,
            roberta_mode=False,
        )

    @classmethod
    def from_pretrained(self, model_path, do_lower_case=False, cache_dir=None):
        dico_word2id, dico_id2word, max_vocab, max_len = super()._from_pretrained(
            model_path
        )
        bpe_model = fastBPE.fastBPE(PYTHON_BPE_CODES)
        return PythonTokenizer(
            bpe_model=bpe_model,
            dico_word2id=dico_word2id,
            dico_id2word=dico_id2word,
            max_vocab=max_vocab,
            max_len_single_sentence=max_len,
        )


class RobertaPythonTokenizer(Tokenizer):
    def __init__(
        self,
        bpe_model,
        dico_word2id,
        dico_id2word,
        max_vocab=-1,
        max_len_single_sentence=1024,
        bos_token="</s>",
        eos_token="</s>",
        cls_token="</s>",
        sep_token="</s>",
    ):
        super().__init__(
            "python",
            bpe_model,
            dico_word2id,
            dico_id2word,
            max_vocab,
            max_len_single_sentence,
            bos_token,
            eos_token,
            cls_token,
            sep_token,
            roberta_mode=True,
        )

    @classmethod
    def from_pretrained(self, model_path, do_lower_case=False, cache_dir=None):
        dico_word2id, dico_id2word, max_vocab, max_len = super()._from_pretrained(
            model_path
        )
        bpe_model = None
        return RobertaPythonTokenizer(
            bpe_model=bpe_model,
            dico_word2id=dico_word2id,
            dico_id2word=dico_id2word,
            max_vocab=max_vocab,
            max_len_single_sentence=max_len,
        )


class RobertaJavaTokenizer(Tokenizer):
    def __init__(
        self,
        bpe_model,
        dico_word2id,
        dico_id2word,
        max_vocab=-1,
        max_len_single_sentence=1024,
        bos_token="</s>",
        eos_token="</s>",
        cls_token="</s>",
        sep_token="</s>",
    ):
        super().__init__(
            "java",
            bpe_model,
            dico_word2id,
            dico_id2word,
            max_vocab,
            max_len_single_sentence,
            bos_token,
            eos_token,
            cls_token,
            sep_token,
            roberta_mode=True,
        )

    @classmethod
    def from_pretrained(self, model_path, do_lower_case=False, cache_dir=None):
        dico_word2id, dico_id2word, max_vocab, max_len = super()._from_pretrained(
            model_path
        )
        bpe_model = None
        return RobertaJavaTokenizer(
            bpe_model=bpe_model,
            dico_word2id=dico_word2id,
            dico_id2word=dico_id2word,
            max_vocab=max_vocab,
            max_len_single_sentence=max_len,
        )
