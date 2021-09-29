# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import os
from logging import getLogger

import numpy as np
import torch

from .dataset import StreamDataset, Dataset, ParallelDataset
from .dictionary import BOS_WORD, EOS_WORD, PAD_WORD, UNK_WORD, MASK_WORD

SELF_TRAINED = "self_training"
DATASET_SPLITS = ["train", "valid", "test"]
TRAIN_SPLITS = {"train", SELF_TRAINED}

logger = getLogger()


def process_binarized(data, params):
    """
    Process a binarized dataset and log main statistics.
    """
    dico = data["dico"]
    assert (
        (data["sentences"].dtype == np.uint16)
        and (dico is None or (len(dico) < 1 << 16))
        or (data["sentences"].dtype == np.int32)
        and (dico is None or (1 << 16 <= len(dico) < 1 << 31))
    )
    logger.info(
        "%i words (%i unique) in %i sentences. %i unknown words (%i unique) covering %.2f%% of the data."
        % (
            len(data["sentences"]) - len(data["positions"]),
            len(dico) if dico else 0,
            len(data["positions"]),
            sum(data["unk_words"].values()),
            len(data["unk_words"]),
            100.0
            * sum(data["unk_words"].values())
            / (len(data["sentences"]) - len(data["positions"])),
        )
    )
    if params.max_vocab != -1:
        assert params.max_vocab > 0
        logger.info("Selecting %i most frequent words ..." % params.max_vocab)
        if dico is not None:
            dico.max_vocab(params.max_vocab)
            data["sentences"][data["sentences"] >= params.max_vocab] = dico.index(
                UNK_WORD
            )
            unk_count = (data["sentences"] == dico.index(UNK_WORD)).sum()
            logger.info(
                "Now %i unknown words covering %.2f%% of the data."
                % (
                    unk_count,
                    100.0
                    * unk_count
                    / (len(data["sentences"]) - len(data["positions"])),
                )
            )
        if params.min_count > 0:
            logger.info("Selecting words with >= %i occurrences ..." % params.min_count)
            dico.min_count(params.min_count)
            data["sentences"][data["sentences"] >= len(dico)] = dico.index(UNK_WORD)
            unk_count = (data["sentences"] == dico.index(UNK_WORD)).sum()
            logger.info(
                "Now %i unknown words covering %.2f%% of the data."
                % (
                    unk_count,
                    100.0
                    * unk_count
                    / (len(data["sentences"]) - len(data["positions"])),
                )
            )
        if (data["sentences"].dtype == np.int32) and (len(dico) < 1 << 16):
            logger.info("Less than 65536 words. Moving data from int32 to uint16 ...")
            data["sentences"] = data["sentences"].astype(np.uint16)
    return data


def load_binarized(path, params):
    """
    Load a binarized dataset.
    """
    assert path.endswith(".pth")
    if params.debug_train:
        path = path.replace("train", "valid")
    if getattr(params, "multi_gpu", False):
        assert params.split_data_accross_gpu in ["local", "global"]
        if params.split_data_accross_gpu == "local":
            split_path = "%s.%i.pth" % (path[:-4], params.local_rank)
        else:
            split_path = "%s.%i.pth" % (path[:-4], params.global_rank)

        if os.path.isfile(split_path):
            assert params.split_data is False
            path = split_path
    if not os.path.isfile(path):
        path = "%s.%i.pth" % (path[:-4], 0)
    assert os.path.isfile(path), path
    logger.info("Loading data from %s ..." % path)
    data = torch.load(path)
    data = process_binarized(data, params)
    return data


