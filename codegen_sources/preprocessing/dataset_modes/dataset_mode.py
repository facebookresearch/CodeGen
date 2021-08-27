# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import fileinput
import json
from multiprocessing import Pool, cpu_count
import submitit
from typing import TypeVar, Generic, List
from pathlib import Path
import subprocess
import zlib
from itertools import chain, repeat
from hashlib import sha256
from submitit import Executor, LocalExecutor
from logging import getLogger

import sys

from codegen_sources.preprocessing import timeout

from codegen_sources.preprocessing.utils import (
    binarize_for_XLM_file,
    shuf_parallel_files,
    create_symlink,
    shuf_file,
    get_all_pairs,
    is_valid_file,
    check_same_number_of_lines,
)
import tqdm
from codegen_sources.preprocessing.bpe_modes.bpe_mode import BPEMode
from codegen_sources.preprocessing.obfuscation.utils_deobfuscation import SEPARATOR
from codegen_sources.preprocessing.lang_processors.cpp_processor import CppProcessor
from codegen_sources.preprocessing.lang_processors.java_processor import JavaProcessor
from codegen_sources.preprocessing.lang_processors.python_processor import (
    PythonProcessor,
)
from codegen_sources.preprocessing.lang_processors.lang_processor import LangProcessor
import time

TIMEOUT = "timeout"

T = TypeVar("T")
logger = getLogger()

DATASET_SPLITS = ["train", "valid", "test"]


def extract_language_name(path):
    return path.name.split(".")[0]


