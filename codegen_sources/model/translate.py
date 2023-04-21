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
import typing as tp
from pathlib import Path
import sys
import torch
from codegen_sources.model.src.logger import create_logger
from codegen_sources.model.src.data.dictionary import (
    Dictionary,
    BOS_WORD,
    EOS_WORD,
    PAD_WORD,
    UNK_WORD,
    MASK_WORD,
)
from codegen_sources.model.src.utils import bool_flag
from codegen_sources.model.src.constants import SUPPORTED_LANGUAGES_FOR_TESTS
from codegen_sources.model.src.model import build_model
from codegen_sources.model.src.utils import AttrDict
import codegen_sources.dataloaders.transforms as transf


SUPPORTED_LANGUAGES = list(SUPPORTED_LANGUAGES_FOR_TESTS) + ["ir"]
logger = create_logger(None, 0)


def get_params():
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
    parser.add_argument(
        "--gpu", type=bool_flag, default=True, help="input path",
    )
    parser.add_argument(
        "--efficient_attn",
        type=str,
        default=None,
        choices=["None", "flash", "cutlass", "fctls_bflsh", "auto"],
        help="If set, uses efficient attention from xformers.",
    )
    parameters = parser.parse_args()
    if parameters.efficient_attn == "None":
        parameters.efficient_attn = None

    return parameters


class Translator:
    def __init__(self, model_path, BPE_path, gpu=True, efficient_attn=None) -> None:
        self.gpu = gpu
        # reload model
        reloaded = torch.load(model_path, map_location="cpu")
        # change params of the reloaded model so that it will
        # relaod its own weights and not the MLM or DOBF pretrained model
        reloaded["params"]["reload_model"] = ",".join([str(model_path)] * 2)
        reloaded["params"]["lgs_mapping"] = ""
        reloaded["params"]["reload_encoder_for_decoder"] = False
        self.reloaded_params = AttrDict(reloaded["params"])
        self.reloaded_params["efficient_attn"] = efficient_attn
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
        encoder, decoder = build_model(self.reloaded_params, self.dico, self.gpu)
        self.encoder = encoder[0]
        self.decoder = decoder[0]
        if gpu:
            self.encoder.cuda()
            self.decoder.cuda()
        self.encoder.eval()
        self.decoder.eval()

        # reload bpe
        if (
            self.reloaded_params.get("roberta_mode", False)
            or self.reloaded_params.get("tokenization_mode", "") == "roberta"
        ):
            self.bpe_transf: transf.BpeBase = transf.RobertaBpe()
            raise ValueError("This part has not be tested thoroughly yet")
        else:
            self.bpe_transf = transf.FastBpe(code_path=Path(BPE_path).absolute())

    def translate(
        self,
        input_code,
        lang1: str,
        lang2: str,
        suffix1: str = "_sa",
        suffix2: str = "_sa",
        n: int = 1,
        beam_size: int = 1,
        sample_temperature=None,
        device=None,
        tokenized=False,
        detokenize: bool = True,
        max_tokens: tp.Optional[int] = None,
        length_penalty: float = 0.5,
        max_len: tp.Optional[int] = None,
    ):
        if device is None:
            device = "cuda:0" if self.gpu else "cpu"

        # Build language processors
        assert lang1 in SUPPORTED_LANGUAGES, lang1
        assert lang2 in SUPPORTED_LANGUAGES, lang2
        bpetensorizer = transf.BpeTensorizer()
        bpetensorizer.dico = self.dico  # TODO: hacky
        in_pipe: transf.Transform[tp.Any, torch.Tensor] = self.bpe_transf.pipe(
            bpetensorizer
        )
        out_pipe = in_pipe
        if not tokenized:
            in_pipe = transf.CodeTokenizer(lang1).pipe(in_pipe)
        if detokenize:
            out_pipe = transf.CodeTokenizer(lang2).pipe(out_pipe)

        lang1 += suffix1
        lang2 += suffix2
        avail_langs = list(self.reloaded_params.lang2id.keys())
        for lang in [lang1, lang2]:
            if lang not in avail_langs:
                raise ValueError(f"{lang} should be in {avail_langs}")

        with torch.no_grad():

            lang1_id = self.reloaded_params.lang2id[lang1]
            lang2_id = self.reloaded_params.lang2id[lang2]

            # Create torch batch
            x1 = in_pipe.apply(input_code).to(device)[:, None]
            size = x1.shape[0]
            len1 = torch.LongTensor(1).fill_(size).to(device)
            if max_tokens is not None and size > max_tokens:
                logger.info(f"Ignoring long input sentence of size {size}")
                return [f"Error: input too long: {size}"] * max(n, beam_size)
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
                tok.append(out_pipe.revert(x2[:, i]))
            return tok


if __name__ == "__main__":
    # generate parser / parse parameters
    params = get_params()

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
    translator = Translator(
        params.model_path, params.BPE_path, params.gpu, params.efficient_attn
    )

    # read input code from stdin
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
