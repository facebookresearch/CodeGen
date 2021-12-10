# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
# Translate sentences from the input stream.
# The model will be faster is sentences are sorted by length.
# Input sentences must have the same tokenization and BPE codes than the ones used in the model.
#


import os
import argparse
from pathlib import Path
import sys
import torch
from codegen_sources.model.src.logger import create_logger
from codegen_sources.preprocessing.lang_processors.cpp_processor import CppProcessor
from codegen_sources.preprocessing.lang_processors.java_processor import JavaProcessor
from codegen_sources.preprocessing.lang_processors.python_processor import (
    PythonProcessor,
)
from codegen_sources.preprocessing.lang_processors.lang_processor import LangProcessor
from codegen_sources.preprocessing.bpe_modes.fast_bpe_mode import FastBPEMode
from codegen_sources.preprocessing.bpe_modes.roberta_bpe_mode import RobertaBPEMode
from codegen_sources.model.src.data.dictionary import (
    Dictionary,
    BOS_WORD,
    EOS_WORD,
    PAD_WORD,
    UNK_WORD,
    MASK_WORD,
)
from codegen_sources.model.src.utils import restore_roberta_segmentation_sentence
from codegen_sources.model.src.model import build_model
from codegen_sources.model.src.utils import AttrDict, TREE_SITTER_ROOT

SUPPORTED_LANGUAGES = ["cpp", "java", "python"]

logger = create_logger(None, 0)


def get_parser():
    """
    Generate a parameters parser.
    """
    # parse parameters
    parser = argparse.ArgumentParser(description="Translate sentences")

    # model
    parser.add_argument("--model_path", type=str, default="", help="Model path")
    parser.add_argument(
        "--src_lang",
        type=str,
        default="",
        help=f"Source language, should be either {', '.join(SUPPORTED_LANGUAGES[:-1])} or {SUPPORTED_LANGUAGES[-1]}",
    )
    parser.add_argument(
        "--tgt_lang",
        type=str,
        default="",
        help=f"Target language, should be either {', '.join(SUPPORTED_LANGUAGES[:-1])} or {SUPPORTED_LANGUAGES[-1]}",
    )
    parser.add_argument(
        "--BPE_path",
        type=str,
        default=str(
            Path(__file__).parents[2].joinpath("data/bpe/cpp-java-python/codes")
        ),
        help="Path to BPE codes.",
    )
    parser.add_argument(
        "--beam_size",
        type=int,
        default=1,
        help="Beam size. The beams will be printed in order of decreasing likelihood.",
    )
    parser.add_argument(
        "--input", type=str, default=None, help="input path",
    )

    return parser


