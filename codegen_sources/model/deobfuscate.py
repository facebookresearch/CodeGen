# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#


import os
import argparse
from pathlib import Path
import sys
import fastBPE
import torch
from codegen_sources.model.src.logger import create_logger
from codegen_sources.preprocessing.lang_processors.cpp_processor import CppProcessor
from codegen_sources.preprocessing.lang_processors.java_processor import JavaProcessor
from codegen_sources.preprocessing.lang_processors.python_processor import (
    PythonProcessor,
)
from codegen_sources.model.src.utils import restore_roberta_segmentation_sentence
from codegen_sources.preprocessing.bpe_modes.fast_bpe_mode import FastBPEMode
from codegen_sources.preprocessing.bpe_modes.roberta_bpe_mode import RobertaBPEMode
from codegen_sources.preprocessing.lang_processors.lang_processor import LangProcessor
from codegen_sources.model.src.data.dictionary import (
    Dictionary,
    BOS_WORD,
    EOS_WORD,
    PAD_WORD,
    UNK_WORD,
    MASK_WORD,
)
from codegen_sources.model.src.model import build_model
from codegen_sources.model.src.utils import AttrDict

SUPPORTED_LANGUAGES = ["java", "python"]

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
        "--lang",
        type=str,
        default="",
        help=f"Code language, should be either {', '.join(SUPPORTED_LANGUAGES[:-1])} or {SUPPORTED_LANGUAGES[-1]}",
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

    return parser


class Deobfuscator:
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

    def deobfuscate(
        self, input, lang, n=1, beam_size=1, sample_temperature=None, device="cuda:0",
    ):

        # Build language processors
        assert lang, lang in SUPPORTED_LANGUAGES

        lang_processor = LangProcessor.processors[lang](
            root_folder=Path(__file__).parents[2].joinpath("tree-sitter")
        )
        obfuscator = lang_processor.obfuscate_code
        tokenizer = lang_processor.tokenize_code

        lang1 = lang + "_obfuscated"
        lang2 = lang + "_dictionary"
        lang1_id = self.reloaded_params.lang2id[lang1]
        lang2_id = self.reloaded_params.lang2id[lang2]

        assert (
            lang1 in self.reloaded_params.lang2id.keys()
        ), f"{lang1} should be in {self.reloaded_params.lang2id.keys()}"
        assert (
            lang2 in self.reloaded_params.lang2id.keys()
        ), f"{lang2} should be in {self.reloaded_params.lang2id.keys()}"

        print("Original Code:")
        print(input)

        input = obfuscator(input)[0]
        print("Obfuscated Code:")
        print(input)

        with torch.no_grad():
            # Convert source code to ids
            tokens = [t for t in tokenizer(input)]
            print(f"Tokenized {lang} function:")
            print(tokens)
            tokens = self.bpe_model.apply_bpe(" ".join(tokens))
            tokens = self.bpe_model.repair_bpe_for_obfuscation_line(tokens)
            print(f"BPE {params.lang} function:")
            print(tokens)
            tokens = ["</s>"] + tokens.split() + ["</s>"]
            input = " ".join(tokens)

            # Create torch batch
            len1 = len(input.split())
            len1 = torch.LongTensor(1).fill_(len1).to(device)
            x1 = torch.LongTensor([self.dico.index(w) for w in input.split()]).to(
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
            if beam_size == 1:
                x2, len2 = self.decoder.generate(
                    enc1,
                    len1,
                    lang2_id,
                    max_len=int(
                        min(self.reloaded_params.max_len, 3 * len1.max().item() + 10)
                    ),
                    sample_temperature=sample_temperature,
                )
            else:
                x2, len2, _ = self.decoder.generate_beam(
                    enc1,
                    len1,
                    lang2_id,
                    max_len=int(
                        min(self.reloaded_params.max_len, 3 * len1.max().item() + 10)
                    ),
                    early_stopping=False,
                    length_penalty=1.0,
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
            results = []
            for t in tok:
                results.append(t)
            return results


if __name__ == "__main__":
    # generate parser / parse parameters
    parser = get_parser()
    params = parser.parse_args()

    # check parameters
    assert os.path.isfile(
        params.model_path
    ), f"The path to the model checkpoint is incorrect: {params.model_path}"
    assert os.path.isfile(
        params.BPE_path
    ), f"The path to the BPE tokens is incorrect: {params.BPE_path}"
    assert (
        params.lang in SUPPORTED_LANGUAGES
    ), f"The source language should be in {SUPPORTED_LANGUAGES}."

    # Initialize translator
    deobfuscator = Deobfuscator(params.model_path, params.BPE_path)

    # read input code from stdin
    src_sent = []
    input = sys.stdin.read().strip()

    with torch.no_grad():
        output = deobfuscator.deobfuscate(
            input, lang=params.lang, beam_size=params.beam_size,
        )

    for out in output:
        print("=" * 20)
        print(out)
