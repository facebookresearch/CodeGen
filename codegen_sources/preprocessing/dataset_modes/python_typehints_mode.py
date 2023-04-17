# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import ast
import logging
import itertools

import submitit
import codegen_sources.utils.typing as tp
from codegen_sources.preprocessing.bpe_modes.bpe_mode import TMP_EXT
from codegen_sources.preprocessing.dataset_modes.dataset_mode import (
    DATASET_SPLITS,
    DatasetMode,
)
from codegen_sources.preprocessing.lang_processors import (
    LangProcessor,
    PythonTreeSitterProcessor,
)
from codegen_sources.preprocessing.obfuscation.utils_deobfuscation import REPLACE_DICT
from codegen_sources.preprocessing.timeout import timeout

OUTLIER_INDICES_THRESHOLDS = {"VAR_": 200, "FUNC_": 200, "CLASS_": 100}

TYPEHINTS_SUFFIXES = ["hidden", "dictionary"]
logger = logging.getLogger(__name__)


class PythonTypeHintsMode(DatasetMode):
    """
    Callable where we track the repos processed so that we can checkpoint with submitit
    """

    # nearly copy-pasted from obfuscator_mode, except for the obfuscation function

    def __init__(
        self,
        folder: tp.PathLike,
        languages: tp.List[str],
        bpe,
        processed_lines: tp.Optional[tp.Set[str]] = None,
        nb_train_split: int = 8,
        keep_comments: bool = True,
        repo_split: bool = True,
    ):
        assert languages == ["python"]
        super().__init__(
            suffixes=TYPEHINTS_SUFFIXES,
            folder=folder,
            languages=["python"],
            bpe=bpe,
            parallel_dataset=True,
            processed_lines=processed_lines,
            nb_train_split=nb_train_split,
            keep_comments=keep_comments,
            repo_split=repo_split,
        )

    def extract_data_for_line(
        self,
        line_id: str,
        json_line: tp.Dict[str, str],
        process_strings: bool,
        lang_processor: LangProcessor,
    ):
        # highjack because there are 2 python processors
        lang_processor = PythonTreeSitterProcessor()
        assert isinstance(
            lang_processor, PythonTreeSitterProcessor
        ), f"Got {lang_processor}"
        default_return = line_id, None, None
        if "content" not in json_line:
            return default_return

        content = json_line["content"]
        try:
            ast.parse(content)
        except Exception as e:
            logger.warning("Syntax error in the content: %s", e)
            return default_return
        for k, v in REPLACE_DICT.items():
            content = content.replace(k, v)
        try:
            obfuscated, dico = lang_processor.obfuscate_types(content)
            tokenized_obfuscated_file = " ".join(
                lang_processor.tokenize_code(
                    obfuscated,
                    process_strings=process_strings,
                    keep_comments=self.keep_comments,
                )
            )
        except NotImplementedError:
            logger.error(
                "obfuscate_types method is not implemented for %s",
                lang_processor.__class__.__name__,
            )
            raise
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:  # pylint: disable=broad-except
            logger.warning("Error hiding types in content %s\n", e)
            return default_return
        if not dico:  # not interesting data
            return default_return
        return (
            line_id,
            json_line["repo_name"],
            {"hidden": [tokenized_obfuscated_file], "dictionary": [dico]},
        )

    def post_tok_filter(self, tokenized_data: tp.Dict[str, tp.List[str]]) -> bool:
        assert all(s in tokenized_data for s in self.suffixes)
        assert len(tokenized_data["dictionary"]) == 1
        assert isinstance(tokenized_data["dictionary"][0], str)
        return False

    def _learn_bpe(
        self, ncodes: int, executor: tp.Optional[tp.ExecutorLike] = None
    ) -> None:
        raise Exception(
            "BPE codes should not be learnt from type inference data. Learn them on monolingual data."
            "Please provide bpe codes or learn them."
            "To do so, please run pipepline with monolingual mode until BPE learning."
        )

    def apply_bpe(
        self,
        executor: tp.Optional[tp.ExecutorLike] = None,
        local_parallelism: tp.Optional[int] = None,
    ) -> None:
        """
        Overwrite the method as in the obfuscation mode, need to restore the BPE.
        """
        if executor is None:
            executor = submitit.LocalExecutor(folder=self.folder / "log")
        # apply BPE with tmp suffix
        _bpe_ext = self.bpe.ext
        self.bpe.ext += TMP_EXT
        super().apply_bpe(executor)
        self.bpe.ext = _bpe_ext
        # restore BPE on hidden types special tokens
        jobs = []
        to_restore = list(
            itertools.chain(
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

    def _get_vocab(self, executor: tp.Optional[tp.ExecutorLike] = None) -> None:
        raise Exception(
            "Vocab should not be learnt from hidden type hints data. Learn it on "
            "monolingual data."
            "Please provide vocab or learn them."
            "To do so, please run pipepline with monolingual mode until get_vocab."
        )
