# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import math
from logging import getLogger

import numpy as np
import torch

logger = getLogger()


class StreamDataset(object):
    def __init__(self, sent, pos, bs, params):
        """
        Prepare batches for data iterator.
        """
        bptt = params.bptt
        self.eos = params.eos_index

        # checks
        assert len(pos) == (sent == self.eos).sum()
        assert len(pos) == (sent[pos[:, 1]] == self.eos).sum()

        n_tokens = len(sent)
        n_batches = math.ceil(n_tokens / (bs * bptt))
        t_size = n_batches * bptt * bs

        buffer = np.zeros(t_size, dtype=sent.dtype) + self.eos
        buffer[t_size - n_tokens :] = sent
        buffer = buffer.reshape((bs, n_batches * bptt)).T
        self.data = np.zeros((n_batches * bptt + 1, bs), dtype=sent.dtype) + self.eos
        self.data[1:] = buffer

        self.bptt = bptt
        self.n_tokens = n_tokens
        self.n_batches = n_batches
        self.n_sentences = len(pos)
        self.lengths = torch.LongTensor(bs).fill_(bptt)
        self.add_eof = params.add_eof_to_stream

    def __len__(self):
        """
        Number of sentences in the dataset.
        """
        return self.n_sentences

    def select_data(self, a, b):
        """
        Only select a subset of the dataset.
        """
        if not (0 <= a < b <= self.n_batches):
            logger.warning("Invalid split values: %i %i - %i" % (a, b, self.n_batches))
            return
        assert 0 <= a < b <= self.n_batches
        logger.info("Selecting batches from %i to %i ..." % (a, b))

        # sub-select
        self.data = self.data[a * self.bptt : b * self.bptt]
        self.n_batches = b - a
        self.n_sentences = (self.data == self.eos).sum().item()

    def get_iterator(self, shuffle, subsample=1):
        """
        Return a sentences iterator.
        """
        indexes = (np.random.permutation if shuffle else range)(
            self.n_batches // subsample
        )
        for i in indexes:
            a = self.bptt * i
            b = self.bptt * (i + 1)
            batch = self.data[a:b]
            if self.add_eof:
                batch[0] = self.eos
            yield torch.from_numpy(batch.astype(np.int64)), self.lengths


