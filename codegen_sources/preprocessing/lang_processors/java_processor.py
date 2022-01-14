# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from codegen_sources.preprocessing.lang_processors.tree_sitter_processor import (
    TreeSitterLangProcessor,
    NEW_LINE,
)
from codegen_sources.preprocessing.obfuscation.utils_deobfuscation import dico_to_string
from codegen_sources.preprocessing.obfuscation import javalang_obfuscator

from codegen_sources.preprocessing.lang_processors.tokenization_utils import (
    ind_iter,
    NEWLINE_TOKEN,
)
import re

JAVA_TOKEN2CHAR = {
    "STOKEN00": "//",
    "STOKEN01": "/*",
    "STOKEN02": "*/",
    "STOKEN03": "/**",
    "STOKEN04": "**/",
    "STOKEN05": '"""',
    "STOKEN06": "\\n",
    "STOKEN07": "\\r",
    "STOKEN08": ";",
    "STOKEN09": "{",
    "STOKEN10": "}",
    "STOKEN11": r"\'",
    "STOKEN12": r"\"",
    "STOKEN13": r"\\",
}
JAVA_CHAR2TOKEN = {value: " " + key + " " for key, value in JAVA_TOKEN2CHAR.items()}


class JavaProcessor(TreeSitterLangProcessor):
    def __init__(self, root_folder):
        super().__init__(
            language="java",
            ast_nodes_type_string=[
                "comment",
                "block_comment",
                "line_comment",
                "string_literal",
                "character_literal",
            ],
            stokens_to_chars=JAVA_TOKEN2CHAR,
            chars_to_stokens=JAVA_CHAR2TOKEN,
            root_folder=root_folder,
        )

    def obfuscate_code(self, code):
        res, dico = javalang_obfuscator.obfuscate(code)
        return res, dico_to_string(dico)

    def extract_functions(self, tokenized_code):
        """Extract functions from tokenized Java code"""
        if isinstance(tokenized_code, str):
            tokens = tokenized_code.split()
        else:
            assert isinstance(tokenized_code, list)
            tokens = tokenized_code
        i = ind_iter(len(tokens))
        functions_standalone = []
        functions_class = []
        try:
            token = tokens[i.i]
        except KeyboardInterrupt:
            raise
        except:
            return [], []
        while True:
            try:
                # detect function
                tokens_no_newline = []
                index = i.i
                while index < len(tokens) and len(tokens_no_newline) < 3:
                    index += 1
                    if tokens[index].startswith(NEWLINE_TOKEN):
                        continue
                    tokens_no_newline.append(tokens[index])

                if token == ")" and (
                    tokens_no_newline[0] == "{"
                    or (
                        tokens_no_newline[0] == "throws" and tokens_no_newline[2] == "{"
                    )
                ):
                    # go previous until the start of function
                    while token not in [";", "}", "{", "*/", "ENDCOM", NEW_LINE, "\n"]:
                        i.prev()
                        token = tokens[i.i]

                    if token == "*/":
                        while token != "/*":
                            i.prev()
                            token = tokens[i.i]
                        function = [token]
                        while token != "*/":
                            i.next()
                            token = tokens[i.i]
                            function.append(token)
                    elif token == "ENDCOM":
                        while token != "//":
                            i.prev()
                            token = tokens[i.i]
                        function = [token]
                        while token != "ENDCOM":
                            i.next()
                            token = tokens[i.i]
                            function.append(token)
                    else:
                        i.next()
                        token = tokens[i.i]
                        function = [token]

                    while token != "{":
                        i.next()
                        token = tokens[i.i]
                        function.append(token)
                    if token == "{":
                        number_indent = 1
                        while not (token == "}" and number_indent == 0):
                            try:
                                i.next()
                                token = tokens[i.i]
                                if token == "{":
                                    number_indent += 1
                                elif token == "}":
                                    number_indent -= 1
                                function.append(token)
                            except StopIteration:
                                break
                        if "static" in function[0 : function.index("{")]:
                            functions_standalone.append(
                                self.remove_annotation(" ".join(function))
                            )
                        else:
                            functions_class.append(
                                self.remove_annotation(" ".join(function))
                            )
                i.next()
                token = tokens[i.i]
            except KeyboardInterrupt:
                raise
            except:
                break
        return functions_standalone, functions_class

    def remove_annotation(self, function):
        return re.sub(
            r"^@ (Override|Deprecated|SuppressWarnings) (\( .*? \) )", "", function
        )

    def get_function_name(self, function):
        return self.get_first_token_before_first_parenthesis(function)

    def extract_arguments(self, function):
        return self.extract_arguments_using_parentheses(function)
