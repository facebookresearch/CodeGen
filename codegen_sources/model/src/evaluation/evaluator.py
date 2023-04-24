# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import json
import os
import subprocess
import time
import typing as tp
from collections import OrderedDict, defaultdict
from concurrent.futures.process import ProcessPoolExecutor
from logging import getLogger
from pathlib import Path

import fastBPE
import numpy as np
import torch
from sklearn.metrics import roc_auc_score, average_precision_score

from codegen_sources.IR_tools.utils_ir import code_to_ir, ERROR_MESSAGE
from codegen_sources.preprocessing.lang_processors import LangProcessor, IRProcessor
from .comp_acc_computation import (
    load_evosuite_transcoder_tests,
    eval_function_output,
    GFG,
    FAILED_IR_COMP_,
    init_eval_scripts_folder,
    CODENET_EVAL_FOLDER,
    EVAL_SCRIPT_FOLDER,
)
from ..data.loader import DATASET_SPLITS
from ..trainer import get_programming_language_name
from ..utils import (
    to_cuda,
    restore_segmentation,
    concat_batches,
    show_batch,
    add_noise,
    convert_to_text,
    REPO_ROOT,
    restore_segmentation_sentence,
    read_file_lines,
)
from .subtoken_score import run_subtoken_score
import sys

from ..vizualization_utils import vizualize_do_files, vizualize_translated_files

sys.path.append(str(REPO_ROOT))

PathLike = tp.Union[Path, str]

SRC_ST_LANGS = "java"

TARGET_ST_LANG = {"cpp", "python"}

EVAL_OBF_PROBAS: tp.List[float] = []

BLEU_SCRIPT_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "multi-bleu.perl"
)
EVAL_DATASET_SPLITS = [ds for ds in DATASET_SPLITS if ds != "train"]
assert os.path.isfile(BLEU_SCRIPT_PATH)
ROOT_FOLDER = Path(__file__).parents[4]

logger = getLogger()


