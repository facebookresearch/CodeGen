# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import math
import os
import sys
from logging import getLogger

import torch

from .pretrain import load_embeddings

# , TRANSFORMER_LAYER_PARAMS
from .transformer import DECODER_ONLY_PARAMS, TransformerModel, Classifier
from ..data.dictionary import UNK_WORD

logger = getLogger()


def check_model_params(params):
    """
    Check models parameters.
    """
    # masked language modeling task parameters
    assert params.bptt >= 1
    assert 0 <= params.word_pred < 1
    assert 0 <= params.sample_alpha < 1
    s = params.word_mask_keep_rand.split(",")
    assert len(s) == 3
    s = [float(x) for x in s]
    assert all([0 <= x <= 1 for x in s]) and sum(s) == 1
    params.word_mask = s[0]
    params.word_keep = s[1]
    params.word_rand = s[2]

    if params.mask_length == "":
        params.mask_length = None
        params.mask_length_dist = None
    elif params.mask_length == "poisson":
        assert (
            params.poisson_lambda is not None
        ), "poisson_lambda is None, it should be set when using poisson mask_length"
        _lambda = params.poisson_lambda

        lambda_to_the_k = 1
        e_to_the_minus_lambda = math.exp(-_lambda)
        k_factorial = 1
        ps = []
        for k in range(0, 128):
            ps.append(e_to_the_minus_lambda * lambda_to_the_k / k_factorial)
            lambda_to_the_k *= _lambda
            k_factorial *= k + 1
            if ps[-1] < 0.0000001:
                break
        ps = torch.FloatTensor(ps)
        params.mask_length_dist_probas = ps
        params.mask_length_dist = torch.distributions.Categorical(ps)
    else:
        params.mask_length = int(params.mask_length)
        ps = torch.FloatTensor(params.mask_length + 1).fill_(0.0)
        ps[params.mask_length] = 1
        params.mask_length_dist = torch.distributions.Categorical(ps)

    # input sentence noise for DAE
    if len(params.ae_steps) == 0:
        assert params.word_shuffle == 0
        assert params.word_dropout == 0
        assert params.word_blank == 0
    else:
        assert params.word_shuffle == 0 or params.word_shuffle > 1
        assert 0 <= params.word_dropout < 1
        assert 0 <= params.word_blank < 1

    # model dimensions
    if params.emb_dim_encoder == 0 and params.emb_dim_decoder == 0:
        assert params.emb_dim > 0
        params.emb_dim_encoder = params.emb_dim
        params.emb_dim_decoder = params.emb_dim
    else:
        assert params.emb_dim == 0
        assert params.emb_dim_encoder > 0 and params.emb_dim_decoder > 0
        if params.emb_dim_encoder == params.emb_dim_decoder:
            params.emb_dim = params.emb_dim_decoder
        else:
            assert params.reload_emb == "", (
                "Pre-trained embeddings are not supported when the embedding size of the "
                "encoder and the decoder do not match "
            )
    assert params.emb_dim_encoder % params.n_heads == 0
    assert params.emb_dim_decoder % params.n_heads == 0

    if params.n_layers_encoder == 0 and params.n_layers_decoder == 0:
        assert params.n_layers > 0
        params.n_layers_encoder = params.n_layers
        params.n_layers_decoder = params.n_layers
    else:
        assert params.n_layers == 0

    assert params.n_layers_encoder > 0 and params.n_layers_decoder > 0

    # reload pretrained word embeddings
    if params.reload_emb != "":
        assert os.path.isfile(params.reload_emb)

    # reload a pretrained model
    if params.reload_model != "":
        if params.encoder_only:
            assert os.path.isfile(params.reload_model)
        else:
            s = params.reload_model.split(",")
            assert len(s) == 2
            assert all([x == "" or os.path.isfile(x) for x in s])
        if params.use_classifier and params.reload_classifier == "":
            params.reload_classifier = params.reload_model

    assert not (
        params.beam_size > 1 and params.number_samples > 1
    ), "Cannot sample when already doing beam search"
    assert (params.eval_temperature is None) == (
        params.number_samples <= 1
    ), "Eval temperature should be set if and only if taking several samples at eval time"


