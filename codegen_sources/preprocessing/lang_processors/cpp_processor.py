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
from codegen_sources.preprocessing.lang_processors.java_processor import (
    JAVA_TOKEN2CHAR,
    JAVA_CHAR2TOKEN,
)
from codegen_sources.preprocessing.lang_processors.tokenization_utils import ind_iter
import re

IDENTIFIERS = {"identifier", "field_identifier"}

CPP_TOKEN2CHAR = JAVA_TOKEN2CHAR.copy()
CPP_CHAR2TOKEN = JAVA_CHAR2TOKEN.copy()


class CppProcessor(TreeSitterLangProcessor):
    def __init__(self, root_folder):
        super().__init__(
            language="cpp",
            ast_nodes_type_string=["comment", "string_literal", "char_literal"],
            stokens_to_chars=CPP_TOKEN2CHAR,
            chars_to_stokens=CPP_CHAR2TOKEN,
            root_folder=root_folder,
        )

    def get_function_name(self, function):
        return self.get_first_token_before_first_parenthesis(function)

    def extract_arguments(self, function):
        return self.extract_arguments_using_parentheses(function)

    def clean_hashtags_function(self, function):
        function = re.sub('[#][ ][i][n][c][l][u][d][e][ ]["].*?["]', "", function)
        function = re.sub("[#][ ][i][n][c][l][u][d][e][ ][<].*?[>]", "", function)
        function = re.sub("[#][ ][i][f][n][d][e][f][ ][^ ]*", "", function)
        function = re.sub("[#][ ][i][f][d][e][f][ ][^ ]*", "", function)
        function = re.sub(
            "[#][ ][d][e][f][i][n][e][ ][^ ]*[ ][(][ ].*?[ ][)][ ][(][ ].*[ ][)]",
            "",
            function,
        )
        function = re.sub(
            "[#][ ][d][e][f][i][n][e][ ][^ ]*[ ][(][ ].*?[ ][)][ ][{][ ].*[ ][}]",
            "",
            function,
        )
        function = re.sub(
            '[#][ ][d][e][f][i][n][e][ ][^ ]*[ ]([(][ ])?["].*?["]([ ][)])?',
            "",
            function,
        )
        function = re.sub(
            "[#][ ][d][e][f][i][n][e][ ][^ ]*[ ]([(][ ])?\d*\.?\d*([ ][+-/*][ ]?\d*\.?\d*)?([ ][)])?",
            "",
            function,
        )
        function = re.sub("[#][ ][d][e][f][i][n][e][ ][^ ]", "", function)
        function = re.sub(
            "[#][ ][i][f][ ][d][e][f][i][n][e][d][ ][(][ ].*?[ ][)]", "", function
        )
        function = re.sub("[#][ ][i][f][ ][^ ]*", "", function)
        function = function.replace("# else", "")
        function = function.replace("# endif", "")
        function = function.strip()
        return function

    def extract_functions(self, code):
        """Extract functions from tokenized C++ code"""
        if isinstance(code, list):
            code = " ".join(code)
        else:
            assert isinstance(code, str)

        try:
            code = self.clean_hashtags_function(code)
            code = (
                code.replace("ENDCOM", "\n")
                .replace("▁", "SPACETOKEN")
                .replace(NEW_LINE, "\n")
            )
            tokens, token_types = self.get_tokens_and_types(code)
            tokens = list(zip(tokens, token_types))
        except KeyboardInterrupt:
            raise
        except:
            return [], []
        i = ind_iter(len(tokens))
        functions_standalone = []
        functions_class = []
        try:
            token, token_type = tokens[i.i]
        except:
            return [], []
        while True:
            try:
                # detect function
                if token == ")" and (
                    (tokens[i.i + 1][0] == "{" and tokens[i.i + 2][0] != "}")
                    or (
                        tokens[i.i + 1][0] == "throw"
                        and tokens[i.i + 4][0] == "{"
                        and tokens[i.i + 5][0] != "}"
                    )
                ):
                    # go previous until the start of function
                    while token not in {";", "}", "{", NEW_LINE, "\n"}:
                        try:
                            i.prev()
                        except StopIteration:
                            break
                        token = tokens[i.i][0]
                    # We are at the beginning of the function
                    i.next()
                    token, token_type = tokens[i.i]
                    if token_type == "comment":
                        token = token.strip()
                        token += " ENDCOM"
                    function = [token]
                    token_types = [token_type]
                    while token != "{":
                        i.next()
                        token, token_type = tokens[i.i]
                        if token_type == "comment":
                            token = token.strip()
                            token += " ENDCOM"
                        function.append(token)
                        token_types.append(token_type)

                    if token_types[function.index("(") - 1] not in IDENTIFIERS:
                        continue
                    if token_types[function.index("(") - 1] == "field_identifier":
                        field_identifier = True
                    else:
                        field_identifier = False
                    if token == "{":
                        number_indent = 1
                        while not (token == "}" and number_indent == 0):
                            try:
                                i.next()
                                token, token_type = tokens[i.i]
                                if token == "{":
                                    number_indent += 1
                                elif token == "}":
                                    number_indent -= 1
                                if token_type == "comment":
                                    token = token.strip()
                                    token += " ENDCOM"
                                function.append(token)
                            except StopIteration:
                                break

                        if (
                            "static" in function[0 : function.index("{")]
                            or "::" not in function[0 : function.index("(")]
                            and not field_identifier
                        ):
                            function = " ".join(function)
                            function = re.sub(
                                "[<][ ][D][O][C][U][M][E][N][T].*?[>] ", "", function
                            )
                            function = self.clean_hashtags_function(function)
                            function = function.strip()
                            function = function.replace("\n", "ENDCOM").replace(
                                "SPACETOKEN", "▁"
                            )
                            if not re.sub(
                                "[^ ]*[ ][(][ ]\w*([ ][,][ ]\w*)*[ ][)]",
                                "",
                                function[: function.index("{")],
                            ).strip().startswith("{") and not function.startswith("#"):
                                functions_standalone.append(function)
                        else:
                            function = " ".join(function)
                            function = re.sub(
                                "[<][ ][D][O][C][U][M][E][N][T].*?[>] ", "", function
                            )
                            function = self.clean_hashtags_function(function)
                            function = function.strip()
                            function = function.replace("\n", "ENDCOM").replace(
                                "SPACETOKEN", "▁"
                            )
                            if not re.sub(
                                "[^ ]*[ ][(][ ]\w*([ ][,][ ]\w*)*[ ][)]",
                                "",
                                function[: function.index("{")],
                            ).strip().startswith("{") and not function.startswith("#"):
                                functions_class.append(function)
                i.next()
                token = tokens[i.i][0]
            except KeyboardInterrupt:
                raise
            except:
                break

        return functions_standalone, functions_class

    def detokenize_code(self, code):
        fix_func_defines_pattern = re.compile(r"#define (.*) \(")
        detokenized = super().detokenize_code(code)
        detokenized = fix_func_defines_pattern.sub(r"#define \1(", detokenized)
        return detokenized
