# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from itertools import chain
from logging import getLogger

import submitit
from codegen_sources.preprocessing.bpe_modes.bpe_mode import TMP_EXT
from codegen_sources.preprocessing.dataset_modes.dataset_mode import (
    DATASET_SPLITS,
    DatasetMode,
)
from codegen_sources.preprocessing.lang_processors.lang_processor import LangProcessor
from codegen_sources.preprocessing.obfuscation.utils_deobfuscation import REPLACE_DICT
from codegen_sources.preprocessing.timeout import timeout
from submitit import Executor, LocalExecutor

OUTLIER_INDICES_THRESHOLDS = {"VAR_": 200, "FUNC_": 200, "CLASS_": 100}

OBFUSCATION_SUFFIXES = ["obfuscated", "dictionary"]
logger = getLogger()


class ObfuscationMode(DatasetMode):
    """
    Callable where we track the repos processed so that we can checkpoint with submitit
    """

    def __init__(
        self,
        folder,
        languages,
        bpe,
        processed_lines: set = None,
        nb_train_split: int = 8,
        keep_comments: bool = False,
    ):
        super().__init__(
            suffixes=OBFUSCATION_SUFFIXES,
            folder=folder,
            languages=languages,
            bpe=bpe,
            parallel_dataset=True,
            processed_lines=processed_lines,
            nb_train_split=nb_train_split,
            keep_comments=keep_comments,
        )

    def checkpoint(
        self, input_path: str, process_strings: bool
    ) -> submitit.helpers.DelayedSubmission:
        return submitit.helpers.DelayedSubmission(
            self.__class__(
                self.folder, self.languages, self.bpe, self.processed_lines,
            ),
            input_path,
            process_strings,
        )

    @timeout(60)
    def extract_data_for_line(
        self,
        line_id: int,
        json_line: dict,
        process_strings: bool,
        lang_processor: LangProcessor,
    ):
        default_return = line_id, None, None
        if "content" not in json_line:
            return default_return

        content = json_line["content"]
        for k, v in REPLACE_DICT.items():
            content = content.replace(k, v)
        try:
            obfuscated, dico = lang_processor.obfuscate_code(content)
            tokenized_obfuscated_file = " ".join(
                lang_processor.tokenize_code(
                    obfuscated,
                    process_strings=process_strings,
                    keep_comments=self.keep_comments,
                )
            )
        except NotImplementedError:
            logger.error(
                f"Obfuscate method is not implemented for {lang_processor.__class__.__name__}"
            )
            raise
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logger.warning(f"Error obfuscating content {e} \n")
            return default_return
        return (
            line_id,
            json_line["repo_name"],
            {"obfuscated": [tokenized_obfuscated_file], "dictionary": [dico]},
        )

    def filter(self, tokenized_data):
        assert all(s in tokenized_data for s in self.suffixes)
        assert len(tokenized_data["dictionary"]) == 1
        assert isinstance(tokenized_data["dictionary"][0], str)
        for var_prefix, var_number in OUTLIER_INDICES_THRESHOLDS.items():
            if f"{var_prefix}{var_number}" in tokenized_data["dictionary"][0]:
                return True
        return False

    def _learn_bpe(self, ncodes: int, executor: Executor = None):
        raise Exception(
            "BPE codes should not be learnt from obfuscated data. Learn them on monolingual data."
            "Please provide bpe codes or learn them."
            "To do so, please run pipepline with monolingual mode until BPE learning."
        )

    def apply_bpe(self, executor: Executor = None, local_parallelism: int = None):
        """
        Overwrite the method as in the obfuscation mode, need to restore the BPE.
        """
        if executor is None:
            executor = LocalExecutor(folder=self.folder.joinpath("log"))
        # apply BPE with tmp suffix
        _bpe_ext = self.bpe.ext
        self.bpe.ext += TMP_EXT
        super().apply_bpe(executor)
        self.bpe.ext = _bpe_ext
        # restore BPE on obfuscation special tokens
        jobs = []
        to_restore = list(
            chain(
                *[
                    self.folder.glob(f"{lang}.{split}.*{self.bpe.ext}{TMP_EXT}")
                    for split in DATASET_SPLITS
                    for lang in self.languages
                ]
            )
        )
        for f in to_restore:
            job = executor.submit(
                self.bpe.repair_bpe_for_obfuscation_file, f, f.with_suffix("")
            )
            jobs.append(job)
        for job in jobs:
            job.result()
        for f in to_restore:
            assert f.with_suffix("").is_file()
            f.unlink()

    def _get_vocab(self, executor: Executor = None):
        raise Exception(
            "Vocab should not be learnt from obfuscated data. Learn it on monolingual data."
            "Please provide vocab or learn them."
            "To do so, please run pipepline with monolingual mode until get_vocab."
        )
