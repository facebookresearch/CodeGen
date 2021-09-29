# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import json
import os
import subprocess
from collections import OrderedDict
from logging import getLogger
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import roc_auc_score, average_precision_score

from .comp_acc_computation import load_evosuite_transcoder_tests, eval_function_output
from .subtoken_score import run_subtoken_score
from ..data.loader import DATASET_SPLITS
from ..trainer import get_programming_language_name
from ..utils import (
    to_cuda,
    restore_segmentation,
    concat_batches,
    vizualize_translated_files,
    vizualize_do_files,
    show_batch,
    add_noise,
    convert_to_text,
    REPO_ROOT,
)
import sys

sys.path.append(REPO_ROOT)
from codegen_sources.test_generation.test_runners.cpp_test_runner import CppTestRunner
from codegen_sources.test_generation.test_runners.python_test_runner import (
    PythonTestRunner,
)

SRC_ST_LANGS = "java"

TARGET_ST_LANG = {"cpp", "python"}

EVAL_OBF_PROBAS = []

BLEU_SCRIPT_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "multi-bleu.perl"
)
EVAL_DATASET_SPLITS = [ds for ds in DATASET_SPLITS if ds != "train"]
assert os.path.isfile(BLEU_SCRIPT_PATH)
ROOT_FOLDER = Path(__file__).parents[4]
EVAL_SCRIPT_FOLDER = {
    "test": ROOT_FOLDER.joinpath("data/transcoder_evaluation_gfg"),
    "valid": ROOT_FOLDER.joinpath("data/transcoder_evaluation_gfg"),
}
logger = getLogger()


