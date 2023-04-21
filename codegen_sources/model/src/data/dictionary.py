# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import typing as tp
from pathlib import Path
from logging import getLogger

import numpy as np
import torch

logger = getLogger()

D = tp.TypeVar("D", bound="Dictionary")


BOS_WORD = "<s>"
EOS_WORD = "</s>"
PAD_WORD = "<pad>"
UNK_WORD = "<unk>"

SPECIAL_WORD = "<special%i>"
SPECIAL_WORDS = 10

OBF = {"CLASS": "CLASS_%i", "FUNC": "FUNC_%i", "VAR": "VAR_%i"}
OBFS = {"CLASS": 100, "FUNC": 200, "VAR": 200}
OBFS_TOTAL = sum(OBFS.values())


ENDBLOCK = "#ENDBLOCK"
ENDFUNC = "#ENDFUNC"
ENDCLASS = "#ENDCLASS"

SEP_WORD = SPECIAL_WORD % 0
MASK_WORD = SPECIAL_WORD % 1

NUM_SPECIAL_TOKENS = 4 + SPECIAL_WORDS + OBFS_TOTAL


class Dictionary:
    def __init__(self, id2word, word2id, counts) -> None:
        assert len(id2word) == len(word2id) == len(counts), (
            len(id2word),
            len(word2id),
            len(counts),
        )
        self.id2word = id2word
        self.word2id = word2id
        self.counts = counts
        self.bos_index = word2id[BOS_WORD]
        self.eos_index = word2id[EOS_WORD]
        self.pad_index = word2id[PAD_WORD]
        self.unk_index = word2id[UNK_WORD]
        if OBF["CLASS"] % 0 in word2id:
            self.obf_index = {
                "CLASS": word2id[OBF["CLASS"] % 0],
                "FUNC": word2id[OBF["FUNC"] % 0],
                "VAR": word2id[OBF["VAR"] % 0],
            }
        else:
            self.obf_index = dict()
        self.n_obf_tokens = OBFS_TOTAL
        self.check_valid()

    def __len__(self) -> int:
        """
        Returns the number of words in the dictionary.
        """
        return len(self.id2word)

    def __getitem__(self, i: int) -> str:
        """
        Returns the word of the specified index.
        """
        return self.id2word[i]

    def __contains__(self, w: str) -> bool:
        """
        Returns whether a word is in the dictionary.
        """
        return w in self.word2id

    def __eq__(self, y):
        """
        Compare this dictionary with another one.
        """
        self.check_valid()
        y.check_valid()
        if len(self.id2word) != len(y):
            return False
        return all(self.id2word[i] == y[i] for i in range(len(y)))

    def check_valid(self) -> None:
        """
        Check that the dictionary is valid.
        """
        assert self.bos_index == 0
        assert self.eos_index == 1
        assert self.pad_index == 2
        assert self.unk_index == 3
        assert all(
            self.id2word[4 + i] == SPECIAL_WORD % i for i in range(SPECIAL_WORDS)
        )

        for TYPE in ["CLASS", "FUNC", "VAR"]:
            assert all(
                len(self.obf_index) == 0
                or self.id2word[i + self.obf_index[TYPE]] == OBF[TYPE] % i
                for i in range(OBFS[TYPE])
            )
        assert len(self.id2word) == len(self.word2id) == len(self.counts)
        assert set(self.word2id.keys()) == set(self.counts.keys())
        for i in range(len(self.id2word)):
            assert self.word2id[self.id2word[i]] == i
        last_count = 1e18
        for i in range(NUM_SPECIAL_TOKENS, len(self.id2word) - 1):
            count = self.counts[self.id2word[i]]
            assert count <= last_count
            last_count = count

    def index(self, word: str, no_unk: bool = False) -> int:
        """
        Returns the index of the specified word.
        """
        try:  # faster to ask for forginess if need be
            return self.word2id[word]
        except KeyError as e:
            if no_unk:
                raise e
            return self.unk_index

    def max_vocab(self, max_vocab):
        """
        Limit the vocabulary size.
        """
        assert max_vocab >= 1
        init_size = len(self)
        self.id2word = {k: v for k, v in self.id2word.items() if k < max_vocab}
        self.word2id = {v: k for k, v in self.id2word.items()}
        self.counts = {k: v for k, v in self.counts.items() if k in self.word2id}
        self.check_valid()
        logger.info(
            "Maximum vocabulary size: %i. Dictionary size: %i -> %i (removed %i words)."
            % (max_vocab, init_size, len(self), init_size - len(self))
        )

    def min_count(self, min_count):
        """
        Threshold on the word frequency counts.
        """
        assert min_count >= 0
        init_size = len(self)
        self.id2word = {
            k: v
            for k, v in self.id2word.items()
            if self.counts[self.id2word[k]] >= min_count or k < NUM_SPECIAL_TOKENS
        }
        self.word2id = {v: k for k, v in self.id2word.items()}
        self.counts = {k: v for k, v in self.counts.items() if k in self.word2id}
        self.check_valid()
        logger.info(
            "Minimum frequency count: %i. Dictionary size: %i -> %i (removed %i words)."
            % (min_count, init_size, len(self), init_size - len(self))
        )

    @classmethod
    def read_vocab(cls: tp.Type[D], vocab_path: tp.Union[str, Path]) -> D:
        """
        Create a dictionary from a vocabulary file.
        """
        vocab_path = str(vocab_path)
        skipped = 0
        assert os.path.isfile(vocab_path), vocab_path
        word2id = {BOS_WORD: 0, EOS_WORD: 1, PAD_WORD: 2, UNK_WORD: 3}
        for i in range(SPECIAL_WORDS):
            word2id[SPECIAL_WORD % i] = 4 + i
        for i in range(OBFS_TOTAL):
            if i < OBFS["CLASS"]:
                word2id[OBF["CLASS"] % i] = 4 + SPECIAL_WORDS + i
            elif i < OBFS["CLASS"] + OBFS["FUNC"]:
                word2id[OBF["FUNC"] % (i - OBFS["CLASS"])] = 4 + SPECIAL_WORDS + i
            else:
                word2id[OBF["VAR"] % (i - OBFS["CLASS"] - OBFS["FUNC"])] = (
                    4 + SPECIAL_WORDS + i
                )
        counts = {k: 0 for k in word2id.keys()}
        f = open(vocab_path, "r", encoding="utf-8")
        for i, line_str in enumerate(f):
            if "\u2028" in line_str:
                skipped += 1
                continue
            line = line_str.rstrip().split()
            if len(line) != 2:
                skipped += 1
                continue
            assert len(line) == 2, (i, line)
            # assert line[0] not in word2id and line[1].isdigit(), (i, line)
            assert line[1].lstrip("-").isdigit(), (i, line)
            if line[0] in word2id:
                skipped += 1
                logger.info("%s already in vocab" % line[0])
                continue
            if not line[1].lstrip("-").isdigit():
                skipped += 1
                logger.info("Empty word at line %s with count %s" % (i, line))
                continue
            word2id[line[0]] = (
                NUM_SPECIAL_TOKENS + i - skipped
            )  # shift because of extra words
            counts[line[0]] = int(line[1])
        f.close()
        id2word = {v: k for k, v in word2id.items()}
        dico = cls(id2word, word2id, counts)
        logger.info("Read %i words from the vocabulary file." % len(dico))
        if skipped > 0:
            logger.warning("Skipped %i empty lines!" % skipped)
        return dico

    @staticmethod
    def index_data(path, bin_path, dico):
        """
        Index sentences with a dictionary.

        Parameters (to be confirmed)
        ----------
        path: input
        bin_path: output
        dico: Dictionary
        """
        if bin_path is not None and os.path.isfile(bin_path):
            logger.info("Loading data from %s ..." % bin_path)
            data = torch.load(bin_path)
            assert dico == data["dico"]
            return data

        positions = []
        sentences = []
        unk_words = {}

        # index sentences
        f = open(path, "r", encoding="utf-8")
        for i, line in enumerate(f):
            if i % 1000000 == 0 and i > 0:
                print(i)
            s = line.rstrip().split()
            # skip empty sentences
            if len(s) == 0:
                print("Empty sentence in line %i." % i)
            # index sentence words
            count_unk = 0
            indexed = []
            for w in s:
                word_id = dico.index(w, no_unk=False)
                # if we find a special word which is not an unknown word, skip the sentence
                if 0 <= word_id < 4 + SPECIAL_WORDS and word_id != 3:
                    logger.warning(
                        'Found unexpected special word "%s" (%i)!!' % (w, word_id)
                    )
                    continue
                assert word_id >= 0
                indexed.append(word_id)
                if word_id == dico.unk_index:
                    unk_words[w] = unk_words.get(w, 0) + 1
                    count_unk += 1
            # add sentence
            positions.append([len(sentences), len(sentences) + len(indexed)])
            sentences.extend(indexed)
            sentences.append(1)  # EOS index
        f.close()

        # tensorize data
        positions = np.int64(positions)
        if len(dico) < 1 << 16:
            sentences = np.uint16(sentences)
        elif len(dico) < 1 << 31:
            sentences = np.int32(sentences)
        else:
            raise Exception("Dictionary is too big.")
        assert sentences.min() >= 0
        data = {
            "dico": dico,
            "positions": positions,
            "sentences": sentences,
            "unk_words": unk_words,
        }
        if bin_path is not None:
            print("Saving the data to %s ..." % bin_path)
            torch.save(data, bin_path, pickle_protocol=4)

        return data