class Evaluator(object):
    def __init__(self, trainer, data, params) -> None:
        """
        Initialize evaluator.
        """
        self.trainer = trainer
        self.data = data
        self.dico = data["dico"]
        self.params = params

        # create directory to store hypotheses, and reference files for BLEU evaluation
        if self.params.is_master:
            params.hyp_path = os.path.join(params.dump_path, "hypotheses")
            subprocess.Popen("mkdir -p %s" % params.hyp_path, shell=True).wait()
            params.eval_scripts_root = os.path.join(params.dump_path, "eval_scripts")
            subprocess.Popen(
                "mkdir -p %s" % params.eval_scripts_root, shell=True
            ).wait()
            self.params.ref_paths = {}
            self.params.id_paths = {}
            self.params.eval_scripts_folders = {}
            if params.eval_bleu or params.eval_subtoken_score:
                self.create_reference_files()
            if self.params.eval_st:
                logger.info("Loading evosuite tests")
                self.evosuite_tests_dico = load_evosuite_transcoder_tests()
            else:
                self.evosuite_tests_dico = None

    def get_iterator(
        self, data_set, lang1, lang2=None, stream=False, span=None, subsample=1000,
    ):
        """
        Create a new iterator for a dataset.
        """
        assert data_set in EVAL_DATASET_SPLITS
        assert lang1 in self.params.langs
        assert (
            lang2 is None
            or lang2 in self.params.langs
            or (lang1, lang2) in self.params.classif_steps
        )
        assert stream is False or lang2 is None

        n_sentences = self.params.n_sentences_eval

        if lang2 is None or lang2 == lang1:
            key = lang1 if span is None else (lang1, span)
            if stream and lang2 is None:
                iterator = self.data["mono_stream"][key][data_set].get_iterator(
                    shuffle=False, subsample=subsample
                )
            else:
                iterator = self.data["mono"][key][data_set].get_iterator(
                    tokens_per_batch=self.params.eval_tokens_per_batch,
                    max_batch_size=-1,
                    shuffle=False,
                    group_by_size=True,
                    n_sentences=n_sentences,
                )
        else:
            assert stream is False
            _lang1, _lang2 = (lang1, lang2) if lang1 < lang2 else (lang2, lang1)
            key = (_lang1, _lang2) if span is None else (_lang1, _lang2, span)
            iterator = self.data["para"][key][data_set].get_iterator(
                shuffle=False,
                group_by_size=True,
                n_sentences=n_sentences,
                tokens_per_batch=self.params.eval_tokens_per_batch,
                max_batch_size=-1,
            )
        for batch in iterator:
            yield batch if lang2 is None or lang1 == lang2 or lang1 <= lang2 else batch[
                ::-1
            ]

    def create_reference_files(self):
        """
        Create reference files for BLEU evaluation.
        """
        params = self.params
        for key in list(self.data["para"].keys()) + [
            (l, l) for l in self.params.eval_computation_pivot_self
        ]:
            span = None
            if len(key) == 3:
                lang1, lang2, span = key
            else:
                assert len(key) == 2
                lang1, lang2 = key
            assert lang1 < lang2 or (
                lang1 == lang2 and lang1 in self.params.eval_computation_pivot_self
            ), (lang1, lang2)

            for data_set in EVAL_DATASET_SPLITS:
                init_eval_scripts_folder(data_set, lang1, lang2, params)
                init_eval_scripts_folder(data_set, lang2, lang1, params)

                # define data paths
                lang1_path = os.path.join(
                    params.hyp_path,
                    "ref.{0}-{1}.{2}.txt".format(lang2, lang1, data_set),
                )
                lang2_path = os.path.join(
                    params.hyp_path,
                    "ref.{0}-{1}.{2}.txt".format(lang1, lang2, data_set),
                )
                spans_path = os.path.join(
                    params.hyp_path,
                    "ref.{0}-{1}-{3}.{2}.txt".format(lang1, lang2, span, data_set),
                )
                id_path = os.path.join(
                    params.hyp_path,
                    "ids.{0}-{1}.{2}.txt".format(lang1, lang2, data_set),
                )
                # store data paths
                params.ref_paths[(lang2, lang1, data_set)] = lang1_path
                params.ref_paths[(lang1, lang2, data_set)] = lang2_path
                params.id_paths[(lang1, lang2, data_set)] = id_path
                params.id_paths[(lang2, lang1, data_set)] = id_path

                # text sentences
                lang1_txt = []
                lang2_txt = []

                id_txt = []
                spans = []
                has_sent_ids = None
                # convert to text
                for i, batch in enumerate(
                    self.get_iterator(data_set, lang1, lang2, span=span)
                ):
                    if len(batch) == 2:
                        (sent1, len1, id1, lenid1), (sent2, len2, id2, lenid2) = batch
                    elif len(batch) == 4:
                        sent1, len1, id1, lenid1 = batch
                        sent2, len2, id2, lenid2 = batch
                    else:
                        (
                            (sent1, len1, id1, lenid1),
                            (sent2, len2, id2, lenid2),
                            (span_batch, len_span, _, _),
                        ) = batch
                        spans.extend(list(span_batch.T))
                    lang1_txt.extend(convert_to_text(sent1, len1, self.dico, params))
                    lang2_txt.extend(convert_to_text(sent2, len2, self.dico, params))
                    has_sent_ids = id1 is not None and id2 is not None
                    if has_sent_ids:
                        assert id1.equal(id2) and lenid1.equal(lenid2)
                        id_txt.extend(convert_to_text(id1, lenid1, self.dico, params))

                # replace <unk> by <<unk>> as these tokens cannot be counted in BLEU
                lang1_txt = [x.replace("<unk>", "<<unk>>") for x in lang1_txt]
                lang2_txt = [x.replace("<unk>", "<<unk>>") for x in lang2_txt]

                # export hypothesis
                with open(lang1_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lang1_txt) + "\n")
                with open(lang2_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lang2_txt) + "\n")
                if len(spans) > 0:
                    with open(spans_path, "w", encoding="utf-8") as f:
                        f.write("\n".join([str(s) for s in spans]) + "\n")

                # restore original segmentation
                restore_segmentation(
                    lang1_path,
                    tokenization_mode=params.tokenization_mode,
                    single_line=True,
                    sentencepiece_model_path=params.sentencepiece_model_path,
                )
                restore_segmentation(
                    lang2_path,
                    tokenization_mode=params.tokenization_mode,
                    single_line=True,
                    sentencepiece_model_path=params.sentencepiece_model_path,
                )

                if has_sent_ids:
                    with open(id_path, "w", encoding="utf-8") as f:
                        f.write("\n".join(id_txt) + "\n")
                    restore_segmentation(
                        id_path,
                        tokenization_mode=params.tokenization_mode,
                        single_line=True,
                        sentencepiece_model_path=params.sentencepiece_model_path,
                    )

    def mask_out(self, x, lengths, rng):
        """
        Decide of random words to mask out.
        We specify the random generator to ensure that the test is the same at each epoch.
        """
        params = self.params
        slen, bs = x.size()

        # words to predict - be sure there is at least one word per sentence
        to_predict = rng.rand(slen, bs) <= params.word_pred
        to_predict[0] = 0
        for i in range(bs):
            to_predict[lengths[i] - 1 :, i] = 0
            if not np.any(to_predict[: lengths[i] - 1, i]):
                v = rng.randint(1, lengths[i] - 1)
                to_predict[v, i] = 1
        pred_mask = torch.from_numpy(to_predict.astype(np.uint8))
        pred_mask = pred_mask == 1

        # generate possible targets / update x input
        _x_real = x[pred_mask]
        _x_mask = _x_real.clone().fill_(params.mask_index)
        x = x.masked_scatter(pred_mask, _x_mask)

        assert 0 <= x.min() <= x.max() < params.n_words
        assert x.size() == (slen, bs)
        assert pred_mask.size() == (slen, bs)

        return x, _x_real, pred_mask

    def run_all_evals(self, trainer):
        """
        Run all evaluations.
        """
        params = self.params
        scores = OrderedDict({"epoch": trainer.epoch})
        deobf_probas_to_eval = [1 - x for x in EVAL_OBF_PROBAS]
        deobfuscation_proba = 1 - params.obf_proba
        if deobfuscation_proba not in deobf_probas_to_eval:
            deobf_probas_to_eval.append(deobfuscation_proba)

        with torch.no_grad():

            for data_set in EVAL_DATASET_SPLITS:

                # causal prediction task (evaluate perplexity and accuracy)
                for lang1, lang2 in params.clm_steps:
                    self.evaluate_clm(scores, data_set, lang1, lang2)

                # prediction task (evaluate perplexity and accuracy)
                for lang1, lang2 in params.mlm_steps:
                    self.evaluate_mlm(scores, data_set, lang1, lang2)

                # machine translation task (evaluate perplexity and accuracy)
                for lang1 in sorted(params.eval_computation_pivot_self):
                    self.evaluate_mt(
                        scores,
                        data_set,
                        lang1,
                        lang1,
                        params.eval_bleu,
                        False,
                        True,
                        params.eval_subtoken_score,
                        span=None,
                    )
                set_keys = set(
                    params.mt_steps
                    + [(l1, l2) for l1, langs2 in params.st_steps for l2 in langs2]
                    + [(l2, l1) for l1, langs2 in params.st_steps for l2 in langs2]
                    + [
                        (l2_1, l2_2)
                        for l1, langs2 in params.st_steps
                        for l2_1 in langs2
                        for l2_2 in langs2
                        if l2_1 != l2_2
                    ]
                    + params.mt_spans_steps
                    + params.eval_computation
                    + params.eval_computation_pivot
                )
                if params.eval_bt_pairs:
                    set_keys |= set([(l2, l3) for _, l2, l3 in params.bt_steps])

                for i_set, keys in enumerate(sorted(set_keys)):
                    print(f"Evaluating pair {i_set + 1} / {len(set_keys)}")
                    spans = None
                    assert len(keys) == 2 or len(keys) == 3
                    lang1, lang2 = keys[0], keys[1]
                    if len(keys) == 3:
                        spans = keys[2]
                    self.evaluate_mt(
                        scores,
                        data_set,
                        lang1,
                        lang2,
                        params.eval_bleu,
                        (lang1, lang2) in params.eval_computation,
                        (lang1, lang2) in params.eval_computation_pivot,
                        params.eval_subtoken_score,
                        spans,
                        eval_ir_similarity=(lang1, lang2) in params.eval_ir_similarity,
                    )
                if self.params.eval_denoising:
                    for lang in sorted(set(params.ae_steps)):
                        assert lang in params.langs, lang
                        self.evaluate_mt(
                            scores,
                            data_set,
                            lang,
                            lang,
                            eval_bleu=False,
                            eval_computation=False,
                            eval_computation_pivot=False,
                            eval_subtoken_score=False,
                            span=None,
                        )

                # machine translation task (evaluate perplexity and accuracy)
                for lang1, lang2 in sorted(set(params.do_steps)):
                    assert len(deobf_probas_to_eval) == len(
                        set(deobf_probas_to_eval)
                    ), f"deobf_probas_to_eval should have no duplicates, was {deobf_probas_to_eval}"
                    self.evaluate_mt(
                        scores,
                        data_set,
                        lang1,
                        lang2,
                        params.eval_bleu,
                        eval_computation=False,
                        eval_computation_pivot=False,
                        eval_subtoken_score=params.eval_subtoken_score,
                        span=None,
                        deobfuscate=True,
                        deobfuscate_probas=deobf_probas_to_eval,
                    )

                # prediction task (evaluate perplexity and accuracy)
                for lang1, lang2 in sorted(params.classif_steps):
                    self.evaluate_classif(scores, data_set, lang1, lang2)

                # report average metrics per language
                if len(params.do_steps) > 0 and params.is_master:
                    for obfuscation_proba in deobf_probas_to_eval:
                        for score_type in ["precision", "recall", "F1"]:
                            scores[
                                "%s_obf_proba_%s_mt_subtoken_%s"
                                % (data_set, 1 - obfuscation_proba, score_type)
                            ] = np.mean(
                                [
                                    scores[
                                        "%s_%s_mt_subtoken_%s"
                                        % (
                                            data_set,
                                            get_l1l2_string(
                                                lang1, lang2, obfuscation_proba
                                            ),
                                            score_type,
                                        )
                                    ]
                                    for lang1, lang2 in params.do_steps
                                ]
                            )
                _clm_mono = [l1 for (l1, l2) in params.clm_steps if l2 is None]
                if len(_clm_mono) > 0:
                    scores["%s_clm_ppl" % data_set] = np.mean(
                        [
                            scores["%s_%s_clm_ppl" % (data_set, lang)]
                            for lang in _clm_mono
                        ]
                    )
                    scores["%s_clm_acc" % data_set] = np.mean(
                        [
                            scores["%s_%s_clm_acc" % (data_set, lang)]
                            for lang in _clm_mono
                        ]
                    )
                _mlm_mono = [l1 for (l1, l2) in params.mlm_steps if l2 is None]
                if len(_mlm_mono) > 0:
                    scores["%s_mlm_ppl" % data_set] = np.mean(
                        [
                            scores["%s_%s_mlm_ppl" % (data_set, lang)]
                            for lang in _mlm_mono
                        ]
                    )
                    scores["%s_mlm_acc" % data_set] = np.mean(
                        [
                            scores["%s_%s_mlm_acc" % (data_set, lang)]
                            for lang in _mlm_mono
                        ]
                    )

        if params.is_master:
            logger.info(f"On GPU {params.global_rank}, scores computed \n\n")
            return scores
        else:
            return {}

    def eval_mode(self):
        [enc.eval() for enc in self.encoder]
        if self.decoder is not None:
            [dec.eval() for dec in self.decoder]

    def evaluate_clm(self, scores, data_set, lang1, lang2):
        """
        Evaluate perplexity and next word prediction accuracy.
        """
        params = self.params
        assert data_set in EVAL_DATASET_SPLITS
        assert lang1 in params.langs
        assert lang2 in params.langs or lang2 is None

        model = self.model[0] if params.encoder_only else self.decoder[0]
        model.eval()
        model = model.module if params.multi_gpu else model

        lang1_id = params.lang2id[lang1]
        lang2_id = params.lang2id[lang2] if lang2 is not None else None
        l1l2 = lang1 if lang2 is None else f"{lang1}-{lang2}"

        n_words = 0
        xe_loss = 0
        n_valid = 0

        n_bytes = 0
        valid_bytes = 0

        for batch in self.get_iterator(data_set, lang1, lang2, stream=(lang2 is None)):

            # batch
            if lang2 is None:
                x, lengths = batch
                positions = None
                langs = x.clone().fill_(lang1_id) if params.n_langs > 1 else None
            else:
                (sent1, len1), (sent2, len2) = batch
                x, lengths, positions, langs = concat_batches(
                    sent1,
                    len1,
                    lang1_id,
                    sent2,
                    len2,
                    lang2_id,
                    params.pad_index,
                    params.eos_index,
                    reset_positions=True,
                )

            # words to predict
            alen = torch.arange(lengths.max(), dtype=torch.long, device=lengths.device)
            pred_mask = alen[:, None] < lengths[None] - 1
            y = x[1:].masked_select(pred_mask[:-1])
            assert pred_mask.sum().item() == y.size(0)

            # cuda
            x, lengths, positions, langs, pred_mask, y = to_cuda(
                x, lengths, positions, langs, pred_mask, y
            )

            # forward / loss
            tensor = model(
                "fwd",
                x=x,
                lengths=lengths,
                positions=positions,
                langs=langs,
                causal=True,
            )
            word_scores, loss = model(
                "predict", tensor=tensor, pred_mask=pred_mask, y=y, get_scores=True
            )

            # update stats
            n_words += y.size(0)
            xe_loss += loss.item() * len(y)
            predictions = word_scores.max(1)[1]
            n_valid += (predictions == y).sum().item()
            gt_bytes = [self.dico.id2word[i.item()].encode("utf-8") for i in y]
            n_bytes += sum(len(b) for b in gt_bytes)
            pred_bytes = [
                self.dico.id2word[i.item()].encode("utf-8")
                for i in word_scores.max(1)[1]
            ]
            valid_bytes += sum(
                sum(1 if pred == gt else 0 for pred, gt in zip(pred_seq, gt_seq))
                for pred_seq, gt_seq in zip(pred_bytes, gt_bytes)
            )

        # log
        logger.info(
            "Found %i words in %s. %i were predicted correctly."
            % (n_words, data_set, n_valid)
        )

        logger.info(
            "Found %i bytes in %s. %i were predicted correctly."
            % (n_bytes, data_set, valid_bytes)
        )

        # compute perplexity and prediction accuracy
        ppl_name = "%s_%s_clm_ppl" % (data_set, l1l2)
        acc_name = "%s_%s_clm_acc" % (data_set, l1l2)
        byte_name = "%s_%s_clm_byte_acc" % (data_set, l1l2)
        scores[ppl_name] = np.exp(xe_loss / n_words)
        scores[acc_name] = 100.0 * n_valid / n_words
        scores[byte_name] = 100.0 * valid_bytes / n_bytes

    def evaluate_mlm(self, scores, data_set, lang1, lang2):
        """
        Evaluate perplexity and next word prediction accuracy.
        """
        params = self.params
        assert data_set in EVAL_DATASET_SPLITS
        assert lang1 in params.langs
        assert lang2 in params.langs or lang2 is None

        model = self.model[0] if params.encoder_only else self.encoder[0]
        model.eval()
        model = model.module if params.multi_gpu else model

        rng = np.random.RandomState(0)

        lang1_id = params.lang2id[lang1]
        lang2_id = params.lang2id[lang2] if lang2 is not None else None
        l1l2 = lang1 if lang2 is None else f"{lang1}_{lang2}"

        n_words = 0
        xe_loss = 0
        n_valid = 0

        for i, batch in enumerate(
            self.get_iterator(data_set, lang1, lang2, stream=(lang2 is None))
        ):
            if i > 50:
                break
            # batch
            if lang2 is None:
                x, lengths = batch
                positions = None
                langs = x.clone().fill_(lang1_id) if params.n_langs > 1 else None
            else:
                (sent1, len1, _, _), (sent2, len2, _, _) = batch
                x, lengths, positions, langs = concat_batches(
                    sent1,
                    len1,
                    lang1_id,
                    sent2,
                    len2,
                    lang2_id,
                    params.pad_index,
                    params.eos_index,
                    reset_positions=True,
                )

            # words to predict
            x, y, pred_mask = self.mask_out(x, lengths, rng)

            # log first batch of training
            if i < 1:
                show_batch(
                    logger,
                    [("masked source", x.transpose(0, 1))],
                    self.data["dico"],
                    self.params.tokenization_mode,
                    "Evaluation",
                    self.params.sentencepiece_model_path,
                )

            # cuda
            x, y, pred_mask, lengths, positions, langs = to_cuda(
                x, y, pred_mask, lengths, positions, langs
            )

            # forward / loss
            tensor = model(
                "fwd",
                x=x,
                lengths=lengths,
                positions=positions,
                langs=langs,
                causal=False,
            )
            word_scores, loss = model(
                "predict", tensor=tensor, pred_mask=pred_mask, y=y, get_scores=True
            )

            # update stats
            n_words += len(y)
            xe_loss += loss.item() * len(y)
            n_valid += (word_scores.max(1)[1] == y).sum().item()

        # compute perplexity and prediction accuracy
        ppl_name = "%s_%s_mlm_ppl" % (data_set, l1l2)
        acc_name = "%s_%s_mlm_acc" % (data_set, l1l2)
        scores[ppl_name] = np.exp(xe_loss / n_words) if n_words > 0 else 1e9
        scores[acc_name] = 100.0 * n_valid / n_words if n_words > 0 else 0.0

    def evaluate_classif(self, scores, data_set, lang1, lang2):
        params = self.params
        assert data_set in EVAL_DATASET_SPLITS
        assert lang1 in params.langs
        lang1_id = params.lang2id[lang1]

        model = self.model[0] if params.encoder_only else self.encoder[0]
        model.eval()
        model = model.module if params.multi_gpu else model
        assert self.classifier is not None
        classifier = self.classifier[0].eval()

        n_words = 0
        n_valid = 0
        labels = []
        word_probas = []
        n_words_by_cl = [0 for c in range(self.params.n_classes_classif)]
        n_valid_by_cl = [0 for c in range(self.params.n_classes_classif)]
        n_attribution_by_cl = [0 for c in range(self.params.n_classes_classif)]

        for batch in self.get_iterator(data_set, lang1, lang2, stream=False):
            (x1, len1, _, _), (y, len2, _, _) = batch
            pred_mask = (x1 != self.params.eos_index) * (x1 != self.params.pad_index)
            assert len1.equal(len2)
            langs1 = x1.clone().fill_(lang1_id)

            # cuda
            x1, len1, langs1, y = to_cuda(x1, len1, langs1, y)

            # encode source sentence
            enc1 = model("fwd", x=x1, lengths=len1, langs=langs1, causal=False)
            if self.params.fp16:
                enc1 = enc1.half()

            # classification + loss
            word_scores, loss = classifier(enc1, y, pred_mask)

            # update stats
            y_ = y[pred_mask].view(-1,)
            n_words += len(y_)
            n_valid += (word_scores.max(1)[1] == y_).sum().item()
            labels.extend(y_.cpu().numpy())
            word_probas.extend(word_scores.cpu().numpy())

            for cl in range(self.params.n_classes_classif):
                n_words_by_cl[cl] += (y_ == cl).sum().item()
                n_valid_by_cl[cl] += (
                    ((word_scores.max(1)[1] == y_) * (y_ == cl)).sum().item()
                )
                n_attribution_by_cl[cl] += (word_scores.max(1)[1] == cl).sum().item()

        if len(set(labels)) > 1:
            for target_label in range(self.params.n_classes_classif):
                roc_auc_name = "%s_%s-%s_roc_auc_label_cl%i" % (
                    data_set,
                    lang1,
                    lang2,
                    target_label,
                )
                new_labels = [1 if l == target_label else 0 for l in labels]
                word_level_scores = [wp[target_label] for wp in word_probas]
                scores[roc_auc_name] = roc_auc_score(new_labels, word_level_scores)

                pr_auc_name = "%s_%s-%s_pr_auc_cl%i" % (
                    data_set,
                    lang1,
                    lang2,
                    target_label,
                )
                scores[pr_auc_name] = average_precision_score(
                    new_labels, word_level_scores
                )

            roc_auc_name = "%s_%s-%s_roc_auc_label_all_changes" % (
                data_set,
                lang1,
                lang2,
            )
            new_labels = [1 if l > 0 else 0 for l in labels]
            word_level_scores = [1 - s[0] for s in word_probas]
            scores[roc_auc_name] = roc_auc_score(new_labels, word_level_scores)

            pr_auc_name = "%s_%s-%s_pr_auc_label_all_changes" % (data_set, lang1, lang2)
            scores[pr_auc_name] = average_precision_score(new_labels, word_level_scores)

        # compute perplexity and prediction accuracy
        class_proportion_name = "%s_%s-%s_class_proportion" % (data_set, lang1, lang2)
        acc_name = "%s_%s-%s_classif_acc" % (data_set, lang1, lang2)
        recall_name = "%s_%s-%s_classif_recall" % (data_set, lang1, lang2)
        precision_name = "%s_%s-%s_classif_precision" % (data_set, lang1, lang2)

        scores[class_proportion_name] = [
            (100.0 * x / n_words) if n_words > 0 else 0.0 for x in n_words_by_cl
        ]
        scores[acc_name] = (100.0 * n_valid / n_words) if n_words > 0 else 0.0
        # scores[recall_name] = [(100. * n_valid_by_cl[cl] / n_words_by_cl[cl]) if n_words_by_cl[cl] > 0 else 0 for cl in range(self.params.n_classes_classif)]
        # scores[precision_name] = [(100. * n_valid_by_cl[cl] / n_attribution_by_cl[cl]) if n_attribution_by_cl[cl] > 0 else 0 for cl in range(self.params.n_classes_classif)]

        for cl in range(params.n_classes_classif):
            scores[f"{recall_name}_{cl}"] = (
                100.0 * n_valid_by_cl[cl] / n_words_by_cl[cl]
                if n_words_by_cl[cl] > 0
                else 0
            )
        for cl in range(params.n_classes_classif):
            scores[f"{precision_name}_{cl}"] = (
                100.0 * n_valid_by_cl[cl] / n_attribution_by_cl[cl]
                if n_attribution_by_cl[cl] > 0
                else 0
            )