class Dataset(object):
    def __init__(self, sent, pos, params):

        self.eos_index = params.eos_index
        self.pad_index = params.pad_index
        self.batch_size = params.batch_size
        self.max_batch_size = params.max_batch_size

        self.sent = sent
        self.pos = pos
        self.lengths = self.pos[:, 1] - self.pos[:, 0]

        # check number of sentences
        assert len(self.pos) == (self.sent == self.eos_index).sum()

        # # remove empty sentences
        self.remove_empty_sentences()

        # sanity checks
        self.check()

    def __len__(self):
        """
        Number of sentences in the dataset.
        """
        return len(self.pos)

    def check(self):
        """
        Sanity checks.
        """
        eos = self.eos_index
        # check sentences indices
        assert len(self.pos) == (self.sent[self.pos[:, 1]] == eos).sum()
        # assert self.lengths.min() > 0                                     # check empty sentences

    def batch_sentences(self, sentences):
        """
        Take as input a list of n sentences (torch.LongTensor vectors) and return
        a tensor of size (slen, n) where slen is the length of the longest
        sentence, and a vector lengths containing the length of each sentence.
        """
        # sentences = sorted(sentences, key=lambda x: len(x), reverse=True)
        lengths = torch.LongTensor([len(s) + 2 for s in sentences])
        sent = torch.LongTensor(lengths.max().item(), lengths.size(0)).fill_(
            self.pad_index
        )

        sent[0] = self.eos_index
        for i, s in enumerate(sentences):
            if lengths[i] > 2:  # if sentence not empty
                sent[1 : lengths[i] - 1, i].copy_(torch.from_numpy(s.astype(np.int64)))
            sent[lengths[i] - 1, i] = self.eos_index

        return sent, lengths

    def remove_empty_sentences(self):
        """
        Remove empty sentences.
        """
        init_size = len(self.pos)
        indices = np.arange(len(self.pos))
        indices = indices[self.lengths[indices] > 0]
        self.pos = self.pos[indices]
        self.lengths = self.pos[:, 1] - self.pos[:, 0]
        logger.info("Removed %i empty sentences." % (init_size - len(indices)))
        self.check()

    def remove_long_sentences(self, max_len):
        """
        Remove sentences exceeding a certain length.
        """
        assert max_len >= 0
        if max_len == 0:
            return
        init_size = len(self.pos)
        indices = np.arange(len(self.pos))
        indices = indices[self.lengths[indices] <= max_len]
        self.pos = self.pos[indices]
        self.lengths = self.pos[:, 1] - self.pos[:, 0]
        logger.info("Removed %i too long sentences." % (init_size - len(indices)))
        self.check()

    def select_data(self, a, b):
        """
        Only select a subset of the dataset.
        """
        assert 0 <= a < b <= len(self.pos)
        logger.info("Selecting sentences from %i to %i ..." % (a, b))

        # sub-select
        self.pos = self.pos[a:b]
        self.lengths = self.pos[:, 1] - self.pos[:, 0]

        # re-index
        min_pos = self.pos.min()
        max_pos = self.pos.max()
        self.pos -= min_pos
        self.sent = self.sent[min_pos : max_pos + 1]

        # sanity checks
        self.check()

    def get_batches_iterator(self, batches, return_indices):
        """
        Return a sentences iterator, given the associated sentence batches.
        """
        assert type(return_indices) is bool

        for sentence_ids in batches:
            if 0 < self.max_batch_size < len(sentence_ids):
                np.random.shuffle(sentence_ids)
                sentence_ids = sentence_ids[: self.max_batch_size]
            pos = self.pos[sentence_ids]
            sent = [self.sent[a:b] for a, b in pos]
            sent = self.batch_sentences(sent)
            yield (sent, sentence_ids) if return_indices else sent

    def get_iterator(
        self,
        shuffle,
        tokens_per_batch,
        group_by_size=False,
        n_sentences=-1,
        seed=None,
        return_indices=False,
    ):
        """
        Return a sentences iterator.
        """
        assert seed is None or shuffle is True and type(seed) is int
        rng = np.random.RandomState(seed)
        n_sentences = len(self.pos) if n_sentences == -1 else n_sentences
        n_sentences = min(len(self.pos), n_sentences)
        assert 0 < n_sentences <= len(self.pos)
        assert type(shuffle) is bool and type(group_by_size) is bool
        # assert group_by_size is False or shuffle is True

        # sentence lengths
        lengths = self.lengths + 2

        # select sentences to iterate over
        if shuffle:
            indices = rng.permutation(len(self.pos))[:n_sentences]
        else:
            indices = np.arange(n_sentences)

        # group sentences by lengths
        if group_by_size:
            indices = indices[np.argsort(lengths[indices], kind="mergesort")]

        # create batches - either have a fixed number of sentences, or a similar number of tokens
        if tokens_per_batch == -1:
            batches = np.array_split(
                indices, math.ceil(len(indices) * 1.0 / self.batch_size)
            )
        else:
            batch_ids = np.cumsum(lengths[indices]) // tokens_per_batch
            _, bounds = np.unique(batch_ids, return_index=True)
            batches = [
                indices[bounds[i] : bounds[i + 1]] for i in range(len(bounds) - 1)
            ]
            if bounds[-1] < len(indices):
                batches.append(indices[bounds[-1] :])

        # optionally shuffle batches
        if shuffle:
            rng.shuffle(batches)

        # sanity checks
        assert n_sentences == sum([len(x) for x in batches])
        assert lengths[indices].sum() == sum([lengths[x].sum() for x in batches])
        # assert set.union(*[set(x.tolist()) for x in batches]) == set(range(n_sentences))  # slow

        # return the iterator
        return self.get_batches_iterator(batches, return_indices)


