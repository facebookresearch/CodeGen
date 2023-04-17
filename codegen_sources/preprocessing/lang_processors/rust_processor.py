# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import re
from pathlib import Path

from .java_processor import JAVA_CHAR2TOKEN, JAVA_TOKEN2CHAR
from .tokenization_utils import ind_iter
from .tree_sitter_processor import (
    COMMENT_TYPES,
    NEWLINE_TOK,
    TreeSitterLangProcessor,
    TREE_SITTER_ROOT,
)
import tree_sitter as ts
import typing as tp

RUST_TOKEN2CHAR = JAVA_TOKEN2CHAR.copy()
RUST_CHAR2TOKEN = JAVA_CHAR2TOKEN.copy()


class RustProcessor(TreeSitterLangProcessor):
    def __init__(self, root_folder: Path = TREE_SITTER_ROOT) -> None:
        super().__init__(
            ast_nodes_type_string=[
                "comment",
                "line_comment",
                "block_comment",
                "string_literal",
                "raw_string_literal",
                "char_literal",
            ],
            stokens_to_chars=RUST_TOKEN2CHAR,
            chars_to_stokens=RUST_CHAR2TOKEN,
            root_folder=root_folder,
        )

    def dfs(
        self,
        code: bytes,
        node: ts.Node,
        tokens: tp.List[str],
        tokens_type: tp.List[str],
        scope_info: bool = False,
    ) -> None:
        previous_endpoints = [0]
        return self._dfs(code, node, tokens, tokens_type, previous_endpoints)

    def _dfs(self, code, node, tokens, tokens_type, previous_endpoints):
        if len(node.children) == 0 or node.type in self.ast_nodes_type_string:
            snippet = code[node.start_byte : node.end_byte]
            if node.start_byte > previous_endpoints[-1]:
                previous_snippet = (
                    code[previous_endpoints[-1] : node.start_byte]
                    .strip()
                    .decode("utf8")
                )
                if len(previous_snippet) > 0:
                    tokens.append(previous_snippet)
                    tokens_type.append("was_missing")
                    previous_endpoints.append(node.start_byte)

            if isinstance(snippet, bytes):
                snippet = snippet.decode("utf8")
            if len(snippet) > 0:
                tokens.append(snippet)
                tokens_type.append(node.type)
                previous_endpoints.append(node.end_byte)
            return
        for child in node.children:
            self._dfs(code, child, tokens, tokens_type, previous_endpoints)

    def detokenize_code(self, code):
        assert isinstance(code, str) or isinstance(code, list)
        if isinstance(code, list):
            code = " ".join(code)
        code = re.sub(r"' (.) '", r"'\1'", code)
        return super().detokenize_code(code)

    def get_function_name(self, function):
        assert isinstance(function, str) or isinstance(
            function, list
        ), f"function is not the right type, should be str or list : {function}"
        if isinstance(function, str):
            function = function.split()
        assert "fn" in function, "function definition in rust should contain token 'fn'"
        return function[function.index("fn") + 1]

    def extract_arguments(self, function):
        return self.extract_arguments_using_parentheses(function)

    def extract_functions(
        self, code: tp.Union[str, tp.List[str]], tokenized: bool = True,
    ) -> tp.Tuple[tp.List[str], tp.List[str]]:
        """Extract functions from tokenized rust code"""
        # TODO: make it use the AST to work on untokenized code
        if not tokenized:
            assert isinstance(code, str)
            code = " ".join(self.tokenize_code(code))
        if isinstance(code, list):
            code_str = " ".join(code)
        else:
            code_str = code
        try:
            code_str = (
                code_str.replace("ENDCOM", "\n")
                .replace("▁", "SPACETOKEN")
                .replace(NEWLINE_TOK, "\n")
            )
            tokens, token_types = self.get_tokens_and_types(code_str)
            tokens_types = list(zip(tokens, token_types))
        except KeyboardInterrupt:
            raise
        except:
            return [], []
        i = ind_iter(len(tokens_types))
        functions_standalone = []
        functions_class = []
        in_class = False
        class_indentation = 0
        try:
            token, token_type = tokens_types[i.i]
        except:
            return [], []
        while True:
            try:
                if token == "struct" or token == "trait" or token == "impl":
                    in_class = True

                if in_class and token == "{":
                    class_indentation += 1
                if in_class and token == "}":
                    class_indentation -= 1
                    if class_indentation < 0:
                        raise ValueError("Issue parsing the scopes of the file")
                    if class_indentation == 0:
                        in_class = False

                # detect function
                if token == "fn":
                    # We are at the beginning of the function
                    token, token_type = tokens_types[i.i]
                    function = [token]
                    token_types = [token_type]
                    definition_only = False
                    while token != "{":
                        i.next()
                        token, token_type = tokens_types[i.i]
                        if token == ";":
                            definition_only = True
                            function = []
                            break
                        if token_type in COMMENT_TYPES:
                            token = token.strip()
                            token += " ENDCOM"
                        function.append(token)
                        token_types.append(token_type)
                    if definition_only:
                        continue
                    if token == "{":
                        number_indent = 1
                        while not (token == "}" and number_indent == 0):
                            try:
                                i.next()
                                token, token_type = tokens_types[i.i]
                                if token == "{":
                                    number_indent += 1
                                elif token == "}":
                                    number_indent -= 1
                                if token_type in COMMENT_TYPES:
                                    token = token.strip()
                                    token += " ENDCOM"
                                function.append(token)
                            except StopIteration:
                                break

                        function_str = " ".join(function)
                        function_str = function_str.strip()
                        function_str = function_str.replace("\n", "ENDCOM").replace(
                            "SPACETOKEN", "▁"
                        )
                        if in_class:
                            functions_class.append(function_str)
                        else:
                            functions_standalone.append(function_str)
                i.next()
                token = tokens_types[i.i][0]
            except KeyboardInterrupt:
                raise
            except:
                break

        return functions_standalone, functions_class