class Evaluator(object):
    def __init__(self, trainer, data, params):
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
        self,
        data_set,
        lang1,
        lang2=None,
        stream=False,
        span=None,
        st_scores_cutoff=None,
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
        subsample = 10

        if lang2 is None or lang2 == lang1:
            key = lang1 if span is None else (lang1, span)
            if stream and lang2 is None:
                iterator = self.data["mono_stream"][key][data_set].get_iterator(
                    shuffle=False, subsample=subsample
                )
            else:
                iterator = self.data["mono"][key][data_set].get_iterator(
                    tokens_per_batch=self.params.tokens_per_batch,
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
                tokens_per_batch=self.params.tokens_per_batch,
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
        for key, v in self.data["para"].items():
            span = None
            if len(key) == 3:
                lang1, lang2, span = key
            else:
                assert len(key) == 2
                lang1, lang2 = key
            assert lang1 < lang2, (lang1, lang2)

            for data_set in EVAL_DATASET_SPLITS:
                has_sent_ids = (data_set, (lang1, lang2)) in params.has_sentence_ids

                params.eval_scripts_folders[(lang1, lang2, data_set)] = os.path.join(
                    params.eval_scripts_root,
                    "{0}-{1}.{2}".format(lang1, lang2, data_set),
                )
                subprocess.Popen(
                    "mkdir -p %s"
                    % params.eval_scripts_folders[(lang1, lang2, data_set)],
                    shell=True,
                ).wait()
                params.eval_scripts_folders[(lang2, lang1, data_set)] = os.path.join(
                    params.eval_scripts_root,
                    "{0}-{1}.{2}".format(lang2, lang1, data_set),
                )
                subprocess.Popen(
                    "mkdir -p %s"
                    % params.eval_scripts_folders[(lang2, lang1, data_set)],
                    shell=True,
                ).wait()

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
                # convert to text
                for i, batch in enumerate(
                    self.get_iterator(data_set, lang1, lang2, span=span)
                ):
                    if len(batch) == 2:
                        (sent1, len1, id1, lenid1), (sent2, len2, id2, lenid2) = batch
                    else:
                        (
                            (sent1, len1, id1, lenid1),
                            (sent2, len2, id2, lenid2),
                            (span_batch, len_span, _, _),
                        ) = batch
                        spans.extend(list(span_batch.T))
                    lang1_txt.extend(convert_to_text(sent1, len1, self.dico, params))
                    lang2_txt.extend(convert_to_text(sent2, len2, self.dico, params))
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
                    lang1_path, roberta_mode=params.roberta_mode, single_line=True
                )
                restore_segmentation(
                    lang2_path, roberta_mode=params.roberta_mode, single_line=True
                )

                if has_sent_ids:
                    with open(id_path, "w", encoding="utf-8") as f:
                        f.write("\n".join(id_txt) + "\n")
                    restore_segmentation(
                        id_path, roberta_mode=params.roberta_mode, single_line=True
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
        deobf_probas_to_eval = EVAL_OBF_PROBAS
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
                for keys in set(
                    params.mt_steps
                    + [(l2, l3) for _, l2, l3 in params.bt_steps]
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
                ):
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
                        params.eval_computation,
                        params.eval_subtoken_score,
                        spans,
                    )
                if self.params.eval_denoising:
                    for lang in set(params.ae_steps):
                        assert lang in params.langs, lang
                        self.evaluate_mt(
                            scores,
                            data_set,
                            lang,
                            lang,
                            eval_bleu=False,
                            eval_computation=False,
                            eval_subtoken_score=False,
                            span=None,
                        )

                # machine translation task (evaluate perplexity and accuracy)
                for lang1, lang2 in set(params.do_steps):
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
                        eval_subtoken_score=params.eval_subtoken_score,
                        span=None,
                        deobfuscate=True,
                        deobfuscate_probas=deobf_probas_to_eval,
                    )

                # prediction task (evaluate perplexity and accuracy)
                for lang1, lang2 in params.classif_steps:
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
        return scores

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

        model = self.model if params.encoder_only else self.decoder
        model.eval()
        model = model.module if params.multi_gpu else model

        lang1_id = params.lang2id[lang1]
        lang2_id = params.lang2id[lang2] if lang2 is not None else None
        l1l2 = lang1 if lang2 is None else f"{lang1}-{lang2}"

        n_words = 0
        xe_loss = 0
        n_valid = 0

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
            n_valid += (word_scores.max(1)[1] == y).sum().item()

        # log
        logger.info(
            "Found %i words in %s. %i were predicted correctly."
            % (n_words, data_set, n_valid)
        )

        # compute perplexity and prediction accuracy
        ppl_name = "%s_%s_clm_ppl" % (data_set, l1l2)
        acc_name = "%s_%s_clm_acc" % (data_set, l1l2)
        scores[ppl_name] = np.exp(xe_loss / n_words)
        scores[acc_name] = 100.0 * n_valid / n_words

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
                    self.params.roberta_mode,
                    "Evaluation",
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
    def __init__(self, trainer, data, params):
        """
        Build language model evaluator.
        """
        super().__init__(trainer, data, params)
        self.model = trainer.model
        if params.use_classifier:
            self.classifier = trainer.classifier