def set_pretrain_emb(model, dico, word2id, embeddings):
    """
    Pretrain word embeddings.
    """
    n_found = 0
    with torch.no_grad():
        for i in range(len(dico)):
            idx = word2id.get(dico[i], None)
            if idx is None:
                continue
            n_found += 1
            model.embeddings.weight[i] = embeddings[idx].cuda()
            model.pred_layer.proj.weight[i] = embeddings[idx].cuda()
    logger.info(
        "Pretrained %i/%i words (%.3f%%)."
        % (n_found, len(dico), 100.0 * n_found / len(dico))
    )


def build_model(params, dico):
    """
    Build model.
    """
    if params.encoder_only:
        # build
        model = TransformerModel(params, dico, is_encoder=True, with_output=True)

        # reload pretrained word embeddings
        if params.reload_emb != "":
            word2id, embeddings = load_embeddings(params.reload_emb, params)
            set_pretrain_emb(model, dico, word2id, embeddings)

        # reload a pretrained model
        if params.reload_model != "":
            logger.info("============ Model Reloading")
            logger.info("Reloading model from %s ..." % params.reload_model)
            reload_transformer(params, params.reload_model, dico, model, "model")

        logger.info("Model: {}".format(model))
        logger.info(
            "Number of parameters (model): %i"
            % sum([p.numel() for p in model.parameters() if p.requires_grad])
        )
        logger.info("")

        return [model.cuda()]

    else:
        # build
        # TODO: only output when necessary - len(params.clm_steps + params.mlm_steps) > 0
        encoder = TransformerModel(params, dico, is_encoder=True, with_output=True)

        if params.separate_decoders:
            decoders = [
                TransformerModel(params, dico, is_encoder=False, with_output=True)
                for _ in params.lang2id.values()
            ]
        else:
            decoders = [
                TransformerModel(params, dico, is_encoder=False, with_output=True)
            ]

        for layer in range(params.n_layers_decoder):
            if layer <= params.n_share_dec - 1:
                assert params.amp == -1, "sharing layers is not supported with AMP"
                logger.info("Sharing decoder attention parameters for layer %i" % layer)
                for i in range(1, len(decoders)):
                    decoders[i].attentions[layer] = decoders[0].attentions[layer]

        # reload pretrained word embeddings
        if params.reload_emb != "":
            word2id, embeddings = load_embeddings(params.reload_emb, params)
            set_pretrain_emb(encoder, dico, word2id, embeddings)
            for decoder in decoders:
                set_pretrain_emb(decoder, dico, word2id, embeddings)
        # reload a pretrained model
        if params.reload_model != "":
            logger.info("============ Model Reloading")
            enc_path, dec_path = params.reload_model.split(",")
            assert not (enc_path == "" and dec_path == "")

            # reload encoder
            if enc_path != "":
                logger.info("Reloading encoder from %s ..." % enc_path)
                reload_transformer(params, enc_path, dico, encoder, "encoder")

            # reload decoders
            if dec_path != "":
                for dec in decoders:
                    logger.info("Reloading decoders from %s ..." % dec_path)
                    if params.reload_encoder_for_decoder:
                        reload_transformer(params, dec_path, dico, dec, "encoder")
                    else:
                        reload_transformer(params, dec_path, dico, dec, "decoder")

        logger.debug("Encoder: {}".format(encoder))
        logger.debug("Decoder: {}".format(decoders))
        logger.info(
            "Number of parameters (encoder): %i"
            % sum([p.numel() for p in encoder.parameters() if p.requires_grad])
        )
        logger.info(
            "Number of parameters (decoders): %i"
            % sum([p.numel() for p in decoders[0].parameters() if p.requires_grad])
        )
        logger.info(f"Number of decoders: {len(decoders)}")
        logger.info("")

        return [encoder.cuda()], [dec.cuda() for dec in decoders]


