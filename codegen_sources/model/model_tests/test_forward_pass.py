# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import typing as tp
from pathlib import Path

import numpy
import pytest
import requests
import torch

from ..src.data.dictionary import (
    BOS_WORD,
    EOS_WORD,
    PAD_WORD,
    UNK_WORD,
    MASK_WORD,
    Dictionary,
)
from ..src.model import build_model
from ..src.utils import AttrDict, batch_sentences
import codegen_sources.dataloaders.transforms as transf
import codegen_sources

TOLERANCE = 1e-5
OUTPUT_DELIMITER = """Translated %s function:
===================="""

TRANSCODER_MODEL_1_URL = "https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/TransCoder_model_1.pth"
ROOT_FOLDER = Path(__file__).parents[3]
model_folder = ROOT_FOLDER.joinpath("data", "sample_model")
model_folder.mkdir(exist_ok=True)
MODEL_PATH = model_folder.joinpath("TransCoder_model_1.pth")

if not MODEL_PATH.exists():
    r = requests.get(TRANSCODER_MODEL_1_URL, allow_redirects=True)
    open(MODEL_PATH, "wb").write(r.content)


@pytest.mark.parametrize(
    "efficient_attn", (None, "cutlass", "fctls_bflsh", "auto")
)  # flash attention only works on A100
def test_reload_and_run(efficient_attn) -> None:
    BPE_path: Path = Path(codegen_sources.__file__).parents[1].resolve().joinpath(
        "data/bpe/cpp-java-python/codes"
    )
    gpu = torch.cuda.device_count() > 0
    if not gpu and efficient_attn is not None:
        print("Skipping test: xformers does not run on CPU")
        return
    device = "cuda:0" if gpu else "cpu"
    decoder, encoder, in_pipe, lang2id = reload_model(BPE_path, efficient_attn, gpu)

    lang1 = "cpp"
    input_code = """int factorial ( int n ) {
  if ( n > 1 ) return n * factorial ( n - 1 ) ;
  else return 1 ;
}"""
    in_pipe = transf.CodeTokenizer(lang1).pipe(in_pipe)
    x1 = in_pipe.apply(input_code).to(device)[:, None]
    size = x1.shape[0]
    len1 = torch.LongTensor(1).fill_(size).to(device)
    lang1_id = lang2id[lang1 + "_sa"]
    langs1 = x1.clone().fill_(lang1_id)

    # Encode
    enc1 = encoder("fwd", x=x1, lengths=len1, langs=langs1, causal=False)
    assert abs(enc1.mean().item() + 0.0388823039829731) < TOLERANCE, enc1.mean().item()
    enc1 = enc1.transpose(0, 1)
    print(enc1)

    lang2 = "python"
    output_code = """def factorial ( n ) :
    if n > 1 :
        return n * factorial ( n - 1 )
    else :
        return 1
"""
    dec2, x2, len2 = decode(
        output_code, enc1, len1, lang2, lang2id, in_pipe, decoder, device
    )
    assert (
        abs(dec2.mean().item() + 0.05856532230973244) < TOLERANCE
    ), "Decoder values changed"
    assert abs(dec2[0, 0, 0].item() + 0.5106964111328125) < TOLERANCE * 10
    assert abs(dec2[-1, -1, -1].item() + 0.2060123234987259) < TOLERANCE * 10

    loss = get_loss(x2, len2, dec2, decoder)
    assert abs(loss.item() - 2.666358232498169) < TOLERANCE, loss.item()

    output_code_2 = """def sum(a, b):
    return a + b
    """
    dec2_2, x2_2, len2_2 = decode(
        output_code_2, enc1, len1, lang2, lang2id, in_pipe, decoder, device
    )
    loss = get_loss(x2_2, len2_2, dec2_2, decoder)
    assert abs(loss.item() - 4.038794040679932) < TOLERANCE


@pytest.mark.parametrize(
    "efficient_attn", (None,)
)  # flash attention only works on A100
# Custom attention bias and padding are not supported by xformers right now
def test_reload_and_run_with_padding(efficient_attn) -> None:
    BPE_path: Path = Path(codegen_sources.__file__).parents[1].resolve().joinpath(
        "data/bpe/cpp-java-python/codes"
    )
    gpu = torch.cuda.device_count() > 0
    if not gpu and efficient_attn is not None:
        print("Skipping test: xformers does not run on CPU")
        return
    device = "cuda:0" if gpu else "cpu"
    decoder, encoder, in_pipe, lang2id = reload_model(BPE_path, efficient_attn, gpu)

    lang1 = "cpp"
    input_code = """int factorial ( int n ) {
  if ( n > 1 ) return n * factorial ( n - 1 ) ;
  else return 1 ;
}"""
    longer_code = """// This is an implementation of the factorial function using the int type
    int longer_factorial_function ( int input_integer ) {
  if ( input_integer > 1 ) return input_integer * factorial ( input_integer - 1 ) ;
  else return 1 ;
}"""
    in_pipe = transf.CodeTokenizer(lang1).pipe(in_pipe)
    x1, len1 = batch_sentences(
        [
            numpy.array(in_pipe.apply(input_code))[1:-1],
            numpy.array(in_pipe.apply(longer_code))[1:-1],
        ],
        eos_index=encoder.dico.eos_index,
        pad_index=encoder.dico.pad_index,
    )
    x1, len1 = x1.to(device), len1.to(device)
    lang1_id = lang2id[lang1 + "_sa"]
    langs1 = x1.clone().fill_(lang1_id)

    # Encode
    enc1 = encoder("fwd", x=x1, lengths=len1, langs=langs1, causal=False)
    # check first element did not change
    assert (
        abs(enc1[: len1[0].item(), 0, :].mean().item() + 0.0388823039829731) < TOLERANCE
    ), enc1.mean().item()
    assert abs(enc1.mean().item() + 0.0337064266204834) < TOLERANCE, enc1.mean().item()
    enc1 = enc1.transpose(0, 1)
    print(enc1)

    lang2 = "python"
    output_code = """def factorial ( n ) :
    if n > 1 :
        return n * factorial ( n - 1 )
    else :
        return 1

"""
    output_code_longer = """def longer_factorial_function ( input_integer ) :
        if input_integer > 1 :
            return input_integer * factorial ( input_integer - 1 )
        else :
            return 1

    """
    dec2, x2, len2 = decode(
        [output_code, output_code_longer],
        enc1,
        len1,
        lang2,
        lang2id,
        in_pipe,
        decoder,
        device,
    )
    # Check the output is still the same for first element
    assert (
        abs(dec2[: len2[0].item(), 0, :].mean().item() + 0.05856532230973244)
        < TOLERANCE
    ), f"Decoder values changed: was {dec2[:len2[0].item(), 0, :].mean().item()}"
    assert abs(dec2[0, 0, 0].item() + 0.5106940865516663) < TOLERANCE * 10
    assert abs(dec2[len2[0] - 1, 0, -1].item() + 0.2060139924287796) < TOLERANCE * 10
    loss = get_loss(x2[:, :1], len2[:1], dec2[:, :1, :], decoder)
    assert abs(loss.item() - 2.666358232498169) < TOLERANCE, loss.item()


