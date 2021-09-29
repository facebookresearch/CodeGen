# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import argparse
import json
import random

from src.data.loader import check_data_params, load_data
from src.evaluation.evaluator import SingleEvaluator, EncDecEvaluator
from src.model import check_model_params, build_model, build_classifier
from src.slurm import init_signal_handler, init_distributed_mode
from src.trainer import SingleTrainer, EncDecTrainer
from src.utils import bool_flag, initialize_exp, set_sampling_probs, shuf_order
from src.utils import print_memory


def get_parser():
    """
    Generate a parameters parser.
    """
    # parse parameters
    parser = argparse.ArgumentParser(description="Language transfer")

    # main parameters
    parser.add_argument(
        "--dump_path", type=str, default="./dumped/", help="Experiment dump path"
    )
    parser.add_argument("--exp_name", type=str, default="", help="Experiment name")
    parser.add_argument(
        "--save_periodic",
        type=int,
        default=0,
        help="Save the model periodically (0 to disable)",
    )
    parser.add_argument("--exp_id", type=str, default="", help="Experiment ID")

    # float16 / AMP API
    parser.add_argument(
        "--fp16", type=bool_flag, default=False, help="Run model with float16"
    )
    parser.add_argument(
        "--amp",
        type=int,
        default=-1,
        help="Use AMP wrapper for float16 / distributed / gradient accumulation. Level of optimization. -1 to disable.",
    )

    # only use an encoder (use a specific decoder for machine translation)
    parser.add_argument(
        "--encoder_only", type=bool_flag, default=True, help="Only use an encoder"
    )

    # model parameters
    parser.add_argument("--emb_dim", type=int, default=512, help="Embedding layer size")
    parser.add_argument(
        "--emb_dim_encoder", type=int, default=0, help="Embedding layer size"
    )
    parser.add_argument(
        "--emb_dim_decoder", type=int, default=0, help="Embedding layer size"
    )
    parser.add_argument(
        "--n_layers", type=int, default=4, help="Number of Transformer layers"
    )
    parser.add_argument(
        "--n_layers_encoder",
        type=int,
        default=0,
        help="Number of Transformer layers for the encoder",
    )
    parser.add_argument(
        "--n_layers_decoder",
        type=int,
        default=0,
        help="Number of Transformer layers for the decoder",
    )
    parser.add_argument(
        "--n_heads", type=int, default=8, help="Number of Transformer heads"
    )
    parser.add_argument("--dropout", type=float, default=0, help="Dropout")
    parser.add_argument(
        "--attention_dropout",
        type=float,
        default=0,
        help="Dropout in the attention layer",
    )
    parser.add_argument(
        "--gelu_activation",
        type=bool_flag,
        default=False,
        help="Use a GELU activation instead of ReLU",
    )
    parser.add_argument(
        "--share_inout_emb",
        type=bool_flag,
        default=True,
        help="Share input and output embeddings",
    )
    parser.add_argument(
        "--sinusoidal_embeddings",
        type=bool_flag,
        default=False,
        help="Use sinusoidal embeddings",
    )
    parser.add_argument(
        "--use_lang_emb", type=bool_flag, default=True, help="Use language embedding"
    )

    # causal language modeling task parameters
    parser.add_argument(
        "--context_size",
        type=int,
        default=0,
        help="Context size (0 means that the first elements in sequences won't have any context)",
    )

    # masked language modeling task parameters
    parser.add_argument(
        "--word_pred",
        type=float,
        default=0.15,
        help="Fraction of words for which we need to make a prediction",
    )
    parser.add_argument(
        "--sample_alpha",
        type=float,
        default=0,
        help="Exponent for transforming word counts to probabilities (~word2vec sampling)",
    )
    parser.add_argument(
        "--word_mask_keep_rand",
        type=str,
        default="0.8,0.1,0.1",
        help="Fraction of words to mask out / keep / randomize, among the words to predict",
    )
    parser.add_argument(
        "--mask_length",
        type=str,
        default="",
        help="Length distribution of the masked spans. "
        "No span masking if kept empty. Constant if integer. Poisson if 'poisson'",
    )
    parser.add_argument(
        "--poisson_lambda",
        type=float,
        default=3.0,
        help="Parameter of the poisson distribution for span length",
    )

    # input sentence noise
    parser.add_argument(
        "--word_shuffle",
        type=float,
        default=0,
        help="Randomly shuffle input words (0 to disable)",
    )
    parser.add_argument(
        "--word_dropout",
        type=float,
        default=0,
        help="Randomly dropout input words (0 to disable)",
    )
    parser.add_argument(
        "--word_blank",
        type=float,
        default=0,
        help="Randomly blank input words (0 to disable)",
    )

    # data
    parser.add_argument("--data_path", type=str, default="", help="Data path")
    parser.add_argument(
        "--lgs", type=str, default="", help="Languages (lg1-lg2-lg3 .. ex: en-fr-es-de)"
    )
    parser.add_argument(
        "--lgs_mapping",
        type=str,
        default="",
        help="Map the lngs to pretrained lgs, java_sa:java_obfuscated"
        "then the emb of java_sa in this XP will be mapped to the emb of java_obfuscated in pretrained model",
    )
    parser.add_argument(
        "--lgs_id_mapping",
        type=str,
        default="",
        help="Map the in or out language id of some languages to others for mt_steps "
        "for instance 'java_np:java_buggy-java_resolved' means java_np gets the "
        "same language embeddings as java_buggy for input sentences and java_resolved "
        "for output sentences. Different mappings separated by commas",
    )
    parser.add_argument(
        "--max_vocab",
        type=int,
        default=-1,
        help="Maximum vocabulary size (-1 to disable)",
    )
    parser.add_argument(
        "--min_count", type=int, default=0, help="Minimum vocabulary count"
    )
    parser.add_argument(
        "--lg_sampling_factor", type=float, default=-1, help="Language sampling factor"
    )
    parser.add_argument(
        "--has_sentence_ids",
        type=str,
        default="",
        help="Datasets with parallel sentence ids. Datasets separated by ,. "
        "Example 'valid|para,train|lang1 if all parallel valid datasets and train lang1 datasets have ids",
    )

    # batch parameters
    parser.add_argument("--bptt", type=int, default=256, help="Sequence length")
    parser.add_argument(
        "--max_len",
        type=int,
        default=100,
        help="Maximum length of sentences (after BPE)",
    )
    parser.add_argument(
        "--group_by_size",
        type=bool_flag,
        default=True,
        help="Sort sentences by size during the training",
    )
    parser.add_argument(
        "--batch_size", type=int, default=32, help="Number of sentences per batch"
    )
    parser.add_argument(
        "--max_batch_size",
        type=int,
        default=0,
        help="Maximum number of sentences per batch (used in combination with tokens_per_batch, 0 to disable)",
    )
    parser.add_argument(
        "--tokens_per_batch", type=int, default=-1, help="Number of tokens per batch"
    )

    parser.add_argument(
        "--gen_tpb_multiplier",
        type=int,
        default=1,
        help="Multiplier of token per batch during generation when doing back translation. Typically 4",
    )

    # training parameters
    parser.add_argument(
        "--split_data",
        type=bool_flag,
        default=False,
        help="Split data across workers of a same node",
    )
    parser.add_argument(
        "--split_data_accross_gpu",
        type=str,
        default="local",
        help="Split data across GPU locally or globally. Set 'local' or 'global'",
    )
    parser.add_argument(
        "--optimizer",
        type=str,
        default="adam,lr=0.0001",
        help="Optimizer (SGD / RMSprop / Adam, etc.)",
    )
    parser.add_argument(
        "--clip_grad_norm",
        type=float,
        default=5,
        help="Clip gradients norm (0 to disable)",
    )
    parser.add_argument(
        "--epoch_size",
        type=int,
        default=100000,
        help="Epoch size / evaluation frequency (-1 for parallel data size)",
    )
    parser.add_argument(
        "--max_epoch", type=int, default=100000, help="Maximum epoch size"
    )
    parser.add_argument(
        "--stopping_criterion",
        type=str,
        default="",
        help="Stopping criterion, and number of non-increase before stopping the experiment",
    )
    parser.add_argument(
        "--validation_metrics", type=str, default="", help="Validation metrics"
    )
    parser.add_argument(
        "--accumulate_gradients",
        type=int,
        default=1,
        help="Accumulate model gradients over N iterations (N times larger batch sizes)",
    )
    parser.add_argument(
        "--add_eof_to_stream",
        type=bool_flag,
        default=False,
        help="Whether to add </s> at the beginning "
        "of every sentence in steam datasets."
        "It matters for MLM.",
    )

    # training coefficients
    parser.add_argument(
        "--lambda_mlm", type=str, default="1", help="Prediction coefficient (MLM)"
    )
    parser.add_argument(
        "--lambda_clm", type=str, default="1", help="Causal coefficient (LM)"
    )
    parser.add_argument("--lambda_ae", type=str, default="1", help="AE coefficient")
    parser.add_argument("--lambda_mt", type=str, default="1", help="MT coefficient")
    parser.add_argument(
        "--lambda_do", type=str, default="1", help="Deobfuscation coefficient"
    )
    parser.add_argument("--lambda_bt", type=str, default="1", help="BT coefficient")
    parser.add_argument(
        "--lambda_st", type=str, default="1", help="Self-training coefficient"
    )
    parser.add_argument(
        "--lambda_classif",
        type=str,
        default="1",
        help="Classificationlambda coefficient -  can have one per pair of lang/label - format 'lang1-label1::lambda / lang2-label2::lambda / lambda' or 'lang1-label1::lambda / lang2-label2::lambda' or 'lambda'",
    )

    # training steps
    parser.add_argument(
        "--clm_steps", type=str, default="", help="Causal prediction steps (CLM)"
    )
    parser.add_argument(
        "--mlm_steps", type=str, default="", help="Masked prediction steps (MLM / TLM)"
    )
    parser.add_argument(
        "--mt_steps", type=str, default="", help="Machine translation steps"
    )
    parser.add_argument(
        "--cmt_steps",
        type=str,
        default="",
        help="Conditioned machine translation steps",
    )
    parser.add_argument(
        "--disc_steps", type=str, default="", help="Discriminator training steps"
    )
    parser.add_argument("--do_steps", type=str, default="", help="Deobfuscation steps")
    parser.add_argument(
        "--obf_proba",
        type=float,
        default=0.5,
        help="For Deobfuscation steps, probability of obsfuscation. If = 1 everything is obfuscated, 0 only one variable.",
    )

    parser.add_argument(
        "--st_steps", type=str, default="", help="Self trainings teps using unit tests"
    )
    parser.add_argument(
        "--ae_steps", type=str, default="", help="Denoising auto-encoder steps"
    )
    parser.add_argument(
        "--bt_steps", type=str, default="", help="Back-translation steps"
    )
    parser.add_argument(
        "--mt_spans_steps",
        type=str,
        default="",
        help="Machine translation steps. Format for one step is lang1-lang2-span. Steps are separated by commas.",
    )
    parser.add_argument(
        "--spans_emb_encoder",
        type=bool_flag,
        default=False,
        help="Whether to use span embeddings in the encoder",
    )

    parser.add_argument(
        "--classif_steps", type=str, default="", help="Classification steps"
    )

    # reload pretrained embeddings / pretrained model / checkpoint
    parser.add_argument(
        "--reload_emb", type=str, default="", help="Reload pretrained word embeddings"
    )
    parser.add_argument(
        "--reload_model", type=str, default="", help="Reload a pretrained model"
    )

    parser.add_argument(
        "--reload_encoder_attn_on_decoder",
        type=bool_flag,
        default=False,
        help="If true, reload encoder attention on decoder if there is no pre-trained decoder.",
    )
    parser.add_argument(
        "--reload_encoder_for_decoder",
        type=bool_flag,
        default=False,
        help="Reload a the encoder of the pretrained model for the decoder.",
    )
    parser.add_argument(
        "--roberta_mode",
        type=bool_flag,
        default=False,
        help="If we reload a pretrained roberta, need to put this params to True that positions idx are computed in the roberta way and use gelu.",
    )
    parser.add_argument(
        "--reload_checkpoint", type=str, default="", help="Reload a checkpoint"
    )

    # beam search (for MT only)
    parser.add_argument(
        "--beam_size",
        type=int,
        default=1,
        help="Beam size, default = 1 (greedy decoding)",
    )

    parser.add_argument(
        "--length_penalty",
        type=float,
        default=1,
        help="Length penalty, values < 1.0 favor shorter sentences, while values > 1.0 favor longer ones.",
    )
    parser.add_argument(
        "--early_stopping",
        type=bool_flag,
        default=False,
        help="Early stopping, stop as soon as we have `beam_size` hypotheses, although longer ones may have better scores.",
    )
    # sampling at eval time
    parser.add_argument(
        "--number_samples",
        type=int,
        default=1,
        help="Number of examples to sample (default = 1)",
    )
    parser.add_argument(
        "--eval_temperature",
        type=float,
        default=None,
        help="Evaluation temperature when using several samples",
    )

    # BT parameters
    parser.add_argument(
        "--bt_sample_temperature",
        type=str,
        default="0",
        help="At BT training, sample temperature for generation",
    )

    # ST parameters
    parser.add_argument(
        "--st_sample_temperature",
        type=str,
        default="0",
        help="At ST training, sample temperature for generation",
    )

    parser.add_argument(
        "--st_sample_cache_ratio",
        type=str,
        default="2",
        help="At ST training, probability to sample from cache. If integer, sampling deterministically n times for each creation step",
    )

    parser.add_argument(
        "--st_limit_tokens_per_batch",
        type=bool_flag,
        default=True,
        help="At ST training, whether to limit batch size based on tokens per batch",
    )

    parser.add_argument(
        "--st_sample_size",
        type=int,
        default=1,
        help="Batch size for data sampled from cache",
    )

    parser.add_argument(
        "--st_remove_proba",
        type=float,
        default=0.0,
        help="Proba to remove sampled elements from cache",
    )

    parser.add_argument(
        "--cache_warmup",
        type=int,
        default=500,
        help="Batch size for data sampled from cache",
    )

    parser.add_argument(
        "--robin_cache",
        type=bool_flag,
        default=False,
        help="Whether to use the round robin cache",
    )

    parser.add_argument(
        "--st_min_asserts",
        type=str,
        default="2",
        help="Minimum number of asserts for the unit tests",
    )

    parser.add_argument(
        "--st_show_stats",
        type=bool,
        default=False,
        help="Whether to show stats about the created tests",
    )

    parser.add_argument(
        "--st_min_mutation_score",
        type=str,
        default="0.9",
        help="Minimum mutation score for the unit tests",
    )

    parser.add_argument(
        "--st_refresh_iterator_rate",
        type=int,
        default=-1,
        help="rate for refreshing the iterator taking new cutoff rate into account",
    )

    parser.add_argument(
        "--unit_tests_path",
        type=str,
        default="",
        help="path to the json file containing the unit tests and scores",
    )

    parser.add_argument(
        "--cache_size",
        type=int,
        default=20000,
        help="Size of the cache for round robin cache",
    )

    parser.add_argument(
        "--cache_init_path",
        type=str,
        default="",
        help="path to files to use to initialize the cache",
    )
    # ST beam size
    parser.add_argument(
        "--st_beam_size", type=str, default="1", help="At ST training: beam size",
    )

    # ST beam size
    parser.add_argument(
        "--st_length_penalty",
        type=float,
        default=0.5,
        help="Length penalty for generating elements",
    )

    # ST test timeout
    parser.add_argument(
        "--st_test_timeout",
        type=int,
        default=15,
        help="Timeout for the test runner running the unit tests",
    )

    # Classification parameters
    parser.add_argument(
        "--n_classes_classif",
        type=int,
        default=0,
        help="Number of classes for classification steps.",
    )
    parser.add_argument(
        "--reload_classifier",
        type=str,
        default="",
        help="Reload pretrained classifier.",
    )

    # evaluation
    parser.add_argument(
        "--eval_bleu",
        type=bool_flag,
        default=False,
        help="Evaluate BLEU score during MT training",
    )
    parser.add_argument(
        "--eval_denoising",
        type=bool_flag,
        default=False,
        help="Whether to evaluate the model for denoising",
    )
    parser.add_argument(
        "--eval_subtoken_score",
        type=bool_flag,
        default=False,
        help="Evaluate subtoken score during MT training",
    )
    parser.add_argument(
        "--eval_bleu_test_only",
        type=bool_flag,
        default=False,
        help="Evaluate BLEU score during MT training",
    )
    parser.add_argument(
        "--eval_computation",
        type=bool_flag,
        default=False,
        help="Check if the generated function is compilable, and if it returns the same output as ground truth.",
    )
    parser.add_argument(
        "--eval_st",
        type=bool_flag,
        default=False,
        help="Whether to evaluate on self-generated tests with evosuite.",
    )
    parser.add_argument(
        "--generate_hypothesis",
        type=bool_flag,
        default=False,
        help="generate hypothesis for test/valid mono dataset",
    )
    parser.add_argument(
        "--eval_only", type=bool_flag, default=False, help="Only run evaluations"
    )
    parser.add_argument(
        "--retry_mistmatching_types",
        type=bool_flag,
        default=False,
        help="Retry with wrapper at eval time when the types do not match",
    )

    parser.add_argument(
        "--n_sentences_eval",
        type=int,
        default=1500,
        help="Number of sentences for evaluation",
    )

    # debug
    parser.add_argument(
        "--debug_train",
        type=bool_flag,
        default=False,
        help="Use valid sets for train sets (faster loading)",
    )
    parser.add_argument(
        "--debug_slurm",
        type=bool_flag,
        default=False,
        help="Debug multi-GPU / multi-node within a SLURM job",
    )
    parser.add_argument("--debug", help="Enable all debug flags", action="store_true")

    # multi-gpu / multi-node
    parser.add_argument(
        "--local_rank", type=int, default=-1, help="Multi-GPU - Local rank"
    )
    parser.add_argument(
        "--master_port",
        type=int,
        default=-1,
        help="Master port (for multi-node SLURM jobs)",
    )
    parser.add_argument(
        "--separate_decoders",
        type=bool_flag,
        default=False,
        help="Use a separate decoder for each language",
    )

    parser.add_argument(
        "--n_share_dec", type=int, default=0, help="Number of decoder layers to share"
    )

    return parser


