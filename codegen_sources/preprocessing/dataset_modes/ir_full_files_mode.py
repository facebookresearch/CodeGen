# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
import typing as tp
from logging import getLogger
from pathlib import Path

import submitit

from codegen_sources.IR_tools.utils_ir import code_to_ir, ir_had_errors
from codegen_sources.preprocessing.dataset_modes.dataset_mode import (
    DATASET_SPLITS,
    DatasetMode,
)
from codegen_sources.preprocessing.dataset_modes.ir_functions_mode import (
    IRFunctionsMode,
)
from codegen_sources.preprocessing.lang_processors import LangProcessor, IRProcessor
from codegen_sources.preprocessing.obfuscation.utils_deobfuscation import REPLACE_DICT
from codegen_sources.preprocessing.timeout import timeout
from codegen_sources.preprocessing.utils import (
    check_same_number_of_lines,
    create_symlink,
    get_all_pairs,
    get_subset_file,
    is_valid_file,
)
from submitit import Executor, LocalExecutor

IR_SUFFIXES = ["sa", "ir_sa"]
logger = getLogger()


class IRFullFilesMode(IRFunctionsMode):
    """
    Callable where we track the repos processed so that we can checkpoint with submitit
    """  # TODO currently not callable nor checkpointable

    def __init__(
        self,
        folder,
        languages,
        bpe,
        processed_lines: tp.Optional[tp.Set] = None,
        nb_train_split: int = 8,
        keep_comments: bool = False,
        repo_split: bool = True,
    ):
        super().__init__(
            folder=folder,
            languages=languages,
            bpe=bpe,
            processed_lines=processed_lines,
            nb_train_split=nb_train_split,
            keep_comments=keep_comments,
            repo_split=repo_split,
        )
        self.id_is_line = False

    # TODO reactivate when callable
    # def checkpoint(
    #     self, input_path: str, process_strings: bool
    # ) -> submitit.helpers.DelayedSubmission:
    #     return submitit.helpers.DelayedSubmission(
    #         self.__class__(
    #             self.folder, self.languages, self.bpe, self.processed_lines,
    #         ),
    #         input_path,
    #         process_strings,
    #     )

    def extract_data_for_line(
        self,
        line_id: str,
        json_line: dict,
        process_strings: bool,
        lang_processor: LangProcessor,
    ):
        ir_processor = IRProcessor()
        default_return = line_id, None, None
        if "content" not in json_line:
            return default_return
        content = json_line["content"]
        try:
            tokenized_file = " ".join(
                lang_processor.tokenize_code(
                    content,
                    process_strings=process_strings,
                    keep_comments=self.keep_comments,
                )
            )
            irs = [
                code_to_ir(
                    content,
                    lang_processor.language,
                    func_level=False,
                    cannonize=False,
                    clean_dir=True,
                    verbose=False,
                )
            ]

            ir_errors = [
                len(ir) == 0 or (len(ir) > 0 and ir_had_errors(ir[0])) for ir in irs
            ]
            logger.info(f"error rate: {sum(ir_errors) / len(ir_errors):.3%}")
            if any(ir_errors):
                return default_return

            irs = [
                " ".join(ir_processor.tokenize_code(ir[0]))
                for ir, err in zip(irs, ir_errors)
                if not err
            ]
        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write(f"error {e} tokenizing and extracting functions\n")
            return default_return
        return (
            line_id,
            json_line["repo_name"],
            {"sa": [tokenized_file], "ir_sa": irs},
        )