def reload_model(BPE_path, efficient_attn, gpu) -> tp.Tuple:
    model_path = MODEL_PATH
    reloaded = torch.load(model_path, map_location="cpu")
    # change params of the reloaded model so that it will
    # relaod its own weights and not the MLM or DOBF pretrained model
    reloaded["params"]["reload_model"] = ",".join([str(model_path)] * 2)
    reloaded["params"]["lgs_mapping"] = ""
    reloaded["params"]["reload_encoder_for_decoder"] = False
    reloaded["params"]["fp16"] = False
    reloaded_params = AttrDict(reloaded["params"])
    reloaded_params["efficient_attn"] = efficient_attn
    # build dictionary / update parameters
    dico = Dictionary(
        reloaded["dico_id2word"], reloaded["dico_word2id"], reloaded["dico_counts"]
    )
    assert reloaded_params.n_words == len(dico)
    assert reloaded_params.bos_index == dico.index(BOS_WORD)
    assert reloaded_params.eos_index == dico.index(EOS_WORD)
    assert reloaded_params.pad_index == dico.index(PAD_WORD)
    assert reloaded_params.unk_index == dico.index(UNK_WORD)
    assert reloaded_params.mask_index == dico.index(MASK_WORD)
    lang2id = reloaded_params.lang2id
    # build model / reload weights (in the build_model method)
    encoder, decoder = build_model(reloaded_params, dico, gpu)
    encoder = encoder[0]
    decoder = decoder[0]
    encoder.eval()
    decoder.eval()
    assert (
        abs(
            sum([x.mean().item() for x in encoder.state_dict().values()])
            - 7.67796907491811
        )
        < 1e-6
    ), "Encoder badly reloaded"
    assert (
        abs(
            sum([x.mean().item() for x in decoder.state_dict().values()])
            - 13.814257268892561
        )
        < 1e-6
    ), "Encoder badly reloaded"
    # reload bpe
    if (
        reloaded_params.get("roberta_mode", False)
        or reloaded_params.get("tokenization_mode", "") == "roberta"
    ):
        bpe_transf: transf.BpeBase = transf.RobertaBpe()
        raise ValueError("This part has not beem tested thoroughly yet")
    else:
        bpe_transf = transf.FastBpe(code_path=Path(BPE_path).absolute())
    bpetensorizer = transf.BpeTensorizer()
    bpetensorizer.dico = dico  # TODO: hacky
    in_pipe = bpe_transf.pipe(bpetensorizer)
    return decoder, encoder, in_pipe, lang2id


def get_loss(x2, len2, dec2, decoder):
    # loss
    alen = torch.arange(x2.shape[0], dtype=torch.long, device=len2.device)
    # do not predict anything given the last target word
    pred_mask = alen[:, None] < len2[None] - 1
    y = x2[1:].masked_select(pred_mask[:-1])
    _, loss = decoder(
        "predict", tensor=dec2, pred_mask=pred_mask, y=y, get_scores=False
    )
    return loss


def decode(
    codes_input: tp.Union[str, tp.List[str]],
    enc1,
    len1,
    lang2,
    lang2id,
    in_pipe,
    decoder,
    device,
):
    if isinstance(codes_input, str):
        codes = [codes_input]
    else:
        codes = codes_input
    lang2_id = lang2id[lang2 + "_sa"]
    x2, len2 = batch_sentences(
        [numpy.array(in_pipe.apply(code))[1:-1] for code in codes],
        eos_index=decoder.dico.eos_index,
        pad_index=decoder.dico.pad_index,
    )
    x2, len2 = x2.to(device), len2.to(device)

    langs2 = x2.clone().fill_(lang2_id)
    dec2 = decoder(
        "fwd",
        x=x2,
        lengths=len2,
        langs=langs2,
        causal=True,
        src_enc=enc1,
        src_len=len1,
    )
    return dec2, x2, len2