def main(params):
    # initialize the multi-GPU / multi-node training
    init_distributed_mode(params)

    # initialize the experiment
    logger = initialize_exp(params)

    # initialize SLURM signal handler for time limit / pre-emption
    init_signal_handler()

    # load data
    data = load_data(params)

    # build model
    print_memory(logger, "before build modules")
    if params.encoder_only:
        model = build_model(params, data["dico"])
    else:
        encoder, decoder = build_model(params, data["dico"])
    print_memory(logger, "before build classifier")

    if params.use_classifier:
        classifier = build_classifier(params)
    else:
        classifier = None

    # build trainer, reload potential checkpoints / build evaluator
    if params.encoder_only:
        trainer = SingleTrainer(model, data, params, classifier)
        evaluator = SingleEvaluator(trainer, data, params)
    else:
        trainer = EncDecTrainer(encoder, decoder, data, params)
        evaluator = EncDecEvaluator(trainer, data, params)
    print_memory(logger, "after building all models")

    # evaluation
    if params.eval_only:
        scores = evaluator.run_all_evals(trainer)
        for k, v in scores.items():
            if isinstance(v, list):
                logger.info("%s -> %s" % (k, json.dumps(["%.2f" % el for el in v])))
            else:
                logger.info("%s -> %.6f" % (k, v))
        logger.info("__log__:%s" % json.dumps(scores))
        exit()

    # set sampling probabilities for training
    set_sampling_probs(data, params)

    # language model training
    for _ in range(params.max_epoch):

        logger.info("============ Starting epoch %i ... ============" % trainer.epoch)

        trainer.n_sentences = 0

        while trainer.n_sentences < trainer.epoch_size:
            show_example = True if trainer.n_sentences == 0 else False

            # CLM steps
            for lang1, lang2 in shuf_order(params.clm_steps, params):
                trainer.clm_step(lang1, lang2, params.lambda_clm)

            # MLM steps (also includes TLM if lang2 is not None)
            for lang1, lang2 in shuf_order(params.mlm_steps, params):
                trainer.mlm_step(
                    lang1, lang2, params.lambda_mlm, show_example=show_example
                )

            # denoising auto-encoder steps
            for lang in shuf_order(params.ae_steps):
                trainer.mt_step(
                    lang, lang, params.lambda_ae, show_example=show_example,
                )

            # machine translation steps
            for lang1, lang2 in shuf_order(params.mt_steps, params):
                trainer.mt_step(
                    lang1, lang2, params.lambda_mt, show_example=show_example,
                )

            # machine translation using spans steps
            for lang1, lang2, span in shuf_order(params.mt_spans_steps, params):
                trainer.mt_step(
                    lang1,
                    lang2,
                    params.lambda_mt,
                    span=span,
                    show_example=show_example,
                )

            # deobscuation step
            for lang1, lang2 in shuf_order(params.do_steps):
                trainer.mt_step(
                    lang1,
                    lang2,
                    params.lambda_do,
                    deobfuscate=True,
                    deobfuscate_p=1 - params.obf_proba,
                    show_example=show_example,
                )

            # back-translation steps
            for lang1, lang2, lang3 in shuf_order(params.bt_steps):
                trainer.bt_step(
                    lang1,
                    lang2,
                    lang3,
                    params.lambda_bt,
                    params.bt_sample_temperature,
                    show_example=show_example,
                )

            # Classification
            for lang1, lang2 in shuf_order(params.classif_steps, params):
                trainer.classif_step(
                    lang1,
                    lang2,
                    getattr(params, "lambda_classif_" + "_".join((lang1, lang2))),
                )

            # Self-Labelling
            for lang1, langs2 in shuf_order(params.st_steps):
                trainer.st_step(
                    lang1, langs2, params.lambda_st, show_example=show_example,
                )

            trainer.iter()

        logger.info("============ End of epoch %i ============" % trainer.epoch)

        # evaluate perplexity
        scores = evaluator.run_all_evals(trainer)

        # print / JSON log
        for k, v in scores.items():
            if isinstance(v, list):
                logger.info("%s -> %s" % (k, json.dumps(["%.2f" % el for el in v])))
            else:
                logger.info("%s -> %.6f" % (k, v))
        if params.is_master:
            logger.info("__log__:%s" % json.dumps(scores))

        # end of epoch
        if params.validation_metrics != "":
            trainer.save_best_model(scores)
        trainer.save_periodic()
        trainer.end_epoch(scores)


if __name__ == "__main__":

    # generate parser / parse parameters
    parser = get_parser()
    params = parser.parse_args()

    # debug mode
    if params.debug:
        params.exp_name = "debug"
        params.exp_id = "debug_%08i" % random.randint(0, 100000000)
        params.debug_slurm = True
        params.debug_train = True

    # check parameters
    check_data_params(params)
    check_model_params(params)

    # run experiment
    main(params)