class DatasetMode(Generic[T]):
    def __init__(
        self,
        suffixes: List[T],
        folder: str,
        languages: List[str],
        bpe: BPEMode,
        parallel_dataset: bool,
        processed_lines: set = None,
        suffixes_for_postprocessing=(),
        nb_train_split=8,
    ):
        self.suffixes = suffixes
        self.suffixes_for_postprocessing = suffixes_for_postprocessing

        if processed_lines is None:
            self.processed_lines = set()
        else:
            self.processed_lines = processed_lines
        self.parallel_dataset = parallel_dataset

        self.folder = Path(folder)
        self.languages = languages
        self.languages.sort()
        self.initialize_processor()
        self.bpe = bpe
        self.nb_train_split = nb_train_split

    def initialize_processor(self):
        global lang_processors
        lang_processors = {
            lang: LangProcessor.processors[lang](
                root_folder=Path(__file__).parents[3].joinpath("tree-sitter")
            )
            for lang in self.languages
        }

    def checkpoint(
        self, input_path: str, process_strings: bool
    ) -> submitit.helpers.DelayedSubmission:
        return submitit.helpers.DelayedSubmission(
            self.__class__(
                self.suffixes,
                self.folder,
                self.languages,
                self.bpe,
                self.parallel_dataset,
                self.processed_lines,
                self.suffixes_for_postprocessing,
            ),
            input_path,
            process_strings,
        )

    def extract_data_and_tokenize(
        self, executor: Executor = None,
    ):
        """
        Takes the root folder of the dataset, containing json files as input
        For each json in it extract data, tokenize, and save in dedicated .tok file
        """
        logger.info("")
        logger.info("")
        logger.info("========== Extract and Tokenize ===========")
        if executor is None:
            executor = LocalExecutor(folder=self.folder.joinpath("log"))
        jobs = []

        assert any(
            len(list(self.folder.glob(f"{lang}.*.json.gz"))) > 0
            for lang in self.languages
        ), f"there is no json in {str(self.folder)}"
        json_files = [
            (json_file, language)
            for language in self.languages
            for json_file in self.folder.glob(f"{language}.*.json.gz")
            if extract_language_name(json_file) == language
            and not all(
                [
                    is_valid_file(Path(name))
                    for name in self.get_tok_files_for_json(json_file).values()
                ]
            )
        ]
        file_langs = [f[1] for f in json_files]
        files = [f[0] for f in json_files]
        logger.info(
            f"{' '.join(self.languages)}: tokenizing and extracting parallel functions in {len(json_files)} json files ..."
        )
        if len(json_files) > 0:
            jobs += executor.map_array(
                self.extract_from_json_and_tokenize,
                files,
                file_langs,
                repeat(self.bpe.process_strings),
            )
        else:
            return logger.info("Data extraction and tokenization already done.")

        for job in jobs:
            job.result()

    def extract_from_json_and_tokenize(
        self, input_path: str, lang: str, process_strings: bool
    ):
        """
        Takes one json file as input. For each document, it extracts data and tokenizes it.
        The results is written into a .tok file.
        """
        # {suffix: open(output)}
        tok_files = self.get_tok_files_for_json(input_path)
        tok_files = self.open_tok_files(tok_files)

        lines = []
        for i, line in enumerate(
            fileinput.input(str(input_path), openhook=fileinput.hook_compressed)
        ):
            try:
                lines.append(
                    (f"{input_path}:{i}", json.loads(line), lang, process_strings)
                )
            except KeyboardInterrupt:
                raise
            except:
                pass

        number_errors = 0
        number_timeouts = 0
        multilines_code = 0
        number_lines = len(lines)
        logger.info(f"Number of lines to process: {number_lines}")
        filtered_examples = 0
        try:
            start = time.time()
            executor = Pool(
                processes=cpu_count(), initializer=self.initialize_processor
            )
            results_for_line = tqdm.tqdm(
                executor.map(self.checkpoint_line, lines), total=len(lines)
            )

            for line_id, repo, tokenized_data in results_for_line:
                self.processed_lines.add(line_id)
                # returning None means there was an issue
                if tokenized_data == TIMEOUT:
                    number_timeouts += 1
                    continue
                if (
                    tokenized_data is None
                    or all(v is None for v in tokenized_data.values())
                    or len(tokenized_data) == 0
                    or repo is None
                ):
                    number_errors += 1
                    continue
                if self.parallel_dataset:
                    if any(v is None for v in tokenized_data.values()):
                        number_errors += 1
                        continue
                    expected_length = len(next(iter(tokenized_data.values())))
                    if not all(
                        expected_length == len(v) for v in tokenized_data.values()
                    ):
                        number_errors += 1
                        continue
                if self.filter(tokenized_data):
                    filtered_examples += 1
                    continue
                for suffix, tok_codes in tokenized_data.items():
                    if tok_codes is None:
                        assert not self.parallel_dataset
                        number_errors += 1
                        continue
                    for tok_code in tok_codes:
                        if not len(tok_code.splitlines()) <= 1:
                            multilines_code += 1
                        try:
                            tok_files[suffix].write(repo + SEPARATOR + tok_code)
                            tok_files[suffix].write("\n")
                        except KeyboardInterrupt:
                            raise
                        except Exception:
                            sys.stderr.write(f"Exception writing data: {tok_code}\n")
                            number_errors += 1
                            continue
                for suffix, _ in tokenized_data.items():
                    tok_files[suffix].flush()
            end = time.time()
            logger.info(f"Time elapsed: {round((end - start),2)}")
            if number_errors > 0:
                logger.warning(
                    f"Tokenization of {input_path}:"
                    f"{number_errors} errors out of {number_lines} lines"
                    f"({number_errors / number_lines:.2%})"
                )
            if number_timeouts > 0:
                logger.warning(
                    f"Tokenization of {input_path}:"
                    f"{number_timeouts} timeouts out of {number_lines} lines"
                    f"({number_errors / number_lines:.2%})"
                )

            if filtered_examples > 0:
                logger.warning(
                    f"Tokenization of {input_path}:"
                    f"{filtered_examples} filtered examples in {number_lines} lines"
                    f"({filtered_examples / number_lines:.2%})"
                )
            if multilines_code > 0:
                logger.warning(
                    f"Tokenization of {input_path}:"
                    f"{multilines_code} multiline codes {number_lines} lines"
                    f"({multilines_code / number_lines:.2%})"
                )
        except TimeoutError:
            # The tokenization process is sometimes killed and it makes the multiprocessing hang forever
            for f in tok_files.values():
                f.close()
            logger.warning("Program closed automatically after one hour")
            exit(1)

    def checkpoint_line(self, line):
        line_id, json_line, lang, process_strings = line

        default_return = line_id, None, None
        if line_id in self.processed_lines:
            # this was checkpointed, skip it
            return default_return
        global lang_processors
        try:
            return self.extract_data_for_line(
                line_id, json_line, process_strings, lang_processors[lang]
            )
        except timeout.TimeoutError:
            logger.info("Timeout error extracting data")
            return line_id, None, TIMEOUT

    def open_tok_files(self, files: dict):
        return {
            suffix: open(
                file,
                "a" if self.processed_lines else "w",
                encoding="utf-8",
                errors="ignore",
            )
            for suffix, file in files.items()
        }

    def get_tok_files_for_json(self, json_path):
        return {
            suffix: str(json_path).replace(".json.gz", f".{suffix}.tok")
            for suffix in self.suffixes
        }

    @timeout.timeout(60)
    def extract_data_for_line(
        self,
        line_id: int,
        json_line: dict,
        process_strings: bool,
        lang_processor: LangProcessor,
    ):
        """
        Is designed to be called by the extract_from_file method.
        It should return the repo name,
        and lists of source and target codes (if parallel dataset)
        """
        raise NotImplementedError(
            "The abstract method extract_data_for_line should be overridden"
        )

    def filter(self, tokenized_data: dict):
        return False

    def regroup_all_tok(self):
        """
        Regroup all .tok into a single file.
        This regrouping is a concatenation of the .tok files.
        Therefore order is preserved and works for parallel datasets as well.
        """
        for lang in self.languages:
            for suffix in self.suffixes:
                all_tok_path = self.folder.joinpath(f"{lang}.all.{suffix}.tok")
                if is_valid_file(all_tok_path):
                    continue
                if len(list(self.folder.glob(f"{lang}.*[0-9].{suffix}.tok"))) == 0:
                    continue
                command = (
                    f"cd {self.folder}; cat {lang}.*[0-9].{suffix}.tok > {all_tok_path}"
                )
                proc = subprocess.run(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    executable="/bin/bash",
                )
                logger.info(
                    f"all files {lang}.*[0-9].{suffix}.tok regrouped in {all_tok_path} ."
                )
                # TODO check number of lines
                assert proc.returncode == 0, proc.stderr
                assert is_valid_file(all_tok_path)

    def shuffle_all_tok(self):
        """
        Shuffle all.tok. If dataset is parallel, shuflle them parallely
        """
        for lang in self.languages:
            filenames = [f"{lang}.all.{suf}.tok" for suf in self.suffixes]
            # check inputs
            assert all([is_valid_file(self.folder.joinpath(p)) for p in filenames]), (
                "files not found: "
                + ",".join(
                    [p for p in filenames if not is_valid_file(self.folder.joinpath(p))]
                )
            )
            # check outputs doesnt exist
            if all(
                [is_valid_file(self.folder.joinpath(f"{p}.shuf")) for p in filenames]
            ):
                return
            # shuffle
            if not self.parallel_dataset:
                logger.info(
                    f"shuffling {len(filenames)} files individualy: {', '.join(filenames)}"
                )
                for fname in filenames:
                    shuf_file(self.folder.joinpath(fname))
            else:
                logger.info(
                    f"shuffling {len(filenames)} files parallely: {', '.join(filenames)}"
                )
                shuf_parallel_files(
                    [self.folder.joinpath(fname) for fname in filenames]
                )

    def split_train_test_valid(
        self, percent_test=1, percent_valid=1, dedupe: bool = True
    ):
        """
        Take the tokenized data, that has been regroupe into .tok,
        and split them into a training, test and validation tests
        Do it in parallel for parallel datasets.
        """
        for lang in self.languages:
            if dedupe is False:
                suffix_to_dedup = []
                logger.info(
                    f"{lang}: No deduplication will be run. Dedup is set to False."
                )
            elif self.parallel_dataset:
                suffix_to_dedup = self.suffixes[0]
                logger.info(
                    f"{lang}: Deduplication on '{self.suffixes[0]}' and propagated on other suffixes."
                )
                ids_to_remove = set()
            else:
                suffix_to_dedup = self.suffixes
                logger.info(f"{lang}: Deduplication on {self.suffixes}.")

            # start with obfuscated to dedupe based on the content of the file
            seen_contents = set()
            for suffix in self.suffixes:
                if not self.parallel_dataset:
                    seen_contents = set()
                    ids_to_remove = set()
                all_tok_path = self.folder.joinpath(f"{lang}.all.{suffix}.tok.shuf")
                assert is_valid_file(all_tok_path)
                output_paths = {
                    split: self.folder.joinpath(f"{lang}.{split}.tok")
                    for split in ([f"valid.{suffix}"] if percent_valid > 0 else [])
                    + ([f"test.{suffix}"] if percent_test > 0 else [])
                    + (
                        [f"train.{suffix}.{n}" for n in range(self.nb_train_split)]
                        if percent_test + percent_valid < 100
                        else []
                    )
                }
                if all([is_valid_file(path) for path in output_paths.values()]):
                    return
                output_nlines = {k: 0 for k in output_paths.keys()}
                outputs = {
                    split: open(p, "w", encoding="utf-8", errors="ignore")
                    for split, p in output_paths.items()
                }
                with open(
                    all_tok_path, "r", encoding="utf-8", errors="ignore"
                ) as all_splits_file:
                    # Deduplication
                    for line_id, line in enumerate(all_splits_file):
                        if "|" not in line or "/" not in line.split("|", 1)[0]:
                            continue
                        repo, content = line.split("|", 1)
                        if suffix in suffix_to_dedup:
                            content_hash = sha256(content.encode("utf-8")).hexdigest()
                            if content_hash in seen_contents:
                                ids_to_remove.add(line_id)
                                continue
                            seen_contents.add(content_hash)
                        elif line_id in ids_to_remove:
                            # line for reference suffix is a duplicate. Dedupe
                            continue
                        # select the repo name without the username of the repo creator
                        assert (
                            "/" in repo
                        ), f"Repository {repo} should contain a / character"
                        repo = repo.split("/", 1)[1]
                        hash_repo = zlib.adler32(repo.encode("utf-8")) % 100
                        output_split = (
                            "test"
                            if (hash_repo < percent_test)
                            else (
                                "train"
                                if hash_repo >= (percent_test + percent_valid)
                                else "valid"
                            )
                        )
                        output_split += f".{suffix}"
                        if output_split.startswith("train"):
                            output_split += f".{line_id % self.nb_train_split}"
                        outputs[output_split].write(content)
                        output_nlines[output_split] += 1
                    logger.info(
                        f"{lang}: Duplicated lines for {suffix}: {len(ids_to_remove)} / {line_id + 1}"
                    )
                for o in outputs.values():
                    o.close()
                for k, v in output_nlines.items():
                    logger.info(f"{lang}: {k} -> {v} lines")

    def get_train_test_valid_splits(
        self, percent_test=1, percent_valid=1, dedupe: bool = True
    ):
        """
        Take all tokenized file and regroup them into train/test/validation sets.
        """
        logger.info("")
        logger.info("")
        logger.info("========== Deduplicate and Split ===========")
        # regroup all tokenized files
        self.regroup_all_tok()
        # shuffle
        self.shuffle_all_tok()
        # split into a train, test and valid sets
        self.split_train_test_valid(
            percent_test=percent_test, percent_valid=percent_valid, dedupe=dedupe
        )
        logger.info(
            "Sucessfully regroup, deduplicate and split tokenized data into a train/valid/test sets."
        )

    def learn_bpe(self, ncodes: int, executor: Executor = None):
        logger.info("")
        logger.info("")
        logger.info("========== Learn BPE ===========")
        if getattr(self.bpe, "codes", False) is False:
            logger.info(
                f"No need to train bpe codes for {self.bpe.__class__.__name__}."
            )
            return
        elif is_valid_file(self.bpe.codes):
            logger.info(
                f"No need to train bpe codes, already trained. Codes: {self.bpe.codes}"
            )
            return
        self.bpe.codes = self.folder.joinpath(
            f"{'-'.join(self.languages)}.{'-'.join(self.suffixes)}.codes"
        )
        if is_valid_file(self.bpe.codes):
            logger.info(
                f"BPE codes already trained for this dataset. Codes: {self.bpe.codes}"
            )
            return
        self._learn_bpe(ncodes, executor)

    def _learn_bpe(self, ncodes: int, executor: Executor = None):
        raise NotImplementedError("Learn bpe method need to be implemented.")

    def apply_bpe(self, executor: Executor = None):
        logger.info("")
        logger.info("")
        logger.info("========== Apply BPE ===========")
        if executor is None:
            executor = LocalExecutor(folder=self.folder.joinpath("log"))
        jobs = []
        for f in chain(
            *[
                self.folder.glob(f"{lang}.{split}.{suffix}.*tok")
                for split in DATASET_SPLITS
                for suffix in self.suffixes
                for lang in self.languages
            ]
        ):
            if not is_valid_file(f):
                logger.warning(f"{f} is not a valid file, cannot to apply BPE on it.")
            elif not is_valid_file(f.with_suffix(self.bpe.ext)):
                logger.info(f"Applying BPE on {f} ...")
                job = executor.submit(
                    self.bpe.apply_bpe_file, f, f.with_suffix(self.bpe.ext)
                )
                jobs.append(job)
        for job in jobs:
            job.result()
        logger.info("BPE done.")

    def get_vocab(self, executor: Executor = None):
        logger.info("")
        logger.info("")
        logger.info("========== Get VOCAB ===========")
        if is_valid_file(self.bpe.vocab_path):
            logger.info(
                f"No need to get vocab, already exists. Vocab: {self.bpe.vocab_path}"
            )
            return
        self.bpe.vocab_path = self.folder.joinpath(
            f"{'-'.join(self.languages)}.{'-'.join(self.suffixes)}.vocab"
        )
        if is_valid_file(self.bpe.vocab_path):
            logger.info(
                f"BPE vocab already trained for this dataset. Vocab: {self.bpe.vocab_path}"
            )
            return
        self._get_vocab(executor)

    def _get_vocab(self, executor: Executor = None):
        raise NotImplementedError("Get vocab method needs to be implemented.")

    def binarize(self, executor: Executor = None):
        logger.info("")
        logger.info("")
        logger.info("========== Binarize ===========")
        if executor is None:
            executor = LocalExecutor(folder=self.folder.joinpath("log"))
        jobs = []
        for f in chain(
            *[
                self.folder.glob(f"{lang}.{split}.{suffix}*{self.bpe.ext}")
                for split in DATASET_SPLITS
                for suffix in self.suffixes
                for lang in self.languages
            ]
        ):
            if not is_valid_file(f.with_suffix(f.suffix + ".pth")):
                logger.info(f"binarizing {f} ...")
                jobs.append(
                    executor.submit(binarize_for_XLM_file, f, self.bpe.vocab_path)
                )
        for job in jobs:
            job.result()
        logger.info("Binarize done.")

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
                        suffix1, suffix2 = sorted([suffix1, suffix2])
                        for suffix in [suffix1, suffix2]:
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
                                            f"{split}.{lang}_{suffix1}-{lang}_{suffix2}.{lang}_{suffix}.{i}.pth"
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
                                        f"{split}.{lang}_{suffix1}-{lang}_{suffix2}.{lang}_{suffix}.pth"
                                    ),
                                )
                else:
                    for suffix in self.suffixes:
                        if split == "train":
                            for i in range(self.nb_train_split):
                                create_symlink(
                                    self.folder.joinpath(
                                        f"{lang}.{split}.{suffix}.{i}{self.bpe.ext}.pth"
                                    ),
                                    XLM_folder.joinpath(
                                        f"{split}.{lang}_{suffix}.{i}.pth"
                                    ),
                                )
                        else:
                            create_symlink(
                                self.folder.joinpath(
                                    f"{lang}.{split}.{suffix}{self.bpe.ext}.pth"
                                ),
                                XLM_folder.joinpath(f"{split}.{lang}_{suffix}.pth"),
                            )
        logger.info("Check and symlink done.")