def set_dico_parameters(params, data, dico):
    """
    Update dictionary parameters.
    """
    if dico is None:
        return
    if "dico" in data:
        assert data["dico"] == dico
    else:
        data["dico"] = dico
    n_words = len(dico)
    bos_index = dico.index(BOS_WORD)
    eos_index = dico.index(EOS_WORD)
    pad_index = dico.index(PAD_WORD)
    unk_index = dico.index(UNK_WORD)
    mask_index = dico.index(MASK_WORD)
    if hasattr(params, "bos_index"):
        assert params.n_words == n_words
        assert params.bos_index == bos_index
        assert params.eos_index == eos_index
        assert params.pad_index == pad_index
        assert params.unk_index == unk_index
        assert params.mask_index == mask_index
    else:
        params.n_words = n_words
        params.bos_index = bos_index
        params.eos_index = eos_index
        params.pad_index = pad_index
        params.unk_index = unk_index
        params.mask_index = mask_index
    params.sep_index = dico.index("|")


def load_mono_data(params, data):
    """
    Load monolingual data.
    """
    data["mono"] = {}
    data["mono_stream"] = {}

    for lang in params.mono_dataset.keys():

        logger.info("============ Monolingual data (%s)" % lang)

        assert lang in params.langs and lang not in data["mono"]
        data["mono"][lang] = {}
        data["mono_stream"][lang] = {}

        for splt, data_path in params.mono_dataset[lang].items():
            if splt == SELF_TRAINED and lang not in params.st_src_langs:
                # continue if not doing self training for this language
                continue
            # no need to load training data for evaluation
            if splt in TRAIN_SPLITS and params.eval_only:
                continue
            # load data / update dictionary parameters / update data
            mono_data = load_binarized(data_path, params)
            set_dico_parameters(params, data, mono_data["dico"])

            # create stream dataset
            bs = params.batch_size if splt == "train" else 1
            data["mono_stream"][lang][splt] = StreamDataset(
                mono_data["sentences"], mono_data["positions"], bs, params
            )

            # if there are several processes on the same machine, we can split the dataset
            if (
                splt in TRAIN_SPLITS
                and params.split_data
                and 1
                < params.n_gpu_per_node
                <= data["mono_stream"][lang][splt].n_batches
            ):
                n_batches = (
                    data["mono_stream"][lang][splt].n_batches // params.n_gpu_per_node
                )
                a = n_batches * params.local_rank
                b = n_batches * params.local_rank + n_batches
                data["mono_stream"][lang][splt].select_data(a, b)

            # for denoising auto-encoding and online back-translation, we need a non-stream (batched) dataset
            if (
                lang in params.ae_steps
                or lang in params.bt_src_langs
                or lang
                in [l1 for l1, l2 in params.cmt_steps]
                + [l1 for l1, l2 in params.disc_steps]
                or (lang in params.st_src_langs and splt == SELF_TRAINED)
            ):

                # create batched dataset
                dataset = Dataset(
                    mono_data["sentences"],
                    mono_data["positions"],
                    params,
                    has_sentence_ids=(splt, (lang,)) in params.has_sentence_ids,
                    unit_tests_st=splt == SELF_TRAINED,
                )
                # remove empty and too long sentences
                if splt in TRAIN_SPLITS:
                    dataset.remove_empty_sentences()
                    dataset.remove_long_sentences(params.max_len)
                if splt == SELF_TRAINED:
                    dataset.compute_st_scores(params, data["dico"])
                    data[f"java_st_unit_tests"] = dataset.unit_tests
                    data[f"java_st_tests_scores"] = dataset.st_tests_scores

                # if there are several processes on the same machine, we can split the dataset
                if (
                    splt in TRAIN_SPLITS
                    and params.n_gpu_per_node > 1
                    and params.split_data
                ):
                    n_sent = len(dataset) // params.n_gpu_per_node
                    a = n_sent * params.local_rank
                    b = n_sent * params.local_rank + n_sent
                    dataset.select_data(a, b)

                data["mono"][lang][splt] = dataset

            logger.info("")

    logger.info("")