class Translator:
    def __init__(self, model_path, BPE_path):
        # reload model
        reloaded = torch.load(model_path, map_location="cpu")
        # change params of the reloaded model so that it will
        # relaod its own weights and not the MLM or DOBF pretrained model
        reloaded["params"]["reload_model"] = ",".join([model_path] * 2)
        reloaded["params"]["lgs_mapping"] = ""
        reloaded["params"]["reload_encoder_for_decoder"] = False
        self.reloaded_params = AttrDict(reloaded["params"])

        # build dictionary / update parameters
        self.dico = Dictionary(
            reloaded["dico_id2word"], reloaded["dico_word2id"], reloaded["dico_counts"]
        )
        assert self.reloaded_params.n_words == len(self.dico)
        assert self.reloaded_params.bos_index == self.dico.index(BOS_WORD)
        assert self.reloaded_params.eos_index == self.dico.index(EOS_WORD)
        assert self.reloaded_params.pad_index == self.dico.index(PAD_WORD)
        assert self.reloaded_params.unk_index == self.dico.index(UNK_WORD)
        assert self.reloaded_params.mask_index == self.dico.index(MASK_WORD)

        # build model / reload weights (in the build_model method)
        encoder, decoder = build_model(self.reloaded_params, self.dico)
        self.encoder = encoder[0]
        self.decoder = decoder[0]
        self.encoder.cuda()
        self.decoder.cuda()
        self.encoder.eval()
        self.decoder.eval()

        # reload bpe
        if getattr(self.reloaded_params, "roberta_mode", False):
            self.bpe_model = RobertaBPEMode()
        else:
            self.bpe_model = FastBPEMode(
                codes=os.path.abspath(BPE_path), vocab_path=None
            )

    def translate(
        self,
        input_code,
        lang1,
        lang2,
        suffix1="_sa",
        suffix2="_sa",
        n=1,
        beam_size=1,
        sample_temperature=None,
        device="cuda:0",
        tokenized=False,
        detokenize=True,
        max_tokens=None,
        length_penalty=0.5,
        max_len=None,
    ):

        # Build language processors
        assert lang1 in SUPPORTED_LANGUAGES, lang1
        assert lang2 in SUPPORTED_LANGUAGES, lang2
        src_lang_processor = LangProcessor.processors[lang1](
            root_folder=TREE_SITTER_ROOT
        )
        tokenizer = src_lang_processor.tokenize_code
        tgt_lang_processor = LangProcessor.processors[lang2](
            root_folder=TREE_SITTER_ROOT
        )
        detokenizer = tgt_lang_processor.detokenize_code

        lang1 += suffix1
        lang2 += suffix2

        assert (
            lang1 in self.reloaded_params.lang2id.keys()
        ), f"{lang1} should be in {self.reloaded_params.lang2id.keys()}"
        assert (
            lang2 in self.reloaded_params.lang2id.keys()
        ), f"{lang2} should be in {self.reloaded_params.lang2id.keys()}"

        with torch.no_grad():

            lang1_id = self.reloaded_params.lang2id[lang1]
            lang2_id = self.reloaded_params.lang2id[lang2]

            # Convert source code to ids
            if tokenized:
                tokens = input_code.strip().split()
            else:
                tokens = [t for t in tokenizer(input_code)]
            print(f"Tokenized {lang1} function:")
            print(tokens)
            tokens = self.bpe_model.apply_bpe(" ".join(tokens)).split()
            tokens = ["</s>"] + tokens + ["</s>"]
            input_code = " ".join(tokens)
            if max_tokens is not None and len(input_code.split()) > max_tokens:
                logger.info(
                    f"Ignoring long input sentence of size {len(input_code.split())}"
                )
                return [f"Error: input too long: {len(input_code.split())}"] * max(
                    n, beam_size
                )

            # Create torch batch
            len1 = len(input_code.split())
            len1 = torch.LongTensor(1).fill_(len1).to(device)
            x1 = torch.LongTensor([self.dico.index(w) for w in input_code.split()]).to(
                device
            )[:, None]
            langs1 = x1.clone().fill_(lang1_id)

            # Encode
            enc1 = self.encoder("fwd", x=x1, lengths=len1, langs=langs1, causal=False)
            enc1 = enc1.transpose(0, 1)
            if n > 1:
                enc1 = enc1.repeat(n, 1, 1)
                len1 = len1.expand(n)

            # Decode
            if max_len is None:
                max_len = int(
                    min(self.reloaded_params.max_len, 3 * len1.max().item() + 10)
                )
            if beam_size == 1:
                x2, len2 = self.decoder.generate(
                    enc1,
                    len1,
                    lang2_id,
                    max_len=max_len,
                    sample_temperature=sample_temperature,
                )
            else:
                x2, len2, _ = self.decoder.generate_beam(
                    enc1,
                    len1,
                    lang2_id,
                    max_len=max_len,
                    early_stopping=False,
                    length_penalty=length_penalty,
                    beam_size=beam_size,
                )

            # Convert out ids to text
            tok = []
            for i in range(x2.shape[1]):
                wid = [self.dico[x2[j, i].item()] for j in range(len(x2))][1:]
                wid = wid[: wid.index(EOS_WORD)] if EOS_WORD in wid else wid
                if getattr(self.reloaded_params, "roberta_mode", False):
                    tok.append(restore_roberta_segmentation_sentence(" ".join(wid)))
                else:
                    tok.append(" ".join(wid).replace("@@ ", ""))
            if not detokenize:
                return tok
            results = []
            for t in tok:
                results.append(detokenizer(t))
            return results


if __name__ == "__main__":
    # generate parser / parse parameters
    parser = get_parser()
    params = parser.parse_args()

    # check parameters
    assert os.path.isfile(
        params.model_path
    ), f"The path to the model checkpoint is incorrect: {params.model_path}"
    assert params.input is None or os.path.isfile(
        params.input
    ), f"The path to the input file is incorrect: {params.input}"
    assert os.path.isfile(
        params.BPE_path
    ), f"The path to the BPE tokens is incorrect: {params.BPE_path}"
    assert (
        params.src_lang in SUPPORTED_LANGUAGES
    ), f"The source language should be in {SUPPORTED_LANGUAGES}."
    assert (
        params.tgt_lang in SUPPORTED_LANGUAGES
    ), f"The target language should be in {SUPPORTED_LANGUAGES}."

    # Initialize translator
    translator = Translator(params.model_path, params.BPE_path)

    # read input code from stdin
    src_sent = []
    input = (
        open(params.input).read().strip()
        if params.input is not None
        else sys.stdin.read().strip()
    )

    print(f"Input {params.src_lang} function:")
    print(input)
    with torch.no_grad():
        output = translator.translate(
            input,
            lang1=params.src_lang,
            lang2=params.tgt_lang,
            beam_size=params.beam_size,
        )

    print(f"Translated {params.tgt_lang} function:")
    for out in output:
        print("=" * 20)
        print(out)