def build_classifier(params):
    """
    Build classifier.
    """

    # build
    classifier = Classifier(params)

    # reload a pretrained model
    if params.reload_classifier != "":
        logger.info("Reloading classifier from %s ..." % params.reload_classifier)
        reloaded = torch.load(
            params.reload_classifier,
            map_location=lambda storage, loc: storage.cuda(params.local_rank),
        )
        if "classifier" not in reloaded:
            logger.warning(
                f"There is no classifier in {params.reload_classifier}. The classifier weights will be initialized randomly"
            )
        else:
            reloaded = reloaded["classifier"]
            if all([k.startswith("module.") for k in reloaded.keys()]):
                reloaded = {k[len("module.") :]: v for k, v in reloaded.items()}
            classifier.load_state_dict(reloaded)

    logger.info("Classifier: {}".format(classifier))

    return [classifier.cuda()]


def reload_transformer(params, path, dico, model, model_type):
    """
    Reload a transformer state dict to current model:
    clean 'module.' from state dict,
    match the word embeddings comparing dicos,
    match lang embedding with params lang mapping,
    extend or truncate position embeddings when size dont match,
    load state dict.
    """

    reloaded = torch.load(
        path, map_location=lambda storage, loc: storage.cuda(params.local_rank)
    )
    clean_model_state_dict(reloaded, model_type)
    reload_word_embeddings(reloaded, dico, model_type)
    reload_lang_embeddings(reloaded, params, model_type)
    reload_position_embeddings(reloaded, model, model_type)

    # if the model is a decoder
    if hasattr(model, "encoder_attn"):
        for i in range(params.n_layers_decoder):
            for name in DECODER_ONLY_PARAMS:
                weight_name = name % i
                if weight_name not in reloaded[model_type]:
                    logger.warning("Parameter %s not found." % (weight_name))
                    encoder_attn_name = weight_name.replace(
                        "encoder_attn", "attentions"
                    )
                    if (
                        getattr(params, "reload_encoder_attn_on_decoder", False)
                        and "encoder_attn" in weight_name
                        and encoder_attn_name in reloaded[model_type]
                    ):
                        logger.warning(f"Reloading {encoder_attn_name} instead")
                        reloaded[model_type][weight_name] = (
                            reloaded[model_type][encoder_attn_name].clone().detach()
                        )
                    else:
                        reloaded[model_type][weight_name] = model.state_dict()[
                            weight_name
                        ]
    model.load_state_dict(reloaded[model_type], strict=not params.spans_emb_encoder)


def clean_model_state_dict(reloaded, model_type):
    """
    remove prefix module from the keys of the model state dict.
    """

    model_reloaded = reloaded[model_type if model_type in reloaded else "model"]
    if all([k.startswith("module.") for k in model_reloaded.keys()]):
        model_reloaded = {k[len("module.") :]: v for k, v in model_reloaded.items()}
    reloaded[model_type] = model_reloaded


def reload_word_embeddings(reloaded, dico, model_type):
    """
    Check when reloading a model that dictionary are the same. If not, do a word embedding mapping if possible.
    """
    reloaded_word2id = reloaded["dico_word2id"]
    reloaded_id2word = reloaded["dico_id2word"]
    assert len(reloaded_word2id) == len(reloaded_id2word)
    assert all(reloaded_id2word[v] == k for k, v in reloaded_word2id.items())

    matching_indices = []
    word_not_found = []
    for idx, word in dico.id2word.items():
        if word not in reloaded_word2id:
            word_not_found += [word]
            matching_indices += [reloaded_word2id[UNK_WORD]]
        else:
            matching_indices += [reloaded_word2id[word]]
    assert len(matching_indices) == len(dico)
    if len(word_not_found) > 0:
        logger.warning(
            f"When reloading word embeddings, could not find embeddings for {len(word_not_found)} words: {word_not_found[0:5] + ['...'] + word_not_found[-5:]}... Initializing them to < unk >."
        )

    reloaded[model_type]["embeddings.weight"] = torch.cat(
        [
            reloaded[model_type]["embeddings.weight"][index : index + 1]
            for index in matching_indices
        ],
        dim=0,
    )

    if "pred_layer.proj.weight" in reloaded[model_type]:
        first_line = reloaded[model_type]["pred_layer.proj.weight"][0:1]
        embedding_size = reloaded[model_type]["pred_layer.proj.weight"].shape[1]
        reloaded[model_type]["pred_layer.proj.weight"] = torch.cat(
            [
                reloaded[model_type]["pred_layer.proj.weight"][index : index + 1]
                if index is not None
                else torch.normal(
                    torch.zeros_like(first_line),
                    torch.ones_like(first_line * (embedding_size ** (-0.5))),
                )
                for index in matching_indices
            ],
            dim=0,
        )
        reloaded[model_type]["pred_layer.proj.bias"] = torch.cat(
            [
                reloaded[model_type]["pred_layer.proj.bias"][index].view(1)
                if index is not None
                else torch.rand_like(
                    reloaded[model_type]["pred_layer.proj.bias"][0].view(1)
                )
                for index in matching_indices
            ]
        )


