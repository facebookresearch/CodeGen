# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import re
import tokenize
import typing as tp
from io import BytesIO

import black  # type: ignore

from codegen_sources.preprocessing.obfuscation.bobskater_obfuscator import (
    obfuscateString,
)
from codegen_sources.preprocessing.obfuscation.utils_deobfuscation import dico_to_string
from .lang_processor import LangProcessor, NEWLINE_TOK
from .tokenization_utils import process_string


class PythonProcessor(LangProcessor):
    def __init__(self) -> None:
        self.spetoken2char = {
            "STOKEN00": "#",
            "STOKEN1": "\\n",
            "STOKEN2": '"""',
            "STOKEN3": "'''",
        }
        self.char2spetoken = {
            value: " " + key + " " for key, value in self.spetoken2char.items()
        }

    @property
    def language(self) -> str:
        return "py"  # TODO would "python" (default) be breaking stuff? this is unclear

    def tokenize_code(self, code, keep_comments=False, process_strings=True):
        assert isinstance(code, str)
        code = code.replace(r"\r", "")
        code = code.replace("\r", "")
        tokens = []

        try:
            iterator = tokenize.tokenize(BytesIO(code.encode("utf-8")).readline)
        except SyntaxError as excep:
            raise SyntaxError(excep)

        removed_docstr = 0
        while True:
            try:
                toktype, tok, _, _, line = next(iterator)
            except (
                tokenize.TokenError,
                IndentationError,
                SyntaxError,
                UnicodeDecodeError,
            ) as e:
                raise ValueError(
                    f'Impossible to parse tokens because of incorrect source code "{e}" ...'
                )
            except StopIteration:
                raise StopIteration(f"End of iterator before ENDMARKER token.")

            if toktype == tokenize.ENCODING or toktype == tokenize.NL:
                continue

            elif toktype == tokenize.NEWLINE:
                if removed_docstr == 1:
                    removed_docstr = 0
                    continue
                tokens.append(NEWLINE_TOK)

            elif toktype == tokenize.COMMENT:
                if keep_comments:
                    com = process_string(
                        tok,
                        self.char2spetoken,
                        self.spetoken2char,
                        True,
                        do_whole_processing=process_strings,
                    )
                    if len(com) > 0:
                        tokens.append(com)
                else:
                    continue

            elif toktype == tokenize.STRING:
                if tok == line.strip():  # docstring
                    if not keep_comments:
                        removed_docstr = 1
                        continue
                    else:
                        coms = process_string(
                            tok,
                            self.char2spetoken,
                            self.spetoken2char,
                            True,
                            do_whole_processing=process_strings,
                        )
                        if len(coms) > 0:
                            tokens.append(coms)
                        else:
                            removed_docstr = 1
                else:
                    tokens.append(
                        process_string(
                            tok,
                            self.char2spetoken,
                            self.spetoken2char,
                            False,
                            do_whole_processing=process_strings,
                        )
                    )

            elif toktype == tokenize.INDENT:
                tokens.append("INDENT")

            elif toktype == tokenize.DEDENT:
                # empty block
                if tokens[-1] == "INDENT":
                    tokens = tokens[:-1]
                else:
                    tokens.append("DEDENT")

            elif toktype == tokenize.ENDMARKER:
                tokens.append("ENDMARKER")
                break

            else:
                tokens.append(tok)

        assert tokens[-1] == "ENDMARKER", "Error, no end marker"
        return tokens[:-1]

    def detokenize_code(self, code):
        # replace recreate lines with \n and appropriate indent / dedent
        # removing indent/ dedent tokens
        assert isinstance(code, str) or isinstance(code, list)
        if isinstance(code, list):
            code = " ".join(code)
        code = code.replace("ENDCOM", NEWLINE_TOK)
        code = code.replace("▁", "SPACETOKEN")
        lines = code.split(NEWLINE_TOK)
        tabs = ""
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith("INDENT "):
                tabs += "    "
                line = line.replace("INDENT ", tabs)
            elif line.startswith("DEDENT"):
                number_dedent = line.count("DEDENT")
                tabs = tabs[4 * number_dedent :]
                line = line.replace("DEDENT", "")
                line = line.strip()
                line = tabs + line
            elif line == "DEDENT":
                line = ""
            else:
                line = tabs + line
            lines[i] = line
        untok_s = "\n".join(lines)
        # find string and comment with parser and detokenize string correctly
        try:
            for toktype, tok, _, _, line in tokenize.tokenize(
                BytesIO(untok_s.encode("utf-8")).readline
            ):
                if toktype == tokenize.STRING or toktype == tokenize.COMMENT:
                    tok_ = (
                        tok.replace("STRNEWLINE", "\n")
                        .replace("TABSYMBOL", "\t")
                        .replace(" ", "")
                        .replace("SPACETOKEN", " ")
                    )
                    untok_s = untok_s.replace(tok, tok_)
        except KeyboardInterrupt:
            raise
        except:
            # TODO raise ValueError(f'Invalid python function \n {code}\n')
            pass
        # detokenize imports
        untok_s = (
            untok_s.replace(". ", ".")
            .replace(" .", ".")
            .replace("import.", "import .")
            .replace("from.", "from .")
        )
        # special strings
        string_modifiers = ["r", "u", "f", "rf", "fr", "b", "rb", "br"]
        for modifier in string_modifiers + [s.upper() for s in string_modifiers]:
            untok_s = untok_s.replace(f" {modifier} '", f" {modifier}'").replace(
                f' {modifier} "', f' {modifier}"'
            )
        untok_s = untok_s.replace("> >", ">>").replace("< <", "<<")
        return untok_s

    def obfuscate_code(self, code):
        res, dico = obfuscateString(code, obfuscateNames=True, removeDocstrings=False)
        return res, dico_to_string(dico)

    def extract_functions(
        self, code: tp.Union[str, tp.List[str]], tokenized: bool = True,
    ) -> tp.Tuple[tp.List[str], tp.List[str]]:
        """Extract functions from tokenized python code"""
        if not tokenized:
            raise ValueError(
                "Function extraction not available for PythonProcessor and untokenized files. Please use PythonTreeSitterProcessor"
            )
        if isinstance(code, str):
            tokenized_code = code.split()
        else:
            tokenized_code = code
        assert isinstance(tokenized_code, list)

        tokens = iter(tokenized_code)
        functions_standalone = []
        functions_class = []
        number_indent = 0
        try:
            token = next(tokens)
        except StopIteration:
            return [], []
        while True:
            try:
                if token == "def":
                    function = ["def"]
                    while not (token == "DEDENT" and number_indent == 0):
                        token = next(tokens)
                        if token == "INDENT":
                            number_indent += 1
                        elif token == "DEDENT":
                            number_indent -= 1
                        function.append(token)
                    try:
                        str_function = " ".join(function)
                        if is_python_2(str_function):
                            token = next(tokens)
                            continue
                        if function[function.index("(") + 1] == "self":
                            functions_class.append(str_function)
                        else:
                            functions_standalone.append(str_function)
                    except KeyboardInterrupt:
                        raise
                    except:
                        print(function)
                        token = next(tokens)
                else:
                    token = next(tokens)
            except StopIteration:
                break
        return functions_standalone, functions_class

    def get_function_name(self, function):
        assert isinstance(function, str) or isinstance(function, list)
        if isinstance(function, str):
            function = function.split()
        return function[function.index("def") + 1]

    @staticmethod
    def format(code: str) -> str:
        """normalizes the input code by formatting it"""
        return apply_black(code)


def is_python_2(code: str) -> bool:
    if (
        re.search("print [^(]", code) is None
        and re.search("raise \w+ ,", code) is None
        and re.search("except \w+ ,", code) is None
        and re.search("[^ ]+ = \d+ L", code) is None
        and re.search(".[ ]*iterkeys[ ]*\([ ]*\)", code) is None
        and re.search(".[ ]*itervalues[ ]*\([ ]*\)", code) is None
        and re.search(".[ ]*iteritems[ ]*\([ ]*\)", code) is None
        and re.search("xrange[ ]*\(", code) is None
        and re.search("imap[ ]*\(", code) is None
    ):
        return False
    else:
        return True


def apply_black(code: str, line_length: int = 88):
    """Apply black to code"""
    try:
        mode = black.FileMode(line_length=line_length)
        return black.format_str(code, mode=mode)
    except KeyboardInterrupt:
        raise
    except Exception:
        return code
