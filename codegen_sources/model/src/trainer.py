# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import math
import os
import time
from collections import OrderedDict
from logging import getLogger

import apex
import numpy as np
import torch
from torch import nn
from torch.nn.utils import clip_grad_norm_

from .optim import get_optimizer
from .utils import parse_lambda_config, update_lambdas, add_noise
from .utils import to_cuda, concat_batches, batch_sentences, show_batch

logger = getLogger()


class Trainer(object):
    def __init__(self, data, params):
        """
        Initialize trainer.
        """
        # epoch / iteration size
        self.epoch_size = params.epoch_size
        if self.epoch_size == -1:
            self.epoch_size = len(self.data)
            assert self.epoch_size > 0

        # data iterators
        self.iterators = {}

        # set parameters
        self.set_parameters()

        # float16 / distributed (no AMP)
        assert params.amp >= 1 or not params.fp16
        assert params.amp >= 0 or params.accumulate_gradients == 1
        if params.multi_gpu and params.amp == -1:
            logger.info("Using nn.parallel.DistributedDataParallel ...")
            for name in self.MODEL_NAMES:
                model_attr = getattr(self, name)
                if isinstance(model_attr, list):
                    setattr(
                        self,
                        name,
                        [
                            nn.parallel.DistributedDataParallel(
                                model,
                                device_ids=[params.local_rank],
                                output_device=params.local_rank,
                                broadcast_buffers=True,
                            )
                            for model in model_attr
                        ],
                    )
                else:
                    setattr(
                        self,
                        name,
                        nn.parallel.DistributedDataParallel(
                            model_attr,
                            device_ids=[params.local_rank],
                            output_device=params.local_rank,
                            broadcast_buffers=True,
                        ),
                    )

        # set optimizers
        self.set_optimizers()

        # float16 / distributed (AMP)
        if params.amp >= 0:
            self.init_amp()
            if params.multi_gpu:
                logger.info("Using apex.parallel.DistributedDataParallel ...")
                for name in self.MODEL_NAMES:
                    model_attr = getattr(self, name)
                    if isinstance(model_attr, list):
                        setattr(
                            self,
                            name,
                            [
                                apex.parallel.DistributedDataParallel(
                                    model, delay_allreduce=True
                                )
                                for model in model_attr
                            ],
                        )
                    else:
                        setattr(
                            self,
                            name,
                            apex.parallel.DistributedDataParallel(
                                model_attr, delay_allreduce=True
                            ),
                        )

        # stopping criterion used for early stopping
        if params.stopping_criterion != "":
            split = params.stopping_criterion.split(",")
            assert len(split) == 2 and split[1].isdigit()
            self.decrease_counts_max = int(split[1])
            self.decrease_counts = 0
            if split[0][0] == "_":
                self.stopping_criterion = (split[0][1:], False)
            else:
                self.stopping_criterion = (split[0], True)
            self.best_stopping_criterion = -1e12 if self.stopping_criterion[1] else 1e12
        else:
            self.stopping_criterion = None
            self.best_stopping_criterion = None

        # probability of masking out / randomize / not modify words to predict
        params.pred_probs = torch.FloatTensor(
            [params.word_mask, params.word_keep, params.word_rand]
        )

        # probabilty to predict a word
        counts = np.array(list(self.data["dico"].counts.values()))
        params.mask_scores = np.maximum(counts, 1) ** -params.sample_alpha
        params.mask_scores[params.pad_index] = 0  # do not predict <PAD> index
        # do not predict special tokens
        params.mask_scores[counts == 0] = 0

        # validation metrics
        self.metrics = []
        metrics = [m for m in params.validation_metrics.split(",") if m != ""]
        for m in metrics:
            m = (m[1:], False) if m[0] == "_" else (m, True)
            self.metrics.append(m)
        self.best_metrics = {
            metric: (-1e12 if biggest else 1e12) for (metric, biggest) in self.metrics
        }

        # training statistics
        self.epoch = 0
        self.n_iter = 0
        self.n_total_iter = 0
        self.n_sentences = 0
        self.stats = OrderedDict(
            [("processed_s", 0), ("processed_w", 0)]
            + [("CLM-%s" % l, []) for l in params.langs]
            + [("CLM-%s" % ("-".join(keys)), []) for keys in data["para"].keys()]
            + [("CLM-%s" % "-".join(keys[::-1]), []) for keys in data["para"].keys()]
            + [("MLM-%s" % l, []) for l in params.langs]
            + [("MLM-%s" % ("-".join(keys)), []) for keys in data["para"].keys()]
            + [("MLM-%s" % "-".join(keys[::-1]), []) for keys in data["para"].keys()]
            + [("AE-%s" % lang, []) for lang in params.ae_steps]
            + [("MT-%s-%s" % (l1, l2), []) for l1, l2 in params.mt_steps]
            + [
                ("MT-%s-%s-%s" % (l1, l2, span), [])
                for l1, l2, span in params.mt_spans_steps
            ]
            + [("DO-%s-%s" % (l1, l2), []) for l1, l2 in params.do_steps]
            + [("Classif-%s-%s" % (l1, l2), []) for l1, l2 in params.classif_steps]
            + [("BT-%s-%s-%s" % (l1, l2, l3), []) for l1, l2, l3 in params.bt_steps]
        )
        self.last_time = time.time()

        # reload potential checkpoints
        self.reload_checkpoint()

        # initialize lambda coefficients and their configurations
        parse_lambda_config(params)

    def set_parameters(self):
        """
        Set parameters.
        """
        self.parameters = {}
        named_params = []
        for name in self.MODEL_NAMES:
            models = getattr(self, name)
            if isinstance(models, list):
                for model in models:
                    named_params.extend(
                        [(k, p) for k, p in model.named_parameters() if p.requires_grad]
                    )
            else:
                named_params.extend(
                    [(k, p) for k, p in models.named_parameters() if p.requires_grad]
                )

        # model parameters
        self.parameters["model"] = [p for k, p in named_params]

        # log
        for k, v in self.parameters.items():
            logger.info("Found %i parameters in %s." % (len(v), k))
            assert len(v) >= 1

    def set_optimizers(self):
        """
        Set optimizers.
        """
        params = self.params
        self.optimizers = {}

        # model optimizer
        self.optimizers["model"] = get_optimizer(
            self.parameters["model"], params.optimizer
        )

        # log
        logger.info("Optimizers: %s" % ", ".join(self.optimizers.keys()))

    def init_amp(self):
        """
        Initialize AMP optimizer.
        """
        params = self.params
        assert (
            params.amp == 0
            and params.fp16 is False
            or params.amp in [1, 2, 3]
            and params.fp16 is True
        )
        opt_names = self.optimizers.keys()
        models = [
            model
            for name in self.MODEL_NAMES
            for model in (
                getattr(self, name)
                if isinstance(getattr(self, name), list)
                else [getattr(self, name)]
            )
        ]
        models, optimizers = apex.amp.initialize(
            models,
            [self.optimizers[k] for k in opt_names],
            opt_level=("O%i" % params.amp),
        )
        current_index = 0
        for name in self.MODEL_NAMES:
            model_attr = getattr(self, name)
            if isinstance(model_attr, list):
                models_length = len(model_attr)
                setattr(
                    self, name, models[current_index : current_index + models_length]
                )
                current_index += models_length
            else:
                setattr(self, name, models[current_index])
                current_index += 1
        assert current_index == len(models)
        self.optimizers = {
            opt_name: optimizer for opt_name, optimizer in zip(opt_names, optimizers)
        }

    def optimize(self, loss):
        """
        Optimize.
        """
        # check NaN
        if (loss != loss).data.any():
            logger.warning("NaN detected")
            # exit()

        params = self.params

        # optimizers
        names = self.optimizers.keys()
        optimizers = [self.optimizers[k] for k in names]

        # regular optimization
        if params.amp == -1:
            for optimizer in optimizers:
                optimizer.zero_grad()
            loss.backward()
            if params.clip_grad_norm > 0:
                for name in names:
                    # norm_check_a = (sum([p.grad.norm(p=2).item() ** 2 for p in self.parameters[name]])) ** 0.5
                    clip_grad_norm_(self.parameters[name], params.clip_grad_norm)
                    # norm_check_b = (sum([p.grad.norm(p=2).item() ** 2 for p in self.parameters[name]])) ** 0.5
                    # print(name, norm_check_a, norm_check_b)
            for optimizer in optimizers:
                optimizer.step()

        # AMP optimization
        else:
            if self.n_iter % params.accumulate_gradients == 0:
                with apex.amp.scale_loss(loss, optimizers) as scaled_loss:
                    scaled_loss.backward()
                if params.clip_grad_norm > 0:
                    for name in names:
                        # norm_check_a = (sum([p.grad.norm(p=2).item() ** 2 for p in apex.amp.master_params(self.optimizers[name])])) ** 0.5
                        clip_grad_norm_(
                            apex.amp.master_params(self.optimizers[name]),
                            params.clip_grad_norm,
                        )
                        # norm_check_b = (sum([p.grad.norm(p=2).item() ** 2 for p in apex.amp.master_params(self.optimizers[name])])) ** 0.5
                        # print(name, norm_check_a, norm_check_b)
                for optimizer in optimizers:
                    optimizer.step()
                    optimizer.zero_grad()
            else:
                with apex.amp.scale_loss(
                    loss, optimizers, delay_unscale=True
                ) as scaled_loss:
                    scaled_loss.backward()

    def iter(self):
        """
        End of iteration.
        """
        self.n_iter += 1
        self.n_total_iter += 1
        update_lambdas(self.params, self.n_total_iter)
        if self.n_iter % 5 == 0:
            self.print_stats()

    def print_stats(self):
        """
        Print statistics about the training.
        """
        # if self.n_total_iter % 5 != 0:
        #     return

        s_iter = "%7i - " % self.n_total_iter
        s_stat = " || ".join(
            [
                "{}: {:7.4f}".format(k, np.mean(v))
                for k, v in self.stats.items()
                if type(v) is list and len(v) > 0
            ]
        )
        for k in self.stats.keys():
            if type(self.stats[k]) is list:
                del self.stats[k][:]

        # learning rates
        s_lr = " - "
        for k, v in self.optimizers.items():
            s_lr = (
                s_lr
                + (" - %s LR: " % k)
                + " / ".join("{:.4e}".format(group["lr"]) for group in v.param_groups)
            )

        if self.params.bt_sample_temperature > 0:
            s_bt_samp = " - BT-sampling-T: " + "{:2.2e}".format(
                self.params.bt_sample_temperature
            )
        else:
            s_bt_samp = ""

        # processing speed
        new_time = time.time()
        diff = new_time - self.last_time
        s_speed = "{:7.2f} sent/s - {:8.2f} words/s - ".format(
            self.stats["processed_s"] * 1.0 / diff,
            self.stats["processed_w"] * 1.0 / diff,
        )
        self.stats["processed_s"] = 0
        self.stats["processed_w"] = 0
        self.last_time = new_time

        # log speed + stats + learning rate
        logger.info(s_iter + s_speed + s_stat + s_lr + s_bt_samp)

    def get_iterator(self, iter_name, lang1, lang2, stream, span=None):
        """
        Create a new iterator for a dataset.
        """
        logger.info(
            "Creating new training data iterator (%s) ..."
            % ",".join([str(x) for x in [iter_name, lang1, lang2] if x is not None])
        )
        if lang2 is None:
            if stream:
                if span is None:
                    iterator = self.data["mono_stream"][lang1]["train"].get_iterator(
                        shuffle=True
                    )
                else:
                    iterator = self.data["mono_stream"][(lang1, span)][
                        "train"
                    ].get_iterator(shuffle=True)
            else:
                assert self.params.gen_tpb_multiplier > 0
                it = (
                    self.data["mono"][lang1]["train"]
                    if span is None
                    else self.data["mono"][(lang1, span)]["train"]
                )
                iterator = it.get_iterator(
                    shuffle=True,
                    group_by_size=self.params.group_by_size,
                    n_sentences=-1,
                    tokens_per_batch=self.params.tokens_per_batch
                    * (self.params.gen_tpb_multiplier if iter_name == "bt" else 1),
                )
        else:
            assert stream is False
            _lang1, _lang2 = (lang1, lang2) if lang1 < lang2 else (lang2, lang1)
            it = (
                self.data["para"][(_lang1, _lang2)]["train"]
                if span is None
                else self.data["para"][(_lang1, _lang2, span)]["train"]
            )
            iterator = it.get_iterator(
                shuffle=True,
                group_by_size=self.params.group_by_size,
                n_sentences=-1,
                tokens_per_batch=self.params.tokens_per_batch,
            )

        key = (
            (iter_name, lang1, lang2)
            if span is None
            else (iter_name, lang1, lang2, span)
        )
        self.iterators[key] = iterator
        return iterator

    def get_batch(self, iter_name, lang1, lang2=None, stream=False, span=None):
        """
        Return a batch of sentences from a dataset.
        """
        assert lang1 in self.params.langs
        assert (
            lang2 is None
            or lang2 in self.params.langs
            or (lang1, lang2) in self.params.classif_steps
        )
        assert stream is False or lang2 is None

        iterator = (
            self.iterators.get((iter_name, lang1, lang2, span), None)
            if span is not None
            else self.iterators.get((iter_name, lang1, lang2), None)
        )
        if iterator is None:
            iterator = self.get_iterator(iter_name, lang1, lang2, stream, span)
        try:
            x = next(iterator)
        except StopIteration:
            iterator = self.get_iterator(iter_name, lang1, lang2, stream, span)
            x = next(iterator)
        return x if lang2 is None or lang1 < lang2 else x[::-1]

    def mask_out(self, x, lengths):
        """
        Decide of random words to mask out, and what target they get assigned.
        """
        params = self.params
        slen, bs = x.size()

        # define target words to predict
        if params.sample_alpha == 0:
            pred_mask = np.random.rand(slen, bs) <= params.word_pred
            pred_mask = torch.from_numpy(pred_mask.astype(np.uint8))
        else:
            x_prob = params.mask_scores[x.flatten()]
            n_tgt = math.ceil(params.word_pred * slen * bs)
            tgt_ids = np.random.choice(
                len(x_prob), n_tgt, replace=False, p=x_prob / x_prob.sum()
            )
            pred_mask = torch.zeros(slen * bs, dtype=torch.uint8)
            pred_mask[tgt_ids] = 1
            pred_mask = pred_mask.view(slen, bs)

        # do not predict padding
        pred_mask[x == params.pad_index] = 0
        pred_mask[0] = 0  # TODO: remove

        # mask a number of words == 0 [8] (faster with fp16)
        if params.fp16:
            pred_mask = pred_mask.view(-1)
            n1 = pred_mask.sum().item()
            n2 = max(n1 % 8, 8 * (n1 // 8))
            if n2 != n1:
                pred_mask[torch.nonzero(pred_mask).view(-1)[: n1 - n2]] = 0
            pred_mask = pred_mask.view(slen, bs)
            assert pred_mask.sum().item() % 8 == 0

        # generate possible targets / update x input
        pred_mask = pred_mask == 1
        _x_real = x[pred_mask]
        _x_rand = _x_real.clone().random_(params.n_words)
        _x_mask = _x_real.clone().fill_(params.mask_index)
        probs = torch.multinomial(params.pred_probs, len(_x_real), replacement=True)
        _x = (
            _x_mask * (probs == 0).long()
            + _x_real * (probs == 1).long()
            + _x_rand * (probs == 2).long()
        )
        x = x.masked_scatter(pred_mask, _x)

        assert 0 <= x.min() <= x.max() < params.n_words
        assert x.size() == (slen, bs)
        assert pred_mask.size() == (slen, bs)

        return x, _x_real, pred_mask

    def deobfuscate(self, x, y, p):
        """
        Deobfuscate class, function and variable name with probabilty p.
        For all variables, functions and classes, we pick some occurences with a probability p and deobfuscate them.
        i.e some occurences of VAR_0 will be deobfuscated and other keept as VAR_0.
        x : tensor slen x bs , x is obfuscated, i.e variable, function and classes names are
        replaced by special tokens. ( CLASS_X, FUNC_X and VAR_X)
        y : ylen x bs contains the dictionary of obfuscated tokens, i.e 'CLASS_0 class_name | VAR_0 variable_name .. '
        """
        slen, bs = x.size()

        obf_tokens = (x >= self.data["dico"].obf_index["CLASS"]) * (
            x < (self.data["dico"].obf_index["CLASS"] + self.data["dico"].n_obf_tokens)
        )
        dobf_mask = np.random.rand(slen, bs) <= p
        dobf_mask = torch.from_numpy(dobf_mask)
        dobf_mask = dobf_mask * obf_tokens
        x[dobf_mask] = -x[
            dobf_mask
        ]  # put to negative all the obf_tokens that have to be restored

        # convert sentences to strings and dictionary to a python dictionary {obf_token_special : original_name}
        x_ = [
            " ".join(
                [
                    str(w)
                    for w in s
                    if w not in [self.params.pad_index, self.params.eos_index]
                ]
            )
            for s in x.transpose(0, 1).tolist()
        ]
        y_ = [
            " ".join(
                [
                    str(w)
                    for w in s
                    if w not in [self.params.pad_index, self.params.eos_index]
                ]
            )
            for s in y.transpose(0, 1).tolist()
        ]
        sep = f" {self.data['dico'].word2id['|']} "
        d = [
            {
                mapping.strip().split()[0]: " ".join(mapping.strip().split()[1:])
                for mapping in pred.split(sep)
            }
            for pred in y_
        ]

        # restore x i.e replace negative numbers by the original name
        # TODO check that sentences are < max_len like in deobfuscate_by_variable
        for i in range(bs):
            for k, v in d[i].items():
                x_[i] = x_[i].replace(f"-{k}", v)
            x_[i] = np.array([int(id) for id in x_[i].split()])

        x_b, lengths = batch_sentences(x_, self.params.pad_index, self.params.eos_index)

        assert sum(sum((x_b < 0).float())) == 0

        return (x_b, lengths)

    def deobfuscate_by_variable(self, x, y, p, roberta_mode, rng=None):
        """
        Deobfuscate class, function and variable name with probabilty p, by variable blocked.
        We chose some variables VAR_N, functions FUNC_N or class CLASS_N - with probability p - to deobfuscate entirely.
        I.e if VAR_0 is picked, all the occurences of VAR_0 are deobfuscated.
        x : tensor slen x bs , x is obfuscated, i.e variable, function and classes names are
        replaced by special tokens. ( CLASS_X, FUNC_X and VAR_X)
        y : ylen x bs contains the dictionary of obfuscated tokens, i.e 'CLASS_0 class_name | VAR_0 variable_name .. '
        """

        slen, bs = x.size()

        # put to negative all the obf_tokens, useful for restoration i.e replacement in string later on
        obf_tokens = (x >= self.data["dico"].obf_index["CLASS"]) * (
            x < (self.data["dico"].obf_index["CLASS"] + self.data["dico"].n_obf_tokens)
        )
        x[obf_tokens] = -x[obf_tokens]

        # convert sentences to strings and dictionary to a python dictionary (obf_token_special , original_name)
        x_ = [
            " ".join(
                [
                    str(w)
                    for w in s
                    if w not in [self.params.pad_index, self.params.eos_index]
                ]
            )
            for s in x.transpose(0, 1).tolist()
        ]
        y_ = [
            " ".join(
                [
                    str(w)
                    for w in s
                    if w not in [self.params.pad_index, self.params.eos_index]
                ]
            )
            for s in y.transpose(0, 1).tolist()
        ]
        if roberta_mode:
            sep = (
                f" {self.data['dico'].word2id['Ġ|']} {self.data['dico'].word2id['Ġ']} "
            )
        else:
            sep = f" {self.data['dico'].word2id['|']} "
        # reversed order to have longer obfuscation first, to make replacement in correct order
        d = [
            list(
                reversed(
                    [
                        (
                            mapping.strip().split()[0],
                            " ".join(mapping.strip().split()[1:]),
                        )
                        for mapping in pred.split(sep)
                    ]
                )
            )
            for pred in y_
        ]

        # restore x i.e select variable with probability p and restore all occurence of this variable
        # keep only unrestored variable in dictionary d_
        x = []
        y = []

        for i in range(bs):
            d_ = []
            if rng:
                dobf_mask = rng.rand(len(d[i])) <= p
            else:
                dobf_mask = np.random.rand(len(d[i])) <= p
            # make sure at least one variable is picked
            if sum(dobf_mask) == len(d[i]):
                if rng:
                    dobf_mask[rng.randint(0, len(d[i]))] = False
                else:
                    dobf_mask[np.random.randint(0, len(d[i]))] = False
            for m, (k, v) in enumerate(d[i]):
                if dobf_mask[m]:
                    x_[i] = x_[i].replace(f"-{k}", f"{v}")
                else:
                    d_.append((k, v))
                    x_[i] = x_[i].replace(f"-{k}", f"{k}")
            if roberta_mode:
                # we need to remove the double space introduced during deobfuscation, i.e the "Ġ Ġ"
                sent_ids = np.array(
                    [
                        self.data["dico"].word2id[index]
                        for index in (
                            " ".join(
                                [
                                    self.data["dico"].id2word[int(w)]
                                    for w in x_[i].split()
                                ]
                            ).replace("Ġ Ġ", "Ġ")
                        ).split()
                    ]
                )
            else:
                sent_ids = np.array([int(id) for id in x_[i].split()])
            if len(sent_ids) < self.params.max_len:
                x.append(sent_ids)
                d_ids = sep.join([" ".join([k, v]) for k, v in reversed(d_)])
                d_ids = np.array([int(id) for id in d_ids.split()])
                y.append(d_ids)

        if len(x) == 0:
            return None, None, None, None

        x, len_x = batch_sentences(x, self.params.pad_index, self.params.eos_index)
        y, len_y = batch_sentences(y, self.params.pad_index, self.params.eos_index)

        assert sum(sum((x < 0).float())) == 0

        return (x, len_x, y, len_y)

    def generate_batch(self, lang1, lang2, name):
        """
        Prepare a batch (for causal or non-causal mode).
        """
        params = self.params
        lang1_id = params.lang2id[lang1]
        lang2_id = params.lang2id[lang2] if lang2 is not None else None

        if lang2 is None:
            x, lengths = self.get_batch(name, lang1, stream=True)
            positions = None
            langs = x.clone().fill_(lang1_id) if params.n_langs > 1 else None
        elif lang1 == lang2:
            (x1, len1) = self.get_batch(name, lang1)
            (x2, len2) = (x1, len1)
            (x1, len1) = add_noise(x1, len1, self.params, len(self.data["dico"]) - 1)
            x, lengths, positions, langs = concat_batches(
                x1,
                len1,
                lang1_id,
                x2,
                len2,
                lang2_id,
                params.pad_index,
                params.eos_index,
                reset_positions=False,
            )
        else:
            (x1, len1, _, _), (x2, len2, _, _) = self.get_batch(name, lang1, lang2)
            x, lengths, positions, langs = concat_batches(
                x1,
                len1,
                lang1_id,
                x2,
                len2,
                lang2_id,
                params.pad_index,
                params.eos_index,
                reset_positions=True,
            )

        return (
            x,
            lengths,
            positions,
            langs,
            (None, None) if lang2 is None else (len1, len2),
        )

    def save_checkpoint(self, name, include_optimizers=True):
        """
        Save the model / checkpoints.
        """
        if not self.params.is_master:
            return

        path = os.path.join(self.params.dump_path, "%s.pth" % name)
        logger.info("Saving %s to %s ..." % (name, path))

        data = {
            "epoch": self.epoch,
            "n_total_iter": self.n_total_iter,
            "best_metrics": self.best_metrics,
            "best_stopping_criterion": self.best_stopping_criterion,
        }

        for name in self.MODEL_NAMES:
            logger.warning(f"Saving {name} parameters ...")

            model_attr = getattr(self, name)
            if isinstance(model_attr, list) and len(model_attr) > 1:
                for i, model in enumerate(model_attr):
                    data[f"{name}_{i}"] = model.state_dict()
            else:
                if isinstance(model_attr, list):
                    assert len(model_attr) == 1
                    model_attr = model_attr[0]

                data[name] = model_attr.state_dict()

        if include_optimizers:
            for name in self.optimizers.keys():
                logger.warning(f"Saving {name} optimizer ...")
                data[f"{name}_optimizer"] = self.optimizers[name].state_dict()

        data["dico_id2word"] = self.data["dico"].id2word
        data["dico_word2id"] = self.data["dico"].word2id
        data["dico_counts"] = self.data["dico"].counts
        data["params"] = {k: v for k, v in self.params.__dict__.items()}

        torch.save(data, path)

    def reload_checkpoint(self):
        """
        Reload a checkpoint if we find one.
        """
        checkpoint_path = os.path.join(self.params.dump_path, "checkpoint.pth")
        if not os.path.isfile(checkpoint_path):
            if self.params.reload_checkpoint == "":
                return
            else:
                checkpoint_path = self.params.reload_checkpoint
                assert os.path.isfile(checkpoint_path)
        logger.warning(f"Reloading checkpoint from {checkpoint_path} ...")
        data = torch.load(checkpoint_path, map_location="cpu")

        # reload model parameters
        for name in self.MODEL_NAMES:
            model_attr = getattr(self, name)
            if isinstance(model_attr, list) and len(model_attr) > 1:
                for i, model in enumerate(model_attr):
                    model.load_state_dict(data[f"{name}_{i}"])
            else:
                if isinstance(model_attr, list):
                    assert len(model_attr) == 1
                    model_attr = model_attr[0]
                model_attr.load_state_dict(data[name])

        # reload optimizers
        for name in self.optimizers.keys():
            if (
                False
            ):  # AMP checkpoint reloading is buggy, we cannot do that - TODO: fix - https://github.com/NVIDIA/apex/issues/250
                logger.warning(f"Reloading checkpoint optimizer {name} ...")
                self.optimizers[name].load_state_dict(data[f"{name}_optimizer"])
            else:  # instead, we only reload current iterations / learning rates
                logger.warning(f"Not reloading checkpoint optimizer {name}.")
                for group_id, param_group in enumerate(
                    self.optimizers[name].param_groups
                ):
                    if "num_updates" not in param_group:
                        logger.warning(f"No 'num_updates' for optimizer {name}.")
                        continue
                    logger.warning(
                        f"Reloading 'num_updates' and 'lr' for optimizer {name}."
                    )
                    param_group["num_updates"] = data[f"{name}_optimizer"][
                        "param_groups"
                    ][group_id]["num_updates"]
                    param_group["lr"] = self.optimizers[name].get_lr_for_step(
                        param_group["num_updates"]
                    )

        # reload main metrics
        self.epoch = data["epoch"] + 1
        self.n_total_iter = data["n_total_iter"]
        self.best_metrics = data["best_metrics"]
        self.best_stopping_criterion = data["best_stopping_criterion"]
        logger.warning(
            f"Checkpoint reloaded. Resuming at epoch {self.epoch} / iteration {self.n_total_iter} ..."
        )

    def save_periodic(self):
        """
        Save the models periodically.
        """
        if not self.params.is_master:
            return
        if (
            self.params.save_periodic > 0
            and self.epoch % self.params.save_periodic == 0
        ):
            self.save_checkpoint("periodic-%i" % self.epoch, include_optimizers=False)

    def save_best_model(self, scores):
        """
        Save best models according to given validation metrics.
        """
        if not self.params.is_master:
            return
        for metric, biggest in self.metrics:
            if metric not in scores:
                logger.warning('Metric "%s" not found in scores!' % metric)
                continue
            factor = 1 if biggest else -1
            if factor * scores[metric] > factor * self.best_metrics[metric]:
                self.best_metrics[metric] = scores[metric]
                logger.info("New best score for %s: %.6f" % (metric, scores[metric]))
                self.save_checkpoint("best-%s" % metric, include_optimizers=False)

    def end_epoch(self, scores):
        """
        End the epoch.
        """
        # stop if the stopping criterion has not improved after a certain number of epochs
        if self.stopping_criterion is not None and self.params.is_master:
            metric, biggest = self.stopping_criterion
            assert metric in scores, metric
            factor = 1 if biggest else -1
            if factor * scores[metric] > factor * self.best_stopping_criterion:
                self.best_stopping_criterion = scores[metric]
                logger.info(
                    "New best validation score: %f" % self.best_stopping_criterion
                )
                self.decrease_counts = 0
            else:
                logger.info(
                    "Not a better validation score (%i / %i)."
                    % (self.decrease_counts, self.decrease_counts_max)
                )
                self.decrease_counts += 1
            if self.decrease_counts > self.decrease_counts_max:
                logger.info(
                    "Stopping criterion has been below its best value for more "
                    "than %i epochs. Ending the experiment..."
                    % self.decrease_counts_max
                )
                if self.params.multi_gpu and "SLURM_JOB_ID" in os.environ:
                    os.system("scancel " + os.environ["SLURM_JOB_ID"])
                exit()
        self.save_checkpoint("checkpoint", include_optimizers=True)
        self.epoch += 1

    def round_batch(self, x, lengths, positions, langs):
        """
        For float16 only.
        Sub-sample sentences in a batch, and add padding,
        so that each dimension is a multiple of 8.
        """
        params = self.params
        if not params.fp16 or len(lengths) < 8:
            return x, lengths, positions, langs, None

        # number of sentences == 0 [8]
        bs1 = len(lengths)
        bs2 = 8 * (bs1 // 8)
        assert bs2 > 0 and bs2 % 8 == 0
        if bs1 != bs2:
            idx = torch.randperm(bs1)[:bs2]
            lengths = lengths[idx]
            slen = lengths.max().item()
            x = x[:slen, idx]
            positions = None if positions is None else positions[:slen, idx]
            langs = None if langs is None else langs[:slen, idx]
        else:
            idx = None

        # sequence length == 0 [8]
        ml1 = x.size(0)
        if ml1 % 8 != 0:
            pad = 8 - (ml1 % 8)
            ml2 = ml1 + pad
            x = torch.cat([x, torch.LongTensor(pad, bs2).fill_(params.pad_index)], 0)
            if positions is not None:
                positions = torch.cat(
                    [positions, torch.arange(pad)[:, None] + positions[-1][None] + 1], 0
                )
            if langs is not None:
                langs = torch.cat([langs, langs[-1][None].expand(pad, bs2)], 0)
            assert x.size() == (ml2, bs2)

        assert x.size(0) % 8 == 0
        assert x.size(1) % 8 == 0
        return x, lengths, positions, langs, idx

    def clm_step(self, lang1, lang2, lambda_coeff):
        """
        Next word prediction step (causal prediction).
        CLM objective.
        """
        assert lambda_coeff >= 0
        if lambda_coeff == 0:
            return
        params = self.params
        name = "model" if params.encoder_only else "decoder"
        model = getattr(self, name)
        model.train()

        # generate batch / select words to predict
        x, lengths, positions, langs, _ = self.generate_batch(lang1, lang2, "causal")
        x, lengths, positions, langs, _ = self.round_batch(x, lengths, positions, langs)
        alen = torch.arange(lengths.max(), dtype=torch.long, device=lengths.device)
        pred_mask = alen[:, None] < lengths[None] - 1
        if params.context_size > 0:  # do not predict without context
            pred_mask[: params.context_size] = 0
        y = x[1:].masked_select(pred_mask[:-1])
        assert pred_mask.sum().item() == y.size(0)

        # cuda
        x, lengths, langs, pred_mask, y = to_cuda(x, lengths, langs, pred_mask, y)

        # forward / loss
        tensor = model("fwd", x=x, lengths=lengths, langs=langs, causal=True)
        _, loss = model(
            "predict", tensor=tensor, pred_mask=pred_mask, y=y, get_scores=False
        )
        self.stats[
            ("CLM-%s" % lang1) if lang2 is None else ("CLM-%s-%s" % (lang1, lang2))
        ].append(loss.item())
        loss = lambda_coeff * loss

        # optimize
        self.optimize(loss)

        # number of processed sentences / words
        self.n_sentences += params.batch_size
        self.stats["processed_s"] += lengths.size(0)
        self.stats["processed_w"] += pred_mask.sum().item()

    def mlm_step(self, lang1, lang2, lambda_coeff, show_example=False):
        """
        Masked word prediction step.
        MLM objective is lang2 is None, TLM objective otherwise.
        """
        assert lambda_coeff >= 0
        if lambda_coeff == 0:
            return
        params = self.params
        name = "model" if params.encoder_only else "encoder"
        model = getattr(self, name)[0]
        model.train()

        # generate batch / select words to predict
        x, lengths, positions, langs, _ = self.generate_batch(lang1, lang2, "pred")
        x, lengths, positions, langs, _ = self.round_batch(x, lengths, positions, langs)
        x, y, pred_mask = self.mask_out(x, lengths)

        # log first batch of training
        if show_example:
            show_batch(
                logger,
                [("masked source", x.transpose(0, 1))],
                self.data["dico"],
                self.params.roberta_mode,
                "Training",
            )

        # cuda
        x, y, pred_mask, lengths, positions, langs = to_cuda(
            x, y, pred_mask, lengths, positions, langs
        )

        # forward / loss
        tensor = model(
            "fwd", x=x, lengths=lengths, positions=positions, langs=langs, causal=False
        )
        _, loss = model(
            "predict", tensor=tensor, pred_mask=pred_mask, y=y, get_scores=False
        )
        self.stats[
            ("MLM-%s" % lang1) if lang2 is None else ("MLM-%s-%s" % (lang1, lang2))
        ].append(loss.item())
        loss = lambda_coeff * loss

        # optimize
        self.optimize(loss)

        # number of processed sentences / words
        self.n_sentences += params.batch_size
        self.stats["processed_s"] += lengths.size(0)
        self.stats["processed_w"] += pred_mask.sum().item()

    def classif_step(self, lang1, lang2, lambda_coeff):
        """
        Masked word prediction step.
        MLM objective is lang2 is None, TLM objective otherwise.
        """
        assert lambda_coeff >= 0
        if lambda_coeff == 0:
            return
        params = self.params
        name = "model" if params.encoder_only else "encoder"
        model = getattr(self, name)[0]
        model.train()

        assert self.classifier is not None
        classifier = self.classifier[0].train()

        lang1_id = params.lang2id[lang1]

        (x1, len1, _, _), (y, len2, _, _) = self.get_batch("classif", lang1, lang2)
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
        scores, loss = classifier(enc1, y, pred_mask)

        self.stats[("Classif-%s-%s" % (lang1, lang2))].append(loss.item())
        loss = lambda_coeff * loss

        # optimize
        self.optimize(loss)

        # number of processed sentences / words
        self.n_sentences += params.batch_size
        self.stats["processed_s"] += len2.size(0)
        self.stats["processed_w"] += (len2 - 1).sum().item()


class SingleTrainer(Trainer):
    def __init__(self, model, data, params, classifier=None):

        self.MODEL_NAMES = ["model"]
        if classifier is not None:
            self.MODEL_NAMES.append("classifier")

        # model / data / params
        self.model = model
        self.data = data
        self.params = params
        if classifier is not None:
            self.classifier = [classifier]

        super().__init__(data, params)


class EncDecTrainer(Trainer):
    def __init__(self, encoder, decoder, data, params, second_decoder=None):

        self.MODEL_NAMES = ["encoder", "decoder"]
        # if second_decoder is not None:
        #     self.MODEL_NAMES.append('decoder2')

        # model / data / params
        self.encoder = encoder
        self.decoder = decoder
        self.data = data
        self.params = params
        self.generation_index = 0
        self.generation_inputs = ()
        self.len_generation_inputs = ()
        self.generated_data = ()
        self.len_generated_data = ()

        super().__init__(data, params)

    def mt_step(
        self,
        lang1,
        lang2,
        lambda_coeff,
        span=None,
        deobfuscate=False,
        deobfuscate_p=None,
        show_example=False,
    ):
        """
        Machine translation step.
        Can also be used for denoising auto-encoding.
        """
        assert lambda_coeff >= 0
        if lambda_coeff == 0:
            return
        assert (
            deobfuscate_p is not None and 0 <= deobfuscate_p and deobfuscate_p <= 1
        ) or not deobfuscate
        # assert deobfuscate or span is not None
        params = self.params
        self.train_mode()

        lang1_id = params.lang2id[lang1]
        lang2_id = params.lang2id[lang2]

        decoder = (
            self.decoder[lang2_id] if params.separate_decoders else self.decoder[0]
        )

        spans = None
        # generate batch
        if lang1 == lang2:
            assert not span, "spans not supported for AE steps"
            (x1, len1) = self.get_batch("ae", lang1)
            (x2, len2) = (x1, len1)
            (x1, len1) = add_noise(x1, len1, self.params, len(self.data["dico"]) - 1)
        elif span:
            (
                (x1, len1, _, _),
                (x2, len2, _, _),
                (spans, len_spans, _, _),
            ) = self.get_batch("mt_spans", lang1, lang2, span=span)
        elif deobfuscate:
            (x1, len1, _, _), (x2, len2, _, _) = self.get_batch("mt", lang1, lang2)
            (x1, len1, x2, len2) = self.deobfuscate_by_variable(
                x1, x2, deobfuscate_p, params.roberta_mode, rng=None
            )
            if x1 is None:
                return
        else:
            (x1, len1, _, _), (x2, len2, _, _) = self.get_batch("mt", lang1, lang2)

        # log first batch of training
        if show_example:
            show_batch(
                logger,
                [("source", x1.transpose(0, 1)), ("target", x2.transpose(0, 1))],
                self.data["dico"],
                self.params.roberta_mode,
                f"Train {lang1}-{lang2}",
            )

        langs1 = x1.clone().fill_(lang1_id)
        langs2 = x2.clone().fill_(lang2_id)

        # target words to predict
        alen = torch.arange(len2.max(), dtype=torch.long, device=len2.device)
        # do not predict anything given the last target word
        pred_mask = alen[:, None] < len2[None] - 1
        y = x2[1:].masked_select(pred_mask[:-1])
        assert len(y) == (len2 - 1).sum().item()

        # cuda
        x1, len1, langs1, x2, len2, langs2, y, spans = to_cuda(
            x1, len1, langs1, x2, len2, langs2, y, spans
        )

        # encode source sentence
        enc1 = self.encoder[0](
            "fwd", x=x1, lengths=len1, langs=langs1, causal=False, spans=spans
        )
        enc1 = enc1.transpose(0, 1)

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
        _, loss = decoder(
            "predict", tensor=dec2, pred_mask=pred_mask, y=y, get_scores=False
        )

        if deobfuscate:
            self.stats[("DO-%s-%s" % (lang1, lang2))].append(loss.item())
        else:
            key = (lang1, lang2) if span is None else (lang1, lang2, span)
            self.stats[
                ("AE-%s" % lang1) if lang1 == lang2 else ("MT-%s" % "-".join(key))
            ].append(loss.item())
        loss = lambda_coeff * loss

        # optimize
        self.optimize(loss)

        # number of processed sentences / words
        self.n_sentences += params.batch_size
        self.stats["processed_s"] += len2.size(0)
        self.stats["processed_w"] += (len2 - 1).sum().item()

    def train_mode(self):
        [enc.train() for enc in self.encoder]
        if self.decoder is not None:
            [dec.train() for dec in self.decoder]

    def eval_mode(self):
        [enc.eval() for enc in self.encoder]
        if self.decoder is not None:
            [dec.eval() for dec in self.decoder]

    def bt_step(self, lang1, lang2, lang3, lambda_coeff, sample_temperature):
        """
        Back-translation step for machine translation.
        """
        if sample_temperature == 0:
            sample_temperature = None
        assert lambda_coeff >= 0
        if lambda_coeff == 0:
            return
        assert lang1 == lang3 and lang1 != lang2 and lang2 is not None
        params = self.params

        lang1_id = params.lang2id[lang1]
        lang2_id = params.lang2id[lang2]

        _encoder = self.encoder[0].module if params.multi_gpu else self.encoder[0]
        if params.separate_decoders:
            _decoder_lang1 = (
                self.decoder[lang1_id].module
                if params.multi_gpu
                else self.decoder[lang1_id]
            )
            _decoder_lang2 = (
                self.decoder[lang2_id].module
                if params.multi_gpu
                else self.decoder[lang2_id]
            )
        else:
            _decoder_lang1 = _decoder_lang2 = (
                self.decoder[0].module if params.multi_gpu else self.decoder[0]
            )

        decoder1 = (
            self.decoder[lang1_id] if params.separate_decoders else self.decoder[0]
        )

        # generate source batch
        x1, len1 = self.get_batch("bt", lang1)
        langs1 = x1.clone().fill_(lang1_id)

        # cuda
        x1, len1, langs1 = to_cuda(x1, len1, langs1)

        # generate a translation
        with torch.no_grad():

            # evaluation mode
            self.eval_mode()

            # encode source sentence and translate it
            enc1 = _encoder("fwd", x=x1, lengths=len1, langs=langs1, causal=False)
            enc1 = enc1.transpose(0, 1)

            len_v = (3 * len1 + 10).clamp(max=params.max_len)
            if self.params.fp16:
                enc1 = enc1.half()
            x2, len2 = _decoder_lang2.generate(
                enc1,
                len1,
                lang2_id,
                max_len=len_v,
                sample_temperature=sample_temperature,
            )
            langs2 = x2.clone().fill_(lang2_id)

            # free CUDA memory
            del enc1

        self.generation_index += 1
        # training mode
        self.train_mode()

        # encode generate sentence
        enc2 = self.encoder[0]("fwd", x=x2, lengths=len2, langs=langs2, causal=False)
        enc2 = enc2.transpose(0, 1)

        # words to predict
        alen = torch.arange(len1.max(), dtype=torch.long, device=len1.device)
        # do not predict anything given the last target word
        pred_mask = alen[:, None] < len1[None] - 1
        y1 = x1[1:].masked_select(pred_mask[:-1])

        # decode original sentence
        dec3 = decoder1(
            "fwd",
            x=x1,
            lengths=len1,
            langs=langs1,
            causal=True,
            src_enc=enc2,
            src_len=len2,
        )

        # loss
        _, loss = decoder1(
            "predict", tensor=dec3, pred_mask=pred_mask, y=y1, get_scores=False
        )
        self.stats[("BT-%s-%s-%s" % (lang1, lang2, lang3))].append(loss.item())
        loss = lambda_coeff * loss

        # optimize
        self.optimize(loss)

        # number of processed sentences / words
        self.n_sentences += params.batch_size
        self.stats["processed_s"] += len1.size(0)
        self.stats["processed_w"] += (len1 - 1).sum().item()
