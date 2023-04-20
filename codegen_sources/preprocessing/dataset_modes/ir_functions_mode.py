# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
import typing as tp
from logging import getLogger

from codegen_sources.IR_tools.utils_ir import code_to_ir, ir_had_errors
from codegen_sources.preprocessing.dataset_modes.dataset_mode import (
    DATASET_SPLITS,
    DatasetMode,
)
from codegen_sources.preprocessing.lang_processors import LangProcessor, IRProcessor
from codegen_sources.preprocessing.utils import (
    check_same_number_of_lines,
    create_symlink,
    get_all_pairs,
    is_valid_file,
)

IR_SUFFIXES = ["sa", "ir_sa"]
logger = getLogger()


class IRFunctionsMode(DatasetMode):
    """
    Callable where we track the repos processed so that we can checkpoint with submitit
    """

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
            suffixes=IR_SUFFIXES,
            folder=folder,
            languages=languages,
            bpe=bpe,
            parallel_dataset=True,
            processed_lines=processed_lines,
            nb_train_split=nb_train_split,
            keep_comments=keep_comments,
            repo_split=repo_split,
        )
        self.id_is_line = False

    # TODO update to make it work (currently buggy because non-callable)
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
            f_standalone, f_class = lang_processor.extract_functions(tokenized_file)
            funcs = f_standalone + f_class
            if len(f_standalone) == 0:
                return default_return

            irs = [
                code_to_ir(
                    lang_processor.detokenize_code(x),
                    lang_processor.language,
                    func_level=True,
                    cannonize=False,
                )
                for x in funcs
            ]
            ir_errors = [len(ir) > 0 and ir_had_errors(ir[0]) for ir in irs]
            logger.info(f"error rate: {sum(ir_errors) / len(ir_errors):.3%}")
            f_standalone = [f for f, err in zip(funcs, ir_errors) if not err]
            irs = [
                " ".join(ir_processor.tokenize_code(ir[0]))
                for ir, err in zip(irs, ir_errors)
                if not err
            ]
            assert len(f_standalone) == len(irs), (len(f_standalone), len(irs))
            if len(f_standalone) == 0:
                return default_return
        except KeyboardInterrupt:
            raise
        except Exception as e:
            sys.stderr.write(f"error {e} tokenizing and extracting functions\n")
            return default_return
        return (
            line_id,
            json_line["repo_name"],
            {"sa": f_standalone, "ir_sa": irs},
        )

    # def _learn_bpe(self, ncodes: int, executor: Executor = None):
    #     # get data to training data for bpe
    #     all_shufs = [
    #         self.folder.joinpath(f"{lang}.all.{suf}.tok.shuf")
    #         for lang in self.languages
    #         for suf in self.suffixes
    #     ]
    #     if any(not shuf.is_file() for shuf in all_shufs):
    #         self.regroup_all_tok()
    #         self.shuffle_all_tok()
    #     assert all(shuf.is_file() for shuf in all_shufs)
    #     data_train_bpe = get_subset_file(
    #         file_paths=all_shufs,
    #         subset_size_gb=50,
    #         output_path=self.folder.joinpath(
    #             f"{'-'.join(self.languages)}.{'-'.join(self.suffixes)}.tok.shuf.{50}gb"
    #         ),
    #     )
    #
    #     # train bpe codes
    #     logger.info(f"training bpe on {data_train_bpe}...")
    #     if executor is None:
    #         executor = LocalExecutor(self.folder.joinpath("log"))
    #     job = executor.submit(self.bpe.learn_bpe_file, data_train_bpe, ncodes)
    #     job.result()
    #     assert is_valid_file(self.bpe.codes)
    #     logger.info(f"Successfully learnt bpe. Bpe codes stored in {self.bpe.codes}.")
    #
    # def _get_vocab(self, executor: Executor = None):
    #     # get data to learn vocab
    #     data_get_vocab = [
    #         self.folder.joinpath(f"{lang}.train.{suf}.0.bpe")
    #         for lang in self.languages
    #         for suf in self.suffixes
    #     ]
    #     data_get_vocab = get_subset_file(
    #         data_get_vocab,
    #         20,
    #         output_path=self.folder.joinpath(
    #             f"{'-'.join(self.languages)}.train.{'-'.join(self.suffixes)}.0.20BG.bpe"
    #         ),
    #     )
    #     assert Path(
    #         data_get_vocab
    #     ).is_file(), f"cannot get vocab, {data_get_vocab} doesnt not exist."
    #
    #     # get vocab
    #     logger.info(f"Getting vocab from {data_get_vocab} ...")
    #     if executor is None:
    #         executor = LocalExecutor(folder=self.folder.joinpath("log"))
    #     job = executor.submit(self.bpe.get_vocab_file, data_get_vocab)
    #     job.result()
    #     assert self.bpe.vocab_path.is_file()
    #     logger.info(f"Successfully get vocab. Vocab stored in {self.bpe.vocab_path}.")

    def check_files_and_symlink_for_XLM(self):
        logger.info("")
        logger.info("")
        logger.info("========== Check and Create symlinks ===========")
        # check that all files exist and are not empty
        for lang in self.languages:
            for suffix in self.suffixes:
                for split in DATASET_SPLITS:
                    if split == "train":
                        for i in range(self.nb_train_split):
                            f = self.folder.joinpath(
                                f"{lang}.{split}.{suffix}.{i}{self.bpe.ext}.pth"
                            )
                            if not is_valid_file(f):
                                logger.warning(f"doest not exist {f}")
                    else:
                        f = self.folder.joinpath(
                            f"{lang}.{split}.{suffix}{self.bpe.ext}.pth"
                        )
                        if not is_valid_file(f):
                            logger.warning(f"doest not exist {f}")
        logger.info("create symlinks for XLM ...")
        XLM_folder = self.folder.joinpath("XLM-syml")
        XLM_folder.mkdir(exist_ok=True)
        for lang in self.languages:
            for split in DATASET_SPLITS:
                if self.parallel_dataset:
                    for suffix1, suffix2 in get_all_pairs(self.suffixes):
                        name_suff1, name_suff2 = [
                            suffix if "ir_" in suffix else f"{lang}_{suffix}"
                            for suffix in [suffix1, suffix2]
                        ]
                        if name_suff1 > name_suff2:
                            name_suff1, name_suff2 = name_suff2, name_suff1
                            suffix1, suffix2 = suffix2, suffix1
                        for suffix, name_suff in [
                            (suffix1, name_suff1),
                            (suffix2, name_suff2),
                        ]:
                            if split == "train":
                                for i in range(self.nb_train_split):
                                    # when parallel dataset, check files have same number of lines
                                    if suffix == suffix1:
                                        check_same_number_of_lines(
                                            self.folder.joinpath(
                                                f"{lang}.{split}.{suffix1}.{i}{self.bpe.ext}"
                                            ),
                                            self.folder.joinpath(
                                                f"{lang}.{split}.{suffix2}.{i}{self.bpe.ext}"
                                            ),
                                        )
                                    create_symlink(
                                        self.folder.joinpath(
                                            f"{lang}.{split}.{suffix}.{i}{self.bpe.ext}.pth"
                                        ),
                                        XLM_folder.joinpath(
                                            f"{split}.{name_suff1}-{name_suff2}.{name_suff}.{i}.pth"
                                        ),
                                    )
                            else:
                                if suffix == suffix1:
                                    check_same_number_of_lines(
                                        self.folder.joinpath(
                                            f"{lang}.{split}.{suffix1}{self.bpe.ext}"
                                        ),
                                        self.folder.joinpath(
                                            f"{lang}.{split}.{suffix2}{self.bpe.ext}"
                                        ),
                                    )
                                create_symlink(
                                    self.folder.joinpath(
                                        f"{lang}.{split}.{suffix}{self.bpe.ext}.pth"
                                    ),
                                    XLM_folder.joinpath(
                                        f"{split}.{name_suff1}-{name_suff2}.{name_suff}.pth"
                                    ),
                                )
        logger.info("Check and symlink done.")
