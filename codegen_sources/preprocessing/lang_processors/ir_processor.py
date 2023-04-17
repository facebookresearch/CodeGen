# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import re

from .lang_processor import LangProcessor, NEWLINE_TOK

IR_LANGUAGE_NAME = "ir"


class IRProcessor(LangProcessor):
    def tokenize_code(
        self, code: str, keep_comments: bool = False, process_strings: bool = True
    ):
        code = code.replace("\n", f" NEW_LINE ").replace("\r", "")
        return re.sub(r"\s+", " ", code).split(" ")

    def detokenize_code(self, code):
        return code.replace(f" NEW_LINE ", "\n").replace(NEWLINE_TOK, "\n")
