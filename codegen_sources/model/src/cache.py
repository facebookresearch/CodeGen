# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import pickle
import random
from logging import getLogger
from pathlib import Path

import torch

logger = getLogger()


class Cache(object):
    def __init__(self, elements=None, params=None):
        self.eos_index = params.eos_index
        self.pad_index = params.pad_index
        self.elements = elements
        self.st_remove_proba = params.st_remove_proba
        self.params = params

    def sample(self, size):
        raise NotImplementedError()

    def add(self, new_elements, keys=None):
        raise NotImplementedError

    def exists(self, element_id):
        raise NotImplementedError

    def __len__(self):
        return len(self.elements)

    def sample_batch(self, n):
        sampled_elements = self.sample(n)

        sent1 = [e[0] for e in sampled_elements]
        len1 = [e[1] for e in sampled_elements]
        sent2 = [e[2] for e in sampled_elements]
        len2 = [e[3] for e in sampled_elements]

        return self.batch_sequences(sent1, len1), self.batch_sequences(sent2, len2)

    def batch_sequences(self, sequences: list, lengths: list):
        """
        Take as input a list of n sequences (torch.LongTensor vectors) and return
        a tensor of size (slen, n) where slen is the length of the longest
        sentence, and a vector lengths containing the length of each sentence.
        """
        assert all(
            [
                len(s) >= l
                and s[0].item() == self.eos_index
                and s[l - 1].item() == self.eos_index
                for s, l in zip(sequences, lengths)
            ]
        )
        lengths = torch.LongTensor(lengths)
        sent = torch.LongTensor(max(lengths), len(lengths)).fill_(self.pad_index)
        assert min(lengths) > 2
        for i, s in enumerate(sequences):
            sent[0 : lengths[i], i].copy_(s[: lengths[i]])

        return sent, lengths

    def limit_tokens_per_batch(self, sampled_elements):
        max_len = 0
        for i, (s1, l1, s2, l2) in enumerate(sampled_elements):
            max_len = max(max_len, l1, l2)
            tokens_in_batch = max_len * (i + 1)
            if tokens_in_batch > self.params.tokens_per_batch:
                return i - 1
        return len(sampled_elements)

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self.elements, f)

    @classmethod
    def from_file(cls, cache_path, params):
        print(cache_path)
        with open(cache_path, "rb") as pickle_in:
            elements = pickle.load(pickle_in)
        return cls(elements, params)

    def load(self, path):
        """Loads elements from a path and adds them to the existing elements"""
        if not Path(path).exists():
            raise ValueError(f"{path} not found")
        with open(path, "rb") as pickle_in:
            elements = pickle.load(pickle_in)
        assert isinstance(elements, list)
        self.add(elements)


class ListCache(Cache):
    def __init__(self, elements: list = None, params=None):
        super().__init__(elements, params)
        if elements is None:
            self.elements = []
        else:
            self.elements = elements
        self.tokens_per_batch = params.tokens_per_batch

    def exists(self, element_id):
        # for ListCache, always we don't store the ID
        return False

    def sample(self, n):
        indices = random.sample(list(range(len(self.elements))), n)
        sampled = [self.elements[i] for i in indices]
        if self.params.st_limit_tokens_per_batch:
            limit = self.limit_tokens_per_batch(sampled)
            indices = indices[:limit]
            sampled = sampled[:limit]

        if random.random() < self.st_remove_proba:
            indices = set(indices)
            self.elements = [e for i, e in enumerate(self.elements) if i not in indices]
        return sampled

    def add(self, new_elements, keys=None):
        self.elements.extend(new_elements)


class RoundRobinCache(Cache):
    def __init__(self, elements: list = None, params=None):
        super().__init__(elements, params)
        self.cache_size = params.cache_size
        if elements is None:
            self.elements = []
        else:
            if len(elements) > self.cache_size:
                logger.info(
                    f"Taking only the first {self.cache_size} elements from {len(elements)} initial cache elements"
                )
                self.elements = elements[: self.cache_size]
            else:
                self.elements = elements
        self.tokens_per_batch = params.tokens_per_batch
        self.current_index = 0

    def exists(self, element_id):
        # for ListCache, always we don't store the ID
        return False

    def sample(self, n):
        indices = random.sample(list(range(len(self.elements))), n)
        sampled = [self.elements[i] for i in indices]
        if self.params.st_limit_tokens_per_batch:
            limit = self.limit_tokens_per_batch(sampled)
            sampled = sampled[:limit]
        return sampled

    def add(self, new_elements, keys=None):
        if len(new_elements) > self.cache_size:
            logger.info(
                f"Cannot add {len(new_elements)} in the cache of size {self.cache_size}. Truncating."
            )
            new_elements = new_elements[: self.cache_size]
        if len(self.elements) < self.cache_size:
            last_fitting = self.cache_size - len(self.elements)
            self.elements.extend(new_elements[:last_fitting])
            if last_fitting < len(new_elements):
                for i, e in enumerate(new_elements[last_fitting:]):
                    self.elements[i] = e
            self.current_index = len(new_elements) - last_fitting
        else:
            for i, e in enumerate(new_elements):
                self.elements[(self.current_index + i) % self.cache_size] = e
            self.current_index = (
                self.current_index + len(new_elements)
            ) % self.cache_size