class SingleEvaluator(Evaluator):
    def __init__(self, trainer, data, params) -> None:
        """
        Build language model evaluator.
        """
        super().__init__(trainer, data, params)
        self.model = trainer.model
        if params.use_classifier:
            self.classifier = trainer.classifier


def gather_model_outputs(model_outputs_list):
    model_outputs = {}
    for k in ["n_words", "xe_loss", "n_valid"]:
        model_outputs[k] = sum(d.get(k, 0) for d in model_outputs_list)
    for k in ["hypothesis", "references", "sources", "computed_irs"]:
        model_outputs[k] = []  # First element of each list, then second...
        for i in range(len(model_outputs_list[0][k])):
            for d in model_outputs_list:
                if k not in d or len(d[k]) <= i:
                    continue
                model_outputs[k].extend(d[k][i])
    return model_outputs


class EncDecEvaluator(Evaluator):
    def __init__(self, trainer, data, params) -> None:
        """
        Build encoder / decoder evaluator.
        """
        super().__init__(trainer, data, params)
        self.encoder = trainer.encoder
        self.decoder = trainer.decoder

    def evaluate_mt(
        self,
        scores,
        data_set: str,
        lang1: str,
        lang2: str,
        eval_bleu: bool,
        eval_computation: bool,
        eval_computation_pivot: bool,
        eval_subtoken_score,
        span,
        deobfuscate=False,
        deobfuscate_probas=None,
        eval_ir_similarity=False,
    ):
        """
        Evaluate perplexity and next word prediction accuracy.
        """
        params = self.params
        assert data_set in EVAL_DATASET_SPLITS
        assert lang1 in params.langs
        assert lang2 in params.langs
        rng = np.random.RandomState(0)
        torch_rng = torch.Generator().manual_seed(0)

        do_eval = {
            "bleu": eval_bleu,
            "st": params.eval_st,
            "computation": eval_computation,
            "computation_pivot": eval_computation_pivot,
            "subtoken_score": eval_subtoken_score,
            "ir_similarity": eval_ir_similarity,
        }

        bpe_model = None
        if do_eval["computation_pivot"]:
            bpe_model = fastBPE.fastBPE(params.pivot_bpe_model)  # type: ignore
            logger.info(f"Computing pivot CA for {lang1} to {lang2}")

        # store hypothesis to compute BLEU score
        if params.eval_bleu_test_only:
            datasets_for_bleu = ["test"]
        else:
            datasets_for_bleu = [s for s in EVAL_DATASET_SPLITS if s != "train"]

        lang2_id = params.lang2id[lang2]

        self.eval_mode()
        encoder = self.encoder[0].module if params.multi_gpu else self.encoder[0]
        decoder = (
            self.decoder[lang2_id] if params.separate_decoders else self.decoder[0]
        )
        decoder = decoder.module if params.multi_gpu else decoder

        for deobfuscation_proba in (
            deobfuscate_probas if deobfuscate_probas is not None else [None]
        ):
            if deobfuscate:
                rng = np.random.RandomState(0)

            word_metrics: tp.Mapping[str, float] = defaultdict(float)
            text_files: tp.Mapping[str, tp.Any] = defaultdict(list)

            logger.info(
                f"{params.global_rank}: generating MT hypotheses {lang1} -> {lang2}"
            )
            time_start_generate = time.perf_counter()
            will_compute_bleu = (
                any(
                    do_eval[k]
                    for k in (
                        "bleu",
                        "computation",
                        "subtoken_score",
                        "computation_pivot",
                    )
                )
                and data_set in datasets_for_bleu
            )
            for i, batch in enumerate(
                self.get_iterator(
                    data_set, lang1, lang2 if lang2 != lang1 else None, span=span
                )
            ):
                if i % params.world_size != params.global_rank:
                    continue  # Distribute batches on all GPUs

                computed_irs_upd, ir_creation_errors = [], None
                show_example = i == 0
                seq1, seq2, spans = self.extract_batch(
                    lang1,
                    lang2,
                    batch,
                    rng,
                    torch_rng,
                    deobfuscate,
                    deobfuscation_proba,
                    params,
                    do_eval["computation_pivot"],
                )
                if seq1 is None:
                    continue
                if do_eval["computation_pivot"]:
                    seq1, computed_irs_upd, ir_creation_errors = self.sequence_to_ir(
                        seq1, lang1, params, bpe_model
                    )
                text_files["computed_irs"].append(computed_irs_upd)
                enc1, dec2 = self.do_forward(
                    encoder, decoder, seq1, seq2, spans, params.fp16
                )
                self.update_word_metrics(
                    word_metrics,
                    seq2,
                    decoder,
                    dec2,
                    do_eval["computation_pivot"],
                    ir_creation_errors,
                )
                self.update_text_files(
                    text_files,
                    decoder,
                    seq1,
                    seq2,
                    enc1,
                    params,
                    lang1,
                    lang2,
                    data_set,
                    will_compute_bleu,
                    do_eval["computation_pivot"],
                    ir_creation_errors,
                    show_example,
                )

            time_hyp_generated = time.perf_counter()
            logger.info(
                f"Timing: Generated hypotheses in {time_hyp_generated - time_start_generate:.2f}s"
            )

            model_outputs = {**word_metrics, **text_files}
            if params.world_size > 1:
                torch.distributed.barrier()
                model_outputs_list = [None for _ in range(params.world_size)]
                torch.distributed.all_gather_object(model_outputs_list, model_outputs)
            else:
                model_outputs_list = [model_outputs]  # type: ignore

            if not params.is_master:
                continue

            model_outputs = gather_model_outputs(model_outputs_list)
            self.compute_metrics(
                model_outputs,
                data_set,
                lang1,
                lang2,
                params,
                scores,
                deobfuscate,
                deobfuscation_proba,
                do_eval,
                datasets_for_bleu,
                will_compute_bleu,
            )
            logger.info(
                f"Timing: Computed metrics in {time.perf_counter() - time_hyp_generated:.2f}s"
            )

    def extract_batch(
        self,
        lang1,
        lang2,
        batch,
        rng,
        torch_rng,
        deobfuscate,
        deobfuscation_proba,
        params,
        eval_computation_pivot,
    ):
        spans = None
        assert len(batch) >= 2
        if len(batch) == 2:
            if lang1 == lang2:
                x2, len2 = batch
                x1, len1 = add_noise(
                    x2, len2, self.params, len(self.data["dico"]) - 1, rng, torch_rng,
                )
            else:
                (x1, len1, ids1, len_ids1), (x2, len2, ids2, len_ids2) = batch
                assert x1 is not None
                if deobfuscate:
                    (x1, len1, x2, len2) = self.trainer.deobfuscate_by_variable(
                        x1,
                        x2,
                        deobfuscation_proba,
                        params.tokenization_mode == "roberta",
                        rng,
                    )
                if x1 is None:
                    return None, None, None
        elif len(batch) == 4:
            assert lang1 == lang2
            if eval_computation_pivot:
                x1, len1, _, _ = batch
                x2, len2 = x1, len1
            else:
                x2, len2, _, _ = batch
                x1, len1 = add_noise(
                    x2, len2, self.params, len(self.data["dico"]) - 1, rng, torch_rng,
                )

        else:
            assert len(batch) == 3
            (
                (x1, len1, ids1, len_ids1),
                (x2, len2, ids2, len_ids2),
                (spans, len_spans, _, _),
            ) = batch

        lang1_id = params.lang2id[lang1]
        lang2_id = params.lang2id[lang2]
        langs1 = x1.clone().fill_(lang1_id)
        langs2 = x2.clone().fill_(lang2_id)

        # cuda
        x1, len1, langs1, x2, len2, langs2, spans = to_cuda(
            x1, len1, langs1, x2, len2, langs2, spans
        )

        return (x1, len1, langs1), (x2, len2, langs2), spans

    def sequence_to_ir(self, seq1, lang1, params, bpe_model):
        x1, len1, langs1 = seq1
        assert "ir_sa" in params.lgs
        input_sent_irs = self.tokens_to_code(x1, len1, lang1, params)
        input_sent_irs, ir_creation_errors = self.batch_to_irs(input_sent_irs, lang1)
        computed_irs_upd = [ir for ir in input_sent_irs]
        x1, len1, lang1_id, ir_creation_errors = self.create_ir_sent_batch(
            input_sent_irs, ir_creation_errors, bpe_model, x1, params
        )
        langs1 = x1.clone().fill_(lang1_id)
        return to_cuda(x1, len1, langs1), computed_irs_upd, ir_creation_errors

    def do_forward(self, encoder, decoder, seq1, seq2, spans, is_fp16):
        x1, len1, langs1 = seq1
        x2, len2, langs2 = seq2

        # encode source sentence
        enc1 = encoder(
            "fwd", x=x1, lengths=len1, langs=langs1, causal=False, spans=spans
        )
        enc1 = enc1.transpose(0, 1)
        enc1 = enc1.half() if is_fp16 else enc1

        # decode target sentence
        dec2 = decoder(
            "fwd",
            x=x2,
            lengths=len2,
            langs=langs2,
            causal=True,
            src_enc=enc1,
            src_len=len1,
            spans=spans,
        )

        return enc1, dec2

    def update_word_metrics(
        self,
        word_metrics,
        seq2,
        decoder,
        dec2,
        eval_computation_pivot,
        ir_creation_errors,
    ):
        x2, len2, _ = seq2

        # target words to predict
        alen = torch.arange(len2.max(), dtype=torch.long, device=len2.device)
        pred_mask = (
            alen[:, None] < len2[None] - 1
        )  # do not predict anything given the last target word
        if eval_computation_pivot:
            # dec2: (len, bs, dim)
            err_mask = torch.BoolTensor([not err for err in ir_creation_errors]).to(
                x2.device
            )
            dec2 = dec2[:, err_mask]
            pred_mask = pred_mask[:, err_mask]
            y = x2[1:, err_mask].masked_select(pred_mask[:-1])
        else:
            y = x2[1:].masked_select(pred_mask[:-1])
            assert len(y) == (len2 - 1).sum().item()

        # loss
        word_scores, loss = decoder(
            "predict", tensor=dec2, pred_mask=pred_mask, y=y, get_scores=True
        )

        word_metrics["n_words"] += y.size(0)
        word_metrics["xe_loss"] += loss.item() * len(y)
        word_metrics["n_valid"] += (
            (word_scores.max(1)[1] == y).sum().item() if y.size(0) else 0
        )

    def update_text_files(
        self,
        text_files,
        decoder,
        seq1,
        seq2,
        enc1,
        params,
        lang1,
        lang2,
        data_set,
        will_compute_bleu,
        eval_computation_pivot,
        ir_creation_errors,
        show_example,
    ):
        x1, len1, _ = seq1
        x2, len2, _ = seq2

        # generate translation - translate / convert to text
        text_hyps_upd, ref_upd, sources_upd = [], [], []

        if will_compute_bleu:
            lang2_id = params.lang2id[lang2]
            text_hyps_upd, generated = self.generate_mt_hypotheses(
                enc1, len1, lang2_id, decoder, params
            )
            if eval_computation_pivot:
                assert ir_creation_errors is not None
                text_hyps_upd = [
                    [FAILED_IR_COMP_ + h if err else h for h in hyp]
                    for hyp, err in zip(text_hyps_upd, ir_creation_errors)
                ]

            ref_upd = convert_to_text(x2, len2, self.dico, params)
            sources_upd = convert_to_text(x1, len1, self.dico, params)

            if show_example:
                # show 1 evaluation example and the corresponding model generation
                show_batch(
                    logger,
                    [
                        ("source", x1.transpose(0, 1)),
                        ("target", x2.transpose(0, 1)),
                        (
                            "gen",
                            generated.transpose(0, 1)
                            if len(generated.shape) == 2
                            else generated[:, 0, :].transpose(0, 1),
                        ),
                    ],
                    self.data["dico"],
                    self.params.tokenization_mode,
                    f"{data_set} {lang1}-{lang2}",
                    self.params.sentencepiece_model_path,
                )

        text_files["hypothesis"].append(text_hyps_upd)
        text_files["references"].append(ref_upd)
        text_files["sources"].append(sources_upd)

    def compute_metrics(
        self,
        model_outputs,
        data_set,
        lang1,
        lang2,
        params,
        scores,
        deobfuscate,
        deobfuscation_proba,
        do_eval,
        datasets_for_bleu,
        will_compute_bleu,
    ):
        n_words = model_outputs["n_words"]
        # compute perplexity and prediction accuracy
        l1l2 = get_l1l2_string(lang1, lang2, deobfuscation_proba)
        is_pivot = "pivot_" if do_eval["computation_pivot"] else ""
        scores["%s_%s_%smt_ppl" % (data_set, l1l2, is_pivot)] = (
            np.exp(model_outputs["xe_loss"] / n_words) if n_words > 0 else -1
        )
        scores["%s_%s_%smt_acc" % (data_set, l1l2, is_pivot)] = (
            100.0 * model_outputs["n_valid"] / n_words if n_words > 0 else -1
        )

        hypothesis = model_outputs["hypothesis"]
        if len(hypothesis) == 0:
            return

        common_variables = {  # Variables that are the input to several eval functions
            "data_set": data_set,
            "hypothesis": hypothesis,
            "lang1": lang1,
            "lang2": lang2,
            "params": params,
            "scores": scores,
        }

        # write hypotheses
        hyp_paths = ref_path = src_path = irs_path = None
        if will_compute_bleu:
            hyp_paths, ref_path, src_path, irs_path = self.write_hypo_ref_src(
                **common_variables,
                references=model_outputs["references"],
                sources=model_outputs["sources"],
                deobfuscation_proba=deobfuscation_proba,
                computed_irs=model_outputs["computed_irs"],
            )

        # check how many functions compiles + return same output as GT
        if (
            do_eval["computation"] or do_eval["computation_pivot"]
        ) and data_set in datasets_for_bleu:
            print(f"compute_comp_acc with {params.translation_eval_set} evaluation set")
            self.compute_comp_acc(
                **common_variables,
                hyp_paths=hyp_paths,
                ref_path=ref_path,
                tests_type=params.translation_eval_set,
                tokenization_mode=params.tokenization_mode,
                irs_path=irs_path,
            )
        if do_eval["ir_similarity"] and data_set in datasets_for_bleu:
            assert "ir" in lang1
            self.compute_ir_similarity(
                hypothesis, hyp_paths, src_path, lang1, lang2, data_set, scores
            )

        if (
            do_eval["st"]
            and data_set in datasets_for_bleu
            and get_programming_language_name(lang1) == SRC_ST_LANGS
            and get_programming_language_name(lang2) in TARGET_ST_LANG
        ):
            logger.info("Computing ST comp acc")
            self.compute_comp_acc(
                **common_variables,
                hyp_paths=hyp_paths,
                ref_path=ref_path,
                tests_type="evosuite",
                tokenization_mode=params.tokenization_mode,
            )

        if do_eval["subtoken_score"] and data_set in datasets_for_bleu:
            subtoken_level_scores = run_subtoken_score(ref_path, hyp_paths)
            for score_type, value in subtoken_level_scores.items():
                logger.info(
                    "Subtoken %s score %s %s : %f"
                    % (score_type, hyp_paths, ref_path, value)
                )
                scores[
                    "%s_%s_mt_subtoken_%s"
                    % (
                        data_set,
                        get_l1l2_string(lang1, lang2, deobfuscation_proba),
                        score_type,
                    )
                ] = value

        # compute BLEU score
        if do_eval["bleu"] and data_set in datasets_for_bleu:
            compute_bleu(
                hyp_paths[0],
                ref_path,
                "%s_%s_%smt_bleu"
                % (
                    data_set,
                    get_l1l2_string(lang1, lang2, deobfuscation_proba),
                    is_pivot,
                ),
                scores,
                filter_failed_irs=do_eval["computation_pivot"],
            )

        if (
            deobfuscate
            and do_eval["bleu"]
            or do_eval["subtoken_score"]
            and data_set in datasets_for_bleu
        ):
            # TODO clean lang1
            vizualize_do_files(lang1, src_path, ref_path, hyp_paths)
        if hyp_paths:
            for hyp_path in hyp_paths:
                Path(hyp_path).unlink()

    def generate_mt_hypotheses(self, enc1, len1, lang2_id, decoder, params):
        len_v = (10 * len1 + 10).clamp(max=params.max_len)
        if params.beam_size == 1:
            if params.number_samples > 1:
                assert params.eval_temperature is not None
                generated, lengths = decoder.generate(
                    enc1.repeat_interleave(params.number_samples, dim=0),
                    len1.repeat_interleave(params.number_samples, dim=0),
                    lang2_id,
                    max_len=len_v.repeat_interleave(params.number_samples, dim=0),
                    sample_temperature=params.eval_temperature,
                )
                generated = generated.T.reshape(
                    -1, params.number_samples, generated.shape[0]
                ).T
                lengths, _ = lengths.reshape(-1, params.number_samples).max(dim=1)
            else:
                generated, lengths = decoder.generate(
                    enc1, len1, lang2_id, max_len=len_v
                )
            # print(f'path 1: {generated.shape}')

        else:
            assert params.number_samples == 1
            generated, lengths, _ = decoder.generate_beam(
                enc1,
                len1,
                lang2_id,
                beam_size=params.beam_size,
                length_penalty=params.length_penalty,
                early_stopping=params.early_stopping,
                max_len=len_v,
            )
            # print(f'path 2: {generated.shape}')

        text_hyps = convert_to_text(
            generated, lengths, self.dico, params, generate_several_reps=True,
        )
        return text_hyps, generated

    def create_ir_sent_batch(
        self, input_sent_irs, ir_creation_errors, bpe_model, x1, params
    ):
        input_irs = [
            ["</s>"]
            + " ".join(
                [
                    x
                    for x in bpe_model.apply("" if ir_err else s.split(" "))
                    # if x.strip() != ""
                ]
            ).split(" ")
            + ["</s>"]
            for s, ir_err in zip(input_sent_irs, ir_creation_errors)
        ]
        too_long = [len(s) > params.max_len for s in input_irs]
        ir_creation_errors = [
            err or len(s) > params.max_len
            for s, err in zip(input_irs, ir_creation_errors)
        ]
        logger.info(
            f"{sum(too_long)} too long failures ({sum(ir_creation_errors)} in total) among {x1.shape[1]} examples"
        )
        ir_creation_errors = [
            err or too_long for err, too_long in zip(ir_creation_errors, too_long)
        ]
        input_irs = [
            ir if len(ir) <= params.max_len else ["</s>", "</s>"] for ir in input_irs
        ]
        old_x1_shape = x1.shape
        x1_device = x1.device
        input_irs = [np.array([self.dico.index(w) for w in ir]) for ir in input_irs]
        # Create ir batch
        len1 = torch.LongTensor([len(ir) for ir in input_irs]).to(x1_device)
        x1 = torch.LongTensor(len1.max().item(), len1.size(0)).fill_(params.pad_index)
        for i, s in enumerate(input_irs):
            x1[: len1[i], i].copy_(torch.from_numpy(s.astype(np.int64)))
        x1.to(x1_device)
        assert (x1 == params.eos_index).sum() == 2 * x1.size(1), (
            x1.shape,
            (x1 == params.eos_index).sum(),
        )
        assert x1.shape[1] == old_x1_shape[1], (x1.shape, old_x1_shape)
        assert "ir_sa" in params.lang2id
        lang1_id = params.lang2id["ir_sa"]
        return x1, len1, lang1_id, ir_creation_errors

    def batch_to_irs(self, input_sent_irs, lang1):
        number_examples = len(input_sent_irs)
        executor = ProcessPoolExecutor()
        ir_verbosity = False
        jobs = [
            executor.submit(
                code_to_ir, s, get_programming_language_name(lang1), True, ir_verbosity,
            )
            for s in input_sent_irs
        ]
        input_sent_irs = [j.result() for j in jobs]
        ir_creation_errors = [
            len(s) == 0 or s[0].startswith(ERROR_MESSAGE) for s in input_sent_irs
        ]
        logger.info(
            f"{len([x for x in ir_creation_errors if x])} failures among {number_examples} examples"
        )
        input_sent_irs = [
            s[0] if s else f"{ERROR_MESSAGE}: no IR" for s in input_sent_irs
        ]
        ir_tokenizer = IRProcessor().tokenize_code
        input_sent_irs = [" ".join(ir_tokenizer(c)) for c in input_sent_irs]
        return input_sent_irs, ir_creation_errors

    def tokens_to_code(self, x1, len1, lang1, params):
        input_sent_irs = convert_to_text(x1, len1, self.dico, params)
        assert x1.shape[1] == len(input_sent_irs), (
            x1.shape[1],
            len(input_sent_irs),
            input_sent_irs,
        )
        input_sent_irs = unsegment_and_detokenize(
            input_sent_irs,
            lang1,
            params.tokenization_mode,
            sentencepiece_model_path=params.sentencepiece_model_path,
        )
        return input_sent_irs

    @staticmethod
    def write_hypo_ref_src(
        data_set,
        hypothesis,
        lang1,
        lang2,
        params,
        references,
        scores,
        sources=None,
        deobfuscation_proba=None,
        computed_irs=None,
    ):
        # hypothesis / reference paths
        hyp_paths = []
        ref_name = "ref.{0}.{1}.txt".format(
            get_l1l2_string(lang1, lang2, deobfuscation_proba), data_set
        )
        ref_path = os.path.join(params.hyp_path, ref_name)
        # export sentences to hypothesis file / restore BPE segmentation
        for beam_number in range(len(hypothesis[0])):
            hyp_name = "hyp{0}.{1}.{2}_beam{3}.txt".format(
                scores["epoch"],
                get_l1l2_string(lang1, lang2, deobfuscation_proba),
                data_set,
                beam_number,
            )
            hyp_path = os.path.join(params.hyp_path, hyp_name)
            hyp_paths.append(hyp_path)
            print(f"outputing hypotheses in {hyp_path}")
            with open(hyp_path, "w", encoding="utf-8") as f:
                f.write("\n".join([hyp[beam_number] for hyp in hypothesis]) + "\n")
            restore_segmentation(
                hyp_path,
                tokenization_mode=params.tokenization_mode,
                single_line=True,
                sentencepiece_model_path=params.sentencepiece_model_path,
            )
        # export reference to ref file / restore BPE segmentation
        EncDecEvaluator.log_eval_outputs(ref_path, references, params)
        src_path = None
        if sources:
            src_path = ref_path.replace("ref.", "src.")
            EncDecEvaluator.log_eval_outputs(src_path, sources, params)
        irs_path = None
        if computed_irs:
            irs_path = ref_path.replace("ref.", "irs.")
            EncDecEvaluator.log_eval_outputs(
                irs_path, computed_irs, params, restore_bpe=False
            )

        return hyp_paths, ref_path, src_path, irs_path

    @staticmethod
    def log_eval_outputs(path, values, params, restore_bpe=True):
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join([s for s in values]) + "\n")
        if restore_bpe:
            restore_segmentation(
                path,
                tokenization_mode=params.tokenization_mode,
                single_line=True,
                sentencepiece_model_path=params.sentencepiece_model_path,
            )

    def compute_ir_similarity(
        self,
        hypothesis: tp.List[tp.List[str]],
        hyp_paths: tp.List[str],
        ref_path: str,
        lang1: str,
        lang2: str,
        data_set: str,
        scores: tp.Dict[str, float],
    ):
        assert "ir" in lang1
        input_sent_irs, ir_creation_errors = self.batch_to_irs(
            unsegment_and_detokenize(
                [h[0] for h in hypothesis],
                lang2,
                self.params.tokenization_mode,
                self.params.sentencepiece_model_path,
            ),
            lang2,
        )

        ratio_computed_irs = 1 - np.mean(ir_creation_errors)
        logger.info(f"IR correct: {hyp_paths[0]}: {ratio_computed_irs}")
        scores["%s_%s-%s_ir_correct" % (data_set, lang1, lang2)] = ratio_computed_irs

        with open(ref_path) as f:
            refs = f.readlines()
        irs_path = hyp_paths[0].replace(".txt", "_recomputed_irs.txt")
        refs_ir_path = ref_path.replace(".txt", "_recomputed_irs.txt")
        count_equal = 0
        assert len(input_sent_irs) == len(refs) == len(ir_creation_errors)
        with open(irs_path, "w") as f_irs:
            with open(refs_ir_path, "w") as f_refs:
                for hyp_ir, ref, error in zip(input_sent_irs, refs, ir_creation_errors):
                    if error:
                        continue
                    if hyp_ir.strip() == ref.strip():
                        count_equal += 1
                    f_irs.write(hyp_ir.strip() + "\n")
                    f_refs.write(ref.strip() + "\n")
        scores["%s_%s-%s_mt_ir_equal" % (data_set, lang1, lang2)] = count_equal / len(
            input_sent_irs
        )
        compute_bleu(
            irs_path,
            refs_ir_path,
            "%s_%s-%s_mt_ir_bleu" % (data_set, lang1, lang2),
            scores,
        )

    def compute_comp_acc(
        self,
        data_set,
        hyp_paths,
        hypothesis,
        lang1,
        lang2,
        params,
        ref_path,
        scores,
        tests_type,
        tokenization_mode="fastbpe",
        irs_path=None,
    ):
        prefix = "st" if tests_type == "evosuite" else ""
        assert self.evosuite_tests_dico is not None or tests_type != "evosuite"
        func_run_stats, func_run_out = eval_function_output(
            ref_path,
            hyp_paths,
            params.id_paths[(lang1, lang2, data_set)],
            lang1,
            lang2,
            params.eval_scripts_folders[(lang1, lang2, data_set)],
            EVAL_SCRIPT_FOLDER[data_set] if tests_type == GFG else CODENET_EVAL_FOLDER,
            params.retry_mistmatching_types,
            tokenization_mode,
            tests_type=tests_type,
            evosuite_tests=self.evosuite_tests_dico,
        )
        out_paths = []
        success_for_beam_number = [0 for _ in range(len(hypothesis[0]))]
        for beam_number in range(len(hypothesis[0])):
            out_name = prefix + "hyp{0}.{1}-{2}.{3}_beam{4}.out.txt".format(
                scores["epoch"], lang1, lang2, data_set, beam_number
            )
            out_path = os.path.join(params.hyp_path, out_name)
            out_paths.append(out_path)
            with open(out_path, "w", encoding="utf-8") as f:
                for results_list in func_run_out:
                    result_for_beam = (
                        results_list[beam_number]
                        if beam_number < len(results_list)
                        else ""
                    )
                    if result_for_beam.startswith("success"):
                        success_for_beam_number[beam_number] += 1
                    f.write(result_for_beam + "\n")
                f.write("\n")
        vizualize_translated_files(
            lang1,
            lang2,
            params.ref_paths[(lang2, lang1, data_set)],
            hyp_paths,
            params.id_paths[(lang1, lang2, data_set)],
            ref_path,
            out_paths,
            irs_path,
            tokenization_mode=tokenization_mode,
        )
        logger.info(
            prefix
            + "Computation res %s %s %s : %s"
            % (data_set, lang1, lang2, json.dumps(func_run_stats))
        )
        scores["%s_%s-%s_mt_comp_acc" % (data_set + prefix, lang1, lang2)] = (
            100.0
            * func_run_stats["success"]
            / (max(func_run_stats["total_evaluated"], 1))
        )
        successful_irs = func_run_stats["total_evaluated"] - func_run_stats.get(
            "Failed IR computation", 0
        )
        scores["%s_%s-%s_mt_comp_acc_pivot_IR" % (data_set + prefix, lang1, lang2)] = (
            100.0
            * func_run_stats["success"]
            / (successful_irs if successful_irs else 1)
        )
        scores["%s_%s-%s_mt_failed_pivot_IR" % (data_set + prefix, lang1, lang2)] = (
            100.0
            * func_run_stats.get("Failed IR computation", 0)
            / (max(func_run_stats["total_evaluated"], 1) if successful_irs else 1)
        )
        for beam_number, success_for_beam in enumerate(success_for_beam_number):
            scores[
                "%s_%s-%smt_comp_acc_contrib_beam_%i"
                % (data_set + prefix, lang1, lang2, beam_number)
            ] = (
                100.0
                * success_for_beam
                / (
                    func_run_stats["total_evaluated"]
                    if func_run_stats["total_evaluated"]
                    else 1
                )
            )
        for out_path in out_paths:
            Path(out_path).unlink()