class EncDecEvaluator(Evaluator):
    def __init__(self, trainer, data, params):
        """
        Build encoder / decoder evaluator.
        """
        super().__init__(trainer, data, params)
        self.encoder = trainer.encoder
        self.decoder = trainer.decoder

    def evaluate_mt(
        self,
        scores,
        data_set,
        lang1,
        lang2,
        eval_bleu,
        eval_computation,
        eval_subtoken_score,
        span,
        deobfuscate=False,
        deobfuscate_probas=None,
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
        eval_st = params.eval_st
        if not params.is_master or "cl" in lang1:
            # Computing the accuracy on every node is useful for debugging but
            # no need to evaluate spend too much time on the evaluation when not on master
            eval_bleu = False
            eval_computation = False
            eval_subtoken_score = False
            eval_st = False

        # store hypothesis to compute BLEU score
        if params.eval_bleu_test_only:
            datasets_for_bleu = ["test"]
        else:
            datasets_for_bleu = [s for s in EVAL_DATASET_SPLITS if s != "train"]

        lang1_id = params.lang2id[lang1]
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

            n_words = 0
            xe_loss = 0
            n_valid = 0
            hypothesis = []
            sources = []
            references = []
            for i, batch in enumerate(
                self.get_iterator(
                    data_set, lang1, lang2 if lang2 != lang1 else None, span=span
                )
            ):
                spans = None
                assert len(batch) >= 2
                if len(batch) == 2:
                    if lang1 == lang2:
                        x2, len2 = batch
                        x1, len1 = add_noise(
                            x2,
                            len2,
                            self.params,
                            len(self.data["dico"]) - 1,
                            rng,
                            torch_rng,
                        )
                    else:
                        (x1, len1, ids1, len_ids1), (x2, len2, ids2, len_ids2) = batch
                        if deobfuscate:
                            (x1, len1, x2, len2) = self.trainer.deobfuscate_by_variable(
                                x1, x2, deobfuscation_proba, params.roberta_mode, rng
                            )
                            if x1 is None:
                                continue
                else:
                    assert len(batch) == 3
                    (
                        (x1, len1, ids1, len_ids1),
                        (x2, len2, ids2, len_ids2),
                        (spans, len_spans, _, _),
                    ) = batch

                langs1 = x1.clone().fill_(lang1_id)
                langs2 = x2.clone().fill_(lang2_id)

                # target words to predict
                alen = torch.arange(len2.max(), dtype=torch.long, device=len2.device)
                pred_mask = (
                    alen[:, None] < len2[None] - 1
                )  # do not predict anything given the last target word
                y = x2[1:].masked_select(pred_mask[:-1])
                assert len(y) == (len2 - 1).sum().item()

                # cuda
                x1, len1, langs1, x2, len2, langs2, y, spans = to_cuda(
                    x1, len1, langs1, x2, len2, langs2, y, spans
                )
                # encode source sentence
                enc1 = encoder(
                    "fwd", x=x1, lengths=len1, langs=langs1, causal=False, spans=spans
                )
                enc1 = enc1.transpose(0, 1)
                enc1 = enc1.half() if params.fp16 else enc1
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

                # loss
                word_scores, loss = decoder(
                    "predict", tensor=dec2, pred_mask=pred_mask, y=y, get_scores=True
                )

                # update stats
                n_words += y.size(0)
                xe_loss += loss.item() * len(y)
                n_valid += (word_scores.max(1)[1] == y).sum().item()

                # generate translation - translate / convert to text
                if (
                    eval_bleu or eval_computation or eval_subtoken_score
                ) and data_set in datasets_for_bleu:
                    len_v = (3 * len1 + 10).clamp(max=params.max_len)
                    if params.beam_size == 1:
                        if params.number_samples > 1:
                            assert params.eval_temperature is not None
                            generated, lengths = decoder.generate(
                                enc1.repeat_interleave(params.number_samples, dim=0),
                                len1.repeat_interleave(params.number_samples, dim=0),
                                lang2_id,
                                max_len=len_v.repeat_interleave(
                                    params.number_samples, dim=0
                                ),
                                sample_temperature=params.eval_temperature,
                            )
                            generated = generated.T.reshape(
                                -1, params.number_samples, generated.shape[0]
                            ).T
                            lengths, _ = lengths.reshape(-1, params.number_samples).max(
                                dim=1
                            )
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
                    if i == 0:
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
                            self.params.roberta_mode,
                            f"{data_set} {lang1}-{lang2}",
                        )

                    hypothesis.extend(
                        convert_to_text(
                            generated,
                            lengths,
                            self.dico,
                            params,
                            generate_several_reps=True,
                        )
                    )
                    references.extend(convert_to_text(x2, len2, self.dico, params))
                    sources.extend(convert_to_text(x1, len1, self.dico, params))

            # compute perplexity and prediction accuracy
            l1l2 = get_l1l2_string(lang1, lang2, deobfuscation_proba)
            scores["%s_%s_mt_ppl" % (data_set, l1l2)] = np.exp(xe_loss / n_words)
            scores["%s_%s_mt_acc" % (data_set, l1l2)] = 100.0 * n_valid / n_words

            # write hypotheses
            if (
                eval_bleu or eval_computation or eval_subtoken_score
            ) and data_set in datasets_for_bleu:
                hyp_paths, ref_path, src_path = self.write_hypo_ref_src(
                    data_set,
                    hypothesis,
                    lang1,
                    lang2,
                    params,
                    references,
                    scores,
                    sources,
                    deobfuscation_proba,
                )

            # check how many functions compiles + return same output as GT
            if eval_computation and data_set in datasets_for_bleu:
                print("compute_comp_acc")
                self.compute_comp_acc(
                    data_set,
                    hyp_paths,
                    hypothesis,
                    lang1,
                    lang2,
                    params,
                    ref_path,
                    scores,
                    roberta_mode=params.roberta_mode,
                )

            if (
                eval_st
                and data_set in datasets_for_bleu
                and get_programming_language_name(lang1) == SRC_ST_LANGS
                and get_programming_language_name(lang2) in TARGET_ST_LANG
            ):
                logger.info("Computing ST comp acc")
                self.compute_comp_acc(
                    data_set,
                    hyp_paths,
                    hypothesis,
                    lang1,
                    lang2,
                    params,
                    ref_path,
                    scores,
                    roberta_mode=params.roberta_mode,
                    evosuite_functions=True,
                )
            if eval_subtoken_score and data_set in datasets_for_bleu:
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
            if eval_bleu and data_set in datasets_for_bleu:
                # evaluate BLEU score
                bleu = eval_moses_bleu(ref_path, hyp_paths[0])
                logger.info("BLEU %s %s : %f" % (hyp_paths[0], ref_path, bleu))
                scores[
                    "%s_%s_mt_bleu"
                    % (data_set, get_l1l2_string(lang1, lang2, deobfuscation_proba))
                ] = bleu
                if eval_computation:
                    for hyp_path in hyp_paths:
                        Path(hyp_path).unlink()

            if (
                deobfuscate
                and eval_bleu
                or eval_subtoken_score
                and data_set in datasets_for_bleu
            ):
                # TODO clean lang1
                vizualize_do_files(lang1.split("_")[0], src_path, ref_path, hyp_paths)

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
                hyp_path, roberta_mode=params.roberta_mode, single_line=True
            )
        # export reference to ref file / restore BPE segmentation
        with open(ref_path, "w", encoding="utf-8") as f:
            f.write("\n".join([ref for ref in references]) + "\n")
        restore_segmentation(
            ref_path, roberta_mode=params.roberta_mode, single_line=True
        )
        if sources:
            src_path = ref_path.replace("ref.", "src.")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write("\n".join([src for src in sources]) + "\n")
            restore_segmentation(
                src_path, roberta_mode=params.roberta_mode, single_line=True
            )
            return hyp_paths, ref_path, src_path
        return hyp_paths, ref_path, None

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
        roberta_mode=False,
        evosuite_functions=False,
    ):
        assert self.evosuite_tests_dico is not None or not evosuite_functions
        func_run_stats, func_run_out = eval_function_output(
            ref_path,
            hyp_paths,
            params.id_paths[(lang1, lang2, data_set)],
            lang2,
            params.eval_scripts_folders[(lang1, lang2, data_set)],
            EVAL_SCRIPT_FOLDER[data_set],
            params.retry_mistmatching_types,
            roberta_mode,
            evosuite_functions=evosuite_functions,
            evosuite_tests=self.evosuite_tests_dico,
        )
        out_paths = []
        success_for_beam_number = [0 for _ in range(len(hypothesis[0]))]
        prefix = "st" if evosuite_functions else ""
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
        )
        logger.info(
            prefix
            + "Computation res %s %s %s : %s"
            % (data_set, lang1, lang2, json.dumps(func_run_stats))
        )
        scores[
            "%s_%s-%s_mt_comp_acc" % (data_set + prefix, lang1, lang2)
        ] = func_run_stats["success"] / (
            func_run_stats["total_evaluated"]
            if func_run_stats["total_evaluated"]
            else 1
        )
        for beam_number, success_for_beam in enumerate(success_for_beam_number):
            scores[
                "%s_%s-%smt_comp_acc_contrib_beam_%i"
                % (data_set + prefix, lang1, lang2, beam_number)
            ] = (
                success_for_beam
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
