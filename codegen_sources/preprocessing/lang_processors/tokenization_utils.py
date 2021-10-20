# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import re
from sacrebleu import tokenize_v14_international

# IMPORTED
NEWLINE_TOKEN = "NEWLINE_TOKEN"


# IMPORTED
class ind_iter(object):
    def __init__(self, len):
        self.i = 0
        self.len = len

    def next(self):
        self.i += 1
        if self.i > (self.len - 1):
            raise StopIteration

    def prev(self):
        self.i -= 1
        if self.i < 0:
            raise StopIteration


# IMPORTED
def process_string(tok, char2tok, tok2char, is_comment, do_whole_processing=True):
    if not (do_whole_processing or is_comment):
        return tok.replace("\n", "\\n").replace("\r", "")

    if is_comment:
        tok = re.sub(" +", " ", tok)
        tok = re.sub(r"(.)\1\1\1\1+", r"\1\1\1\1\1", tok)
        if len(re.sub(r"\W", "", tok)) < 2:
            return ""
    tok = replace_general_string_tok(tok)
    tok = replace_tokens(tok, char2tok)
    if tok.strip().startswith("STOKEN00"):
        if " STRNEWLINE " in tok:
            tok = tok.replace(" STRNEWLINE ", " ENDCOM", 1)
        else:
            tok += " ENDCOM"
    if not do_whole_processing:
        tok = replace_tokens(
            tok, {f" {key} ": value for key, value in tok2char.items()}
        )
        tok = (
            tok.replace(" ▁ ", " ")
            .replace(" TABSYMBOL ", "\t")
            .replace("\\r", "")
            .replace(" STRNEWLINE ", "\\n")
        )
        return tok

    tok = re.sub(" +", " ", tok)
    tok = tokenize_v14_international(tok)
    tok = re.sub(" +", " ", tok)
    tok = tok.replace("\r", "")
    for special_token, char in tok2char.items():
        tok = tok.replace(special_token, char)
    if tok[0].isalpha():
        # for special strings, (e.g. L "s" we should remove the space after L)
        tok = tok.replace(f"{tok[0]} ", tok[0])
    return tok


def tokenize_string(s: str):
    return process_string(
        s, char2tok=dict(), tok2char=dict(), is_comment=False, do_whole_processing=True
    ).split(" ")


def detokenize_string(s):
    assert isinstance(s, str) or isinstance(s, list)
    if isinstance(s, list):
        s = " ".join(s)
    return s.replace(" ", "").replace("▁", " ")


# IMPORTED
def replace_tokens(tok, dictionary):
    for char, special_token in dictionary.items():
        tok = tok.replace(char, special_token)
    return tok


# IMPORTED
def replace_general_string_tok(tok):
    return (
        tok.replace(" ", " ▁ ")
        .replace("\n", " STRNEWLINE ")
        .replace("\t", " TABSYMBOL ")
    )


# IMPORTED
def indent_lines(lines):
    prefix = ""
    for i, line in enumerate(lines):
        line = line.strip()
        if re.match("CB_COLON|CB_COMA|CB_", line):
            prefix = prefix[2:]
            line = prefix + line
        elif line.endswith("OB_"):
            line = prefix + line
            prefix += "  "
        else:
            line = prefix + line
        lines[i] = line
    untok_s = "\n".join(lines)
    return untok_s