def get_l1l2_string(lang1, lang2, deobfuscation_proba):
    l1l2 = [lang1, lang2]
    if deobfuscation_proba is not None:
        l1l2.append(f"obf_proba_{1 - deobfuscation_proba}")

    l1l2 = "-".join(l1l2)
    return l1l2


def eval_moses_bleu(ref, hyp):
    """
    Given a file of hypothesis and reference files,
    evaluate the BLEU score using Moses scripts.
    """
    assert os.path.isfile(hyp)
    assert os.path.isfile(ref) or os.path.isfile(ref + "0")
    assert os.path.isfile(BLEU_SCRIPT_PATH)
    command = BLEU_SCRIPT_PATH + " %s < %s"
    p = subprocess.Popen(command % (ref, hyp), stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0].decode("utf-8")
    if result.startswith("BLEU"):
        return float(result[7 : result.index(",")])
    else:
        logger.warning('Impossible to parse BLEU score! "%s"' % result)
        return -1


def unsegment_and_detokenize(
    sentences,
    lang,
    tokenization_mode: str,
    sentencepiece_model_path: tp.Optional[PathLike] = None,
):
    sentences = [
        restore_segmentation_sentence(
            s,
            tokenization_mode=tokenization_mode,
            sentencepiece_model_path=sentencepiece_model_path,
        )
        for s in sentences
    ]
    lang1_detokenizer = LangProcessor.processors[
        get_programming_language_name(lang)
    ]().detokenize_code
    sentences = [lang1_detokenizer(s) for s in sentences]
    return sentences


def compute_bleu(
    gen_path: str,
    ref_path: str,
    score_name: str,
    scores: tp.Dict[str, float],
    filter_failed_irs=False,
):
    if filter_failed_irs:
        hypotheses = read_file_lines(gen_path)
        references = read_file_lines(ref_path)
        errors = [h.strip().startswith(FAILED_IR_COMP_) for h in hypotheses]
        assert len(hypotheses) == len(references) == len(errors)
        hypotheses = [elmt for elmt, err in zip(hypotheses, errors) if not err]
        references = [elmt for elmt, err in zip(references, errors) if not err]
        ref = ref_path.replace(".txt", "_filtered.txt")
        gen = gen_path.replace(".txt", "_filtered.txt")
        with open(gen, "w") as f:
            f.writelines(hypotheses)

        with open(ref, "w") as f:
            f.writelines(references)
    else:
        ref = ref_path
        gen = gen_path
    bleu = eval_moses_bleu(ref, gen)
    logger.info("BLEU %s %s : %f" % (gen, ref, bleu))
    scores[score_name] = bleu
