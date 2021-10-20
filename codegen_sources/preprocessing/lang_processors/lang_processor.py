# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from abc import ABC


class LangProcessor(ABC):
    processors = {}

    def __init__(self, language):
        self.language = language

    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()
        assert (
            len(cls.__name__.lower().split("processor")) == 2
            and cls.__name__.lower().split("processor")[1] == ""
        ), "language processors class name should be that format : YourlanguageProcessor"
        cls.processors[cls.__name__.lower().split("processor")[0]] = cls

    def tokenize_code(self, code, keep_comments=False, process_strings=True):
        raise NotImplementedError

    def detokenize_code(self, code):
        raise NotImplementedError

    def obfuscate_code(self, code):
        raise NotImplementedError

    def extract_functions(self, code):
        raise NotImplementedError

    def get_function_name(self, function):
        raise NotImplementedError

    def extract_arguments(self, function):
        raise NotImplementedError