def load_para_data(params, data):
    """
    Load parallel data.
    """
    data["para"] = {}

    required_para_train = set(
        params.clm_steps
        + params.mlm_steps
        + params.mt_steps
        + params.mt_spans_steps
        + params.do_steps
        + params.classif_steps
    )

    for key in params.para_dataset.keys():
        span = None
        if len(key) == 2:
            src, tgt = key
        else:
            src, tgt, span = key
        if span is None:
            logger.info("============ Parallel data (%s-%s)" % (src, tgt))
        else:
            logger.info("============ Parallel data (%s/%s-%s)" % (src, span, tgt))

        assert key not in data["para"]
        data["para"][key] = {}

        for splt in DATASET_SPLITS:

            # no need to load training data for evaluation
            if splt in TRAIN_SPLITS and params.eval_only:
                continue

            # for back-translation, we can't load training data
            if splt == "train" and (
                (
                    span is None
                    and (src, tgt) not in required_para_train
                    and (tgt, src) not in required_para_train
                )
                or (
                    span is not None
                    and (src, tgt, span) not in required_para_train
                    and (tgt, src, span) not in required_para_train
                )
            ):
                continue

            # load binarized datasets
            paths = params.para_dataset[key][splt]
            span_path = None
            if span is None:
                src_path, tgt_path = paths
            else:
                src_path, tgt_path, span_path = paths

            src_data = load_binarized(src_path, params)
            tgt_data = load_binarized(tgt_path, params)
            span_data = load_binarized(span_path, params) if span_path else None

            # update dictionary parameters
            set_dico_parameters(params, data, src_data["dico"])
            set_dico_parameters(params, data, tgt_data["dico"])
            if span_data is not None:
                set_dico_parameters(params, data, span_data["dico"])

            sent_list = [src_data["sentences"], tgt_data["sentences"]]
            pos_list = [src_data["positions"], tgt_data["positions"]]
            if span_data is not None:
                sent_list.append(span_data["sentences"])
                pos_list.append(span_data["positions"])
            dataset = ParallelDataset(
                sent_list,
                pos_list,
                params,
                span_prediction=tgt_data["dico"] is None,
                has_sentence_ids=(splt, (src, tgt)) in params.has_sentence_ids,
            )

            # remove empty and too long sentences
            # if splt == 'train':
            dataset.remove_empty_sentences()
            dataset.remove_long_sentences(params.max_len)

            # for validation and test set, enumerate sentence per sentence
            if splt != "train":
                dataset.tokens_per_batch = -1

            # if there are several processes on the same machine, we can split the dataset
            if splt in TRAIN_SPLITS and params.n_gpu_per_node > 1 and params.split_data:
                n_sent = len(dataset) // params.n_gpu_per_node
                a = n_sent * params.local_rank
                b = n_sent * params.local_rank + n_sent
                dataset.select_data(a, b)
            if span is None:
                data["para"][(src, tgt)][splt] = dataset
            else:
                data["para"][(src, tgt, span)][splt] = dataset
            logger.info("")

    logger.info("")


