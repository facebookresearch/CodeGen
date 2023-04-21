# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from abc import ABC
import typing as tp


NEWLINE_TOK = "NEW_LINE"  # different name to avoid confusions by the tokenizer


class LangProcessor(ABC):
    processors: tp.Dict[str, tp.Type["LangProcessor"]] = {}

    @classmethod
    def _language(cls) -> str:
        # note: properties only work on instances, not on the class
        # (unless we reimplement the decorator), so it's simpler to have
        # a method on the class for when we need it, and the property on
        # the instance for a simpler API
        parts = cls.__name__.split("Processor")
        if len(parts) != 2 or parts[1]:
            raise RuntimeError(
                "language processors class name should be that format: "
                f"YourlanguageProcessor (got: {cls.__name__})"
            )
        return parts[0].lower()

    @property
    def language(self) -> str:
        """Language of the processor"""
        return self._language()

    @classmethod
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.processors[cls._language()] = cls

    def tokenize_code(
        self, code: str, keep_comments: bool = False, process_strings: bool = True
    ) -> tp.List[str]:
        raise NotImplementedError

    def detokenize_code(self, code: tp.Union[tp.List[str], str]) -> str:
        raise NotImplementedError

    def obfuscate_code(self, code):
        raise NotImplementedError

    def obfuscate_types(self, code: str) -> tp.Tuple[str, str]:
        raise NotImplementedError

    def extract_functions(
        self, code: tp.Union[str, tp.List[str]], tokenized: bool = True,
    ) -> tp.Tuple[tp.List[str], tp.List[str]]:
        raise NotImplementedError

    def get_function_name(self, function: str) -> str:
        raise NotImplementedError

    def extract_arguments(self, function):
        raise NotImplementedError

    @staticmethod
    def format(code: str) -> str:
        raise NotImplementedError