def reload_lang_embeddings(reloaded, params, model_type):
    """
    When pretrained models has not been trained with the same languages:
    change lang embedding state dict.
    Otherwise, keep as it is.
    """
    model_reloaded = reloaded[model_type]
    reloaded_params = reloaded["params"]
    if params.lgs_mapping == "":
        lang_mapping = {}
    else:
        lang_mapping = {
            mapping.split(":")[0]: mapping.split(":")[1]
            for mapping in params.lgs_mapping.split(",")
        }
    langs_reloaded = reloaded_params["lang2id"]
    langs_reloaded_id2lang = reloaded_params["id2lang"]
    indices = []
    for lang in [l for i, l in sorted(params.id2lang.items())]:
        if lang in lang_mapping:
            lang_ = lang_mapping[lang]
        else:
            lang_ = lang
        index = [id for l, id in langs_reloaded.items() if l == lang_]
        if len(index) == 0:
            logger.warning(
                f"No match found for lang {lang} {lang_} in {langs_reloaded.keys()}. Initializing randomly."
            )
            indices.append(None)
            continue
        else:
            assert (
                len(index) == 1
            ), f"matching lang found: {index} in reloaded model for lang {lang} in {langs_reloaded.keys()}"
            logger.warning(
                f"Lang {lang} matched to pretrained {langs_reloaded_id2lang[index[0]]} lang embedding."
            )
        indices.append(index[0])

    first_line = model_reloaded["lang_embeddings.weight"][0:1]
    embedding_size = model_reloaded["lang_embeddings.weight"].shape[1]
    model_reloaded["lang_embeddings.weight"] = torch.cat(
        [
            model_reloaded["lang_embeddings.weight"][index : index + 1]
            if index is not None
            else torch.normal(
                torch.zeros_like(first_line),
                torch.ones_like(first_line * (embedding_size ** (-0.5))),
            )
            for index in indices
        ],
        dim=0,
    )
    reloaded[model_type] = model_reloaded


def reload_position_embeddings(reloaded, encoder, model_type):
    """
    When pretrained models has not been trained with the same size of position embedding:
    remove unused or add extra positions.
    """
    model_reloaded = reloaded[model_type]
    current_size = encoder.position_embeddings.weight.size()[0]
    reloaded_size = model_reloaded["position_embeddings.weight"].size()[0]
    if current_size == reloaded_size:
        return model_reloaded
    elif current_size < reloaded_size:
        logger.warning(
            f"The size of position embeddings in current model is {current_size}, the size of reloaded is {reloaded_size}. need to truncate the reloaded position embeddings."
        )
        model_reloaded["position_embeddings.weight"] = model_reloaded[
            "position_embeddings.weight"
        ][:current_size, :]
    else:
        logger.warning(
            f"The size of position embeddings in current model is {current_size}, the size of reloaded is {reloaded_size}. need to repeat last positions {current_size - reloaded_size} times."
        )
        model_reloaded["position_embeddings.weight"] = torch.cat(
            [
                model_reloaded["position_embeddings.weight"],
                model_reloaded["position_embeddings.weight"][-1, :].repeat(
                    current_size - reloaded_size, 1
                ),
            ],
            dim=0,
        )
    reloaded[model_type] = model_reloaded