def check_data_params(params):
    """
    Check datasets parameters.
    """
    # data path
    assert os.path.isdir(params.data_path), params.data_path

    # check languages
    params.langs = params.lgs.split("-") if params.lgs != "debug" else ["en"]
    assert len(params.langs) == len(set(params.langs)) >= 1, [
        l for l in params.langs if params.langs.count(l) >= 2
    ]

    # assert sorted(params.langs) == params.langs
    params.id2lang = {k: v for k, v in enumerate(sorted(params.langs))}
    params.lang2id = {k: v for v, k in params.id2lang.items()}
    params.n_langs = len(params.langs)
    if params.lgs_id_mapping != "":
        mappings = params.lgs_id_mapping.split(",")
        for m in mappings:
            split = m.split(":")
            assert len(split) == 2, f"Cannot parse {m} in {params.lgs_id_mapping}"
            source, dest = split
            assert (
                source in params.langs
            ), f"unknown source {source} from {m}. Not part of the languages in {params.langs}"
            assert (
                dest in params.langs
            ), f"unknown destination language {dest} from {m}. Not part of the languages in {params.langs}"
            params.lang2id[source] = params.lang2id[dest]

    # CLM steps
    clm_steps = [s.split("-") for s in params.clm_steps.split(",") if len(s) > 0]
    params.clm_steps = [(s[0], None) if len(s) == 1 else tuple(s) for s in clm_steps]
    assert all(
        [
            (l1 in params.langs) and (l2 in params.langs or l2 is None)
            for l1, l2 in params.clm_steps
        ]
    )
    assert len(params.clm_steps) == len(set(params.clm_steps))

    # MLM / TLM steps
    mlm_steps = [s.split("-") for s in params.mlm_steps.split(",") if len(s) > 0]
    params.mlm_steps = [(s[0], None) if len(s) == 1 else tuple(s) for s in mlm_steps]
    assert all(
        [
            (l1 in params.langs) and (l2 in params.langs or l2 is None)
            for l1, l2 in params.mlm_steps
        ]
    )
    assert len(params.mlm_steps) == len(set(params.mlm_steps))

    # machine translation steps
    params.mt_steps = [
        tuple(s.split("-")) for s in params.mt_steps.split(",") if len(s) > 0
    ]

    assert all([len(x) == 2 for x in params.mt_steps])
    assert all(
        [l1 in params.langs and l2 in params.langs for l1, l2 in params.mt_steps]
    )
    assert all([l1 != l2 for l1, l2 in params.mt_steps])
    assert len(params.mt_steps) == len(set(params.mt_steps))

    params.mt_spans_steps = [
        tuple(s.split("-")) for s in params.mt_spans_steps.split(",") if len(s) > 0
    ]
    assert all((len(split) == 3 for split in params.mt_spans_steps))
    assert all(
        [l1 != l2 and l1 != l3 and l2 != l3 for l1, l2, l3 in params.mt_spans_steps]
    )
    assert len(params.mt_spans_steps) == len(set(params.mt_spans_steps))
    assert (
        len(params.mt_steps) + len(params.mt_spans_steps) == 0
        or not params.encoder_only
    )

    assert (
        len(params.mt_spans_steps) > 0
    ) == params.spans_emb_encoder, f"mt_spans steps but spans are not used or trying to use spans without spans steps {len(params.mt_spans_steps)}, {params.spans_emb_encoder}"

    # do steps
    params.do_steps = [
        tuple(s.split("-")) for s in params.do_steps.split(",") if len(s) > 0
    ]
    assert all([len(x) == 2 for x in params.do_steps])
    assert all(
        [l1 in params.langs and l2 in params.langs for l1, l2 in params.do_steps]
    )
    assert all([l1 != l2 for l1, l2 in params.do_steps])
    assert len(params.do_steps) == len(set(params.do_steps))

    # classification steps
    params.classif_steps = [
        tuple(s.split("-")) for s in params.classif_steps.split(",") if len(s) > 0
    ]
    assert all([len(x) == 2 for x in params.classif_steps])
    assert all([l1 in params.langs for l1, l2 in params.classif_steps])
    assert all([l1 != l2 for l1, l2 in params.classif_steps])
    assert len(params.classif_steps) == len(set(params.classif_steps))
    assert (
        len(params.classif_steps) + len(params.mt_spans_steps) == 0
        or not params.n_classes_classif <= 0
    )
    params.use_classifier = True if len(params.classif_steps) > 0 else False

    # denoising auto-encoder steps
    params.ae_steps = [s for s in params.ae_steps.split(",") if len(s) > 0]
    assert all([lang in params.langs for lang in params.ae_steps])
    assert len(params.ae_steps) == len(set(params.ae_steps))
    assert len(params.ae_steps) == 0 or not params.encoder_only

    # back-translation steps
    params.bt_steps = [
        tuple(s.split("-")) for s in params.bt_steps.split(",") if len(s) > 0
    ]
    assert all([len(x) == 3 for x in params.bt_steps])
    assert all(
        [
            l1 in params.langs and l2 in params.langs and l3 in params.langs
            for l1, l2, l3 in params.bt_steps
        ]
    )
    assert all([l1 == l3 and l1 != l2 for l1, l2, l3 in params.bt_steps])
    assert len(params.bt_steps) == len(set(params.bt_steps))
    assert len(params.bt_steps) == 0 or not params.encoder_only
    params.bt_src_langs = [l1 for l1, _, _ in params.bt_steps]

    # self-training steps
    params.st_steps = [
        (s.split("-")[0], tuple(s.split("-")[1].split("|")))
        for s in params.st_steps.split(",")
        if len(s) > 0
    ]
    assert all([len(x) == 2 for x in params.st_steps])

    assert all(
        [
            l1 in params.langs and all([l2 in params.langs for l2 in langs2])
            for l1, langs2 in params.st_steps
        ]
    ), params.st_steps
    assert all([l1 != l2 for l1, langs2 in params.st_steps for l2 in langs2])
    assert len(params.st_steps) == len(set(params.st_steps))
    assert all([len(langs2) > 0 for l1, langs2 in params.st_steps]), params.st_steps
    params.st_src_langs = [l1 for l1, _ in params.st_steps]
    params.st_tgt_langs = list(
        set([l2 for _, langs2 in params.st_steps for l2 in langs2])
    )
    if len(params.st_src_langs) > 0:
        logger.info(f"st source langs: {params.st_src_langs}")
        logger.info(f"st target langs: {params.st_tgt_langs}")
        # unit tests path
        assert os.path.isfile(params.unit_tests_path), params.unit_tests_path

    # check monolingual datasets
    required_mono = set(
        [l1 for l1, l2 in (params.mlm_steps + params.clm_steps) if l2 is None]
        + params.ae_steps
        + params.bt_src_langs
    )
    params.mono_dataset = {
        lang: {
            splt: os.path.join(params.data_path, "%s.%s.pth" % (splt, lang))
            for splt in DATASET_SPLITS
        }
        for lang in params.langs
        if lang in required_mono
    }
    for lang in params.st_src_langs:
        if lang not in params.mono_dataset:
            params.mono_dataset[lang] = dict()
        params.mono_dataset[lang][SELF_TRAINED] = os.path.join(
            params.data_path, "%s.%s.pth" % (SELF_TRAINED, lang)
        )
    for paths in params.mono_dataset.values():
        for p in paths.values():
            if not os.path.isfile(p):
                logger.error(f"{p} not found")

    if not params.eval_only:
        assert all(
            [
                all(
                    [
                        os.path.isfile(p) or os.path.isfile(p.replace("pth", "0.pth"))
                        for p in paths.values()
                    ]
                )
                for paths in params.mono_dataset.values()
            ]
        ), [
            [
                p
                for p in paths.values()
                if not (os.path.isfile(p) or os.path.isfile(p.replace("pth", "0.pth")))
            ]
            for paths in params.mono_dataset.values()
        ]
    assert isinstance(
        params.n_sentences_eval, int
    ), f"n_sentences_eval was {params.n_sentences_eval}, it should be an int"
    # check parallel datasets
    required_para_train = set(
        params.clm_steps
        + params.mlm_steps
        + params.mt_steps
        + params.classif_steps
        + params.do_steps
    )
    required_para = (
        required_para_train
        | set([(l2, l3) for _, l2, l3 in params.bt_steps])
        | set([(l1, l2) for l1, langs2 in params.st_steps for l2 in langs2])
        | set([(l2, l1) for l1, langs2 in params.st_steps for l2 in langs2])
        | set(
            [
                (l2_1, l2_2)
                for l1, langs2 in params.st_steps
                for l2_1 in langs2
                for l2_2 in langs2
                if l2_1 != l2_2
            ]
        )
    )

    params.para_dataset = {
        (src, tgt): {
            splt: (
                os.path.join(
                    params.data_path, "%s.%s-%s.%s.pth" % (splt, src, tgt, src)
                ),
                os.path.join(
                    params.data_path, "%s.%s-%s.%s.pth" % (splt, src, tgt, tgt)
                ),
            )
            for splt in DATASET_SPLITS
            if splt != "train"
            or (src, tgt) in required_para_train
            or (tgt, src) in required_para_train
        }
        for src in params.langs
        for tgt in params.langs
        if src < tgt and ((src, tgt) in required_para or (tgt, src) in required_para)
    }
    for lang, label in params.classif_steps:
        params.para_dataset[(lang, label)] = {
            splt: (
                os.path.join(
                    params.data_path, "%s.%s-%s.%s.pth" % (splt, lang, label, lang)
                ),
                os.path.join(
                    params.data_path, "%s.%s-%s.%s.pth" % (splt, lang, label, label)
                ),
            )
            for splt in DATASET_SPLITS
        }

    for lang1, lang2, span in params.mt_spans_steps:
        params.para_dataset[(lang1, lang2, span)] = {
            splt: (
                os.path.join(
                    params.data_path, "%s.%s-%s.%s.pth" % (splt, lang1, lang2, lang1)
                ),
                os.path.join(
                    params.data_path, "%s.%s-%s.%s.pth" % (splt, lang1, lang2, lang2)
                ),
                os.path.join(
                    params.data_path, "%s.%s-%s.%s.pth" % (splt, lang1, span, span)
                ),
            )
            for splt in DATASET_SPLITS
        }

    for step_paths in params.para_dataset.values():
        for paths in step_paths.values():
            for p in paths:
                if not os.path.isfile(p):
                    logger.error(f"{p} not found")

    params.validation_metrics = params.validation_metrics.replace(
        "#obf_proba", str(params.obf_proba)
    )
    params.stopping_criterion = params.stopping_criterion.replace(
        "#obf_proba", str(params.obf_proba)
    )

    # parse which datasets should have sentence ids
    params.has_sentence_ids = (
        [s.split("|") for s in params.has_sentence_ids.split(",")]
        if params.has_sentence_ids != ""
        else []
    )

    assert all([len(x) == 2 for x in params.has_sentence_ids]), params.has_sentence_ids
    params.has_sentence_ids = [
        (split, tuple(langs.split("-"))) for split, langs in params.has_sentence_ids
    ]
    assert all(
        [len(langs) == 1 or len(langs) == 2 for split, langs in params.has_sentence_ids]
    ), params.has_sentence_ids
    for split, langs in params.has_sentence_ids:
        if langs == ("para",) or langs == ("all",):
            params.has_sentence_ids += [
                (split, langs) for langs in params.para_dataset.keys()
            ]
        if langs == ("mono",) or langs == ("all",):
            params.has_sentence_ids += [
                (split, (lang,)) for lang in params.mono_dataset.keys()
            ]
    assert all(
        [
            all([lang in params.langs + ["para", "mono", "all"] for lang in langs])
            for split, langs in params.has_sentence_ids
        ]
    ), params.has_sentence_ids
    assert len(set(params.has_sentence_ids)) == len(params.has_sentence_ids)

    assert (
        len(params.mono_dataset) > 0 or len(params.para_dataset) > 0
    ), "No dataset to be loaded, you probably forget to set a training step."
    # assert all([all([os.path.isfile(p1) and os.path.isfile(p2) for p1, p2 in paths.values()]) for paths in params.para_dataset.values()])

    # check that we can evaluate on BLEU
    # assert params.eval_bleu is False or len(params.mt_steps + params.bt_steps) > 0


def load_data(params):
    """
    Load monolingual data.
    The returned dictionary contains:
        - dico (dictionary)
        - vocab (FloatTensor)
        - train / valid / test (monolingual datasets)
    """
    data = {}

    # monolingual datasets
    load_mono_data(params, data)

    # parallel datasets
    load_para_data(params, data)

    # monolingual data summary
    logger.info("============ Data summary")
    for lang, v in data["mono_stream"].items():
        for data_set in v.keys():
            logger.info(
                "{: <18} - {: >5} - {: >12}:{: >10}".format(
                    "Monolingual data", data_set, lang, len(v[data_set])
                )
            )

    # parallel data summary
    for key, v in data["para"].items():
        for data_set in v.keys():
            logger.info(
                "{: <18} - {: >5} - {: >12}:{: >10}".format(
                    "Parallel data", data_set, "%s" % "-".join(key), len(v[data_set])
                )
            )

    logger.info("")
    return data