class ParallelDataset(Dataset):
    def __init__(
        self, sent_list, pos_list, params, span_prediction=False, has_sentences_id=None
    ):
        """
        :param sent_list: list of sentences tensors. The order is (src, tgt, (optional) span)
        :param pos_list: list of positions of each sample
        :param span_prediction: whether it predicts spans or sentences

        The length of the lists should be 2 when doing translation or span classification
         and 3 when doing translation using spans
        """
        assert len(pos_list) == 2 or len(pos_list) == 3
        self.eos_index = params.eos_index
        self.pad_index = params.pad_index
        self.sep_index = params.sep_index
        self.batch_size = params.batch_size
        self.max_batch_size = params.max_batch_size
        self.has_sentences_ids = (
            has_sentences_id
            if has_sentences_id is not None
            else params.has_sentences_ids
        )

        self.sent_list = sent_list
        self.pos_list = pos_list
        self.lengths_list = [pos[:, 1] - pos[:, 0] for pos in self.pos_list]
        self.span_prediction = span_prediction
        self.mt_with_spans = len(self.pos_list) == 3

        # check number of sentences
        assert all(
            [len(pos) == len(self) > 0 for pos in self.pos_list]
        ), "number of sentences do not match"

        # remove empty sentences
        self.remove_empty_sentences()

        # sanity checks
        self.check()

    def __len__(self):
        """
        Number of sentences in the dataset.
        """
        return len(self.pos_list[0])

    def batch_sentences(self, sentences, split_sentences_ids=None):
        """
        Take as input a list of n sentences (torch.LongTensor vectors) and return
        a tensor of size (slen, n) where slen is the length of the longest
        sentence, and a vector lengths containing the length of each sentence.
        """
        if split_sentences_ids is None:
            split_sentences_ids = self.has_sentences_ids
        if split_sentences_ids:
            sentences_WITH_IDS = sentences
            sentences = []
            ids_ = []
            for s in sentences_WITH_IDS:
                pos = np.where(s == self.sep_index)[0][0]
                sentences.append(s[pos + 1 :])
                ids_.append(s[:pos])

            lengths_ids = torch.LongTensor([len(i) + 2 for i in ids_])
            ids = torch.LongTensor(lengths_ids.max().item(), lengths_ids.size(0)).fill_(
                self.pad_index
            )

            ids[0] = self.eos_index
            for i, s in enumerate(ids_):
                if lengths_ids[i] > 2:  # if sentence not empty
                    ids[1 : lengths_ids[i] - 1, i].copy_(
                        torch.from_numpy(s.astype(np.int64))
                    )
                ids[lengths_ids[i] - 1, i] = self.eos_index

        else:
            # sentences = sorted(sentences, key=lambda x: len(x), reverse=True)
            ids = None
            lengths_ids = None

        lengths = torch.LongTensor([len(s) + 2 for s in sentences])
        sent = torch.LongTensor(lengths.max().item(), lengths.size(0)).fill_(
            self.pad_index
        )

        sent[0] = self.eos_index
        for i, s in enumerate(sentences):
            if lengths[i] > 2:  # if sentence not empty
                sent[1 : lengths[i] - 1, i].copy_(torch.from_numpy(s.astype(np.int64)))
            sent[lengths[i] - 1, i] = self.eos_index

        return sent, lengths, ids, lengths_ids

    def check(self):
        """
        Sanity checks.
        """
        eos = self.eos_index

        # check number of sentences
        assert all([len(pos) == len(self) > 0 for pos in self.pos_list])

        # check sentences indices
        for i, (pos, sent) in enumerate(zip(self.pos_list, self.sent_list)):
            assert (
                len(pos) == (sent[pos[:, 1]] == eos).sum()
            ), f"size of pos: {len(pos)}. num eos:{(sent == self.eos_index).sum()}"
            # check dictionary indices
            assert eos <= sent.min() < sent.max()
            if self.span_prediction:
                break
            if i == 1:
                break

        if self.span_prediction:
            assert (
                len(self.pos_list) == len(self.sent_list) == len(self.lengths_list) == 2
            )
            assert len(self.sent_list[0]) == len(self.sent_list[1])
            if self.has_sentences_ids:
                assert all(self.lengths_list[0] > self.lengths_list[1])
            else:
                assert all(self.lengths_list[0] == self.lengths_list[1])

        if self.mt_with_spans:
            # the spans are in position 3
            assert (
                len(self.pos_list) == len(self.sent_list) == len(self.lengths_list) == 3
            )
            assert len(self.sent_list[0]) == len(self.sent_list[2])
            if self.has_sentences_ids:
                assert all(self.lengths_list[0] > self.lengths_list[2])
            else:
                assert all(self.lengths_list[0] == self.lengths_list[2])

        # check empty sentences
        for lengths in self.lengths_list:
            assert lengths.min() > 0

    def remove_empty_sentences(self):
        """
        Remove empty sentences.
        """
        init_size = len(self)
        indices = np.arange(len(self))
        for lengths in self.lengths_list:
            indices = indices[lengths[indices] > 0]
        self.pos_list = [pos[indices] for pos in self.pos_list]
        self.lengths_list = [pos[:, 1] - pos[:, 0] for pos in self.pos_list]
        logger.info("Removed %i empty sentences." % (init_size - len(indices)))
        self.check()

    def remove_long_sentences(self, max_len):
        """
        Remove sentences exceeding a certain length.
        """
        assert max_len >= 0
        if max_len == 0:
            return
        init_size = len(self)
        indices = np.arange(len(self))
        for lengths in self.lengths_list:
            indices = indices[lengths[indices] <= max_len]
        self.pos_list = [pos[indices] for pos in self.pos_list]
        self.lengths_list = [pos[:, 1] - pos[:, 0] for pos in self.pos_list]
        logger.info("Removed %i too long sentences." % (init_size - len(indices)))
        self.check()

    def select_data(self, a, b):
        """
        Only select a subset of the dataset.
        """
        assert 0 <= a < b <= len(self)
        logger.info("Selecting sentences from %i to %i ..." % (a, b))

        # sub-select
        self.pos_list = [pos[a:b] for pos in self.pos_list]
        self.lengths_list = [pos[:, 1] - pos[:, 0] for pos in self.pos_list]

        # re-index
        min_pos_list = [pos.min() for pos in self.pos_list]
        max_pos_list = [pos.max() for pos in self.pos_list]
        self.pos_list = [
            pos - min_pos for pos, min_pos in zip(self.pos_list, min_pos_list)
        ]
        self.sent_list = [
            sent[min_pos : max_pos + 1]
            for sent, min_pos, max_pos in zip(
                self.sent_list, min_pos_list, max_pos_list
            )
        ]

        # sanity checks
        self.check()

    def get_batches_iterator(self, batches, return_indices):
        """
        Return a sentences iterator, given the associated sentence batches.
        """
        assert type(return_indices) is bool

        for sentence_ids in batches:
            if 0 < self.max_batch_size < len(sentence_ids):
                np.random.shuffle(sentence_ids)
                sentence_ids = sentence_ids[: self.max_batch_size]
            pos = [pos[sentence_ids] for pos in self.pos_list]

            split_sentences_id = [self.has_sentences_ids for i in range(len(pos))]
            if self.span_prediction:
                assert len(split_sentences_id) == 2
                split_sentences_id[1] = False
            if self.mt_with_spans:
                assert len(split_sentences_id) == 3
                split_sentences_id[2] = False
            sents = [
                self.batch_sentences([sent[a:b] for a, b in pos], split_id)
                for split_id, pos, sent in zip(split_sentences_id, pos, self.sent_list)
            ]
            yield (sents.append(sentence_ids)) if return_indices else sents

    def get_iterator(
        self,
        shuffle,
        tokens_per_batch,
        group_by_size=False,
        n_sentences=-1,
        return_indices=False,
    ):
        """
        Return a sentences iterator.
        """
        n_sentences = len(self) if n_sentences == -1 else n_sentences
        n_sentences = min(len(self), n_sentences)
        assert 0 < n_sentences <= len(self)
        assert type(shuffle) is bool and type(group_by_size) is bool

        # sentence lengths
        lengths = sum(self.lengths_list) + 2 * len(self.lengths_list)

        # select sentences to iterate over
        if shuffle:
            indices = np.random.permutation(len(self))[:n_sentences]
        else:
            indices = np.arange(n_sentences)

        # group sentences by lengths
        if group_by_size:
            indices = indices[np.argsort(lengths[indices], kind="mergesort")]

        # create batches - either have a fixed number of sentences, or a similar number of tokens
        if tokens_per_batch == -1:
            batches = np.array_split(
                indices, math.ceil(len(indices) * 1.0 / self.batch_size)
            )
        else:
            batch_ids = np.cumsum(lengths[indices]) // tokens_per_batch
            _, bounds = np.unique(batch_ids, return_index=True)
            batches = [
                indices[bounds[i] : bounds[i + 1]] for i in range(len(bounds) - 1)
            ]
            if bounds[-1] < len(indices):
                batches.append(indices[bounds[-1] :])

        # optionally shuffle batches
        if shuffle:
            np.random.shuffle(batches)

        # sanity checks
        assert n_sentences == sum([len(x) for x in batches])
        assert lengths[indices].sum() == sum([lengths[x].sum() for x in batches])
        # assert set.union(*[set(x.tolist()) for x in batches]) == set(range(n_sentences))  # slow

        # return the iterator
        return self.get_batches_iterator(batches, return_indices)
