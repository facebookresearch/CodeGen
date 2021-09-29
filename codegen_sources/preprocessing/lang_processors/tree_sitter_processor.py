# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from codegen_sources.preprocessing.lang_processors.lang_processor import LangProcessor
from codegen_sources.preprocessing.lang_processors.tokenization_utils import (
    process_string,
    replace_tokens,
    indent_lines,
)
import re
from tree_sitter import Language, Parser
from pathlib import Path
from logging import getLogger

TREE_SITTER_ROOT = Path(__file__).parents[3].joinpath("tree-sitter")
NEW_LINE = "NEW_LINE"

logger = getLogger()
COMMENT_TYPES = {"comment", "line_comment", "block_comment"}


class TreeSitterLangProcessor(LangProcessor):
    def __init__(
        self,
        language,
        ast_nodes_type_string,
        stokens_to_chars,
        chars_to_stokens,
        root_folder,
    ):
        self.language = language
        self.ast_nodes_type_string = ast_nodes_type_string
        self.stokens_to_chars = stokens_to_chars
        self.chars_to_stokens = chars_to_stokens
        self.root_folder = Path(root_folder)
        self.root_folder.is_dir(), f"{self.root_folder} is not a directory."
        self.parser = None
        self.create_treesiter_parser()

    def create_treesiter_parser(self):
        if self.parser is None:
            lib_path = self.root_folder.joinpath(f"{self.language}.so")
            repo_path = self.root_folder.joinpath(f"tree-sitter-{self.language}")
            if not lib_path.exists():
                assert repo_path.is_dir(), repo_path
                Language.build_library(
                    # Store the library in the `build` directory
                    str(lib_path),
                    # Include one or more languages
                    [str(repo_path)],
                )
            language = Language(lib_path, self.language)
            self.parser = Parser()
            self.parser.set_language(language)

    def tokenize_code(self, code, keep_comments=False, process_strings=True):
        tokenized_code = []
        tokens, token_types = self.get_tokens_and_types(code)
        for token, token_type in zip(tokens, token_types):
            if token_type in COMMENT_TYPES and keep_comments is False:
                continue
            if token_type in self.ast_nodes_type_string:
                token = process_string(
                    token,
                    self.chars_to_stokens,
                    self.stokens_to_chars,
                    token_type in COMMENT_TYPES,
                    process_strings,
                )
            if len(token) > 0:
                if token_type not in self.ast_nodes_type_string:
                    token = token.replace("\n", "NEW_LINE")
                    token = token.replace("NEW_LINENEW_LINE", "NEW_LINE")
                tokenized_code.append(token)
        return tokenized_code

    def get_tokens_and_types(self, code):
        code = code.replace("\r", "")
        code = bytes(code, "utf8")
        tree = self.get_ast(code)
        tokens = []
        tokens_type = []
        self.dfs(code, tree.root_node, tokens, tokens_type)
        return tokens, tokens_type

    def get_ast(self, code):
        assert isinstance(code, str) or isinstance(code, bytes)
        if isinstance(code, str):
            code = bytes(code, "utf8")
        tree = self.parser.parse(code)
        return tree

    def dfs(self, code, node, tokens, tokens_type):
        if len(node.children) == 0 or node.type in self.ast_nodes_type_string:
            snippet = code[node.start_byte : node.end_byte].strip(b" ")
            if isinstance(snippet, bytes):
                snippet = snippet.decode("utf8")
            if len(snippet) > 0:
                tokens.append(snippet)
                tokens_type.append(node.type)
            return
        for child in node.children:
            self.dfs(code, child, tokens, tokens_type)

    def detokenize_code(self, code):
        # TODO make this cleaner with tree sitter AST ?
        assert isinstance(code, str) or isinstance(code, list)
        if isinstance(code, list):
            code = " ".join(code)
        code = code.replace("ENDCOM", "\n")
        code = code.replace("NEW_LINE", "\n")

        replaced_tokens = []
        # call parser of the tokenizer to find comments and string and detokenize them correctly
        try:
            tokens, token_types = self.get_tokens_and_types(code)
            for token, token_type in zip(tokens, token_types):
                if token_type in self.ast_nodes_type_string:
                    token_ = token.replace("STRNEWLINE", "\n").replace(
                        "TABSYMBOL", "\t"
                    )
                    token_ = (
                        replace_tokens(token_, self.chars_to_stokens)
                        .replace(" ", "")
                        .replace("▁", " ")
                    )
                    if token_type in COMMENT_TYPES:
                        token_ += "\n"
                    replaced_tokens.append(token_)
                else:
                    replaced_tokens.append(token)
                    if token in {";", "{", "}"}:
                        replaced_tokens.append("\n")
        except KeyboardInterrupt:
            raise
        except:
            pass

        code = " ".join(replaced_tokens)
        code = code.replace("\n", "NEW_LINE")
        code = code.replace('} "', 'CB_ "')
        code = code.replace('" {', '" OB_')
        code = code.replace("} ;", "CB_COLON")
        code = code.replace("} ,", "CB_COMA")
        code = code.replace("}", "CB_")
        code = code.replace("{", "OB_")
        code = replace_tokens(code, self.stokens_to_chars)
        lines = re.split("NEW_LINE", code)

        untok_s = indent_lines(lines)
        untok_s = (
            untok_s.replace("CB_COLON", "};")
            .replace("CB_COMA", "},")
            .replace("CB_", "}")
            .replace("OB_", "{")
        )
        untok_s = untok_s.replace("> > >", ">>>").replace("<< <", "<<<")
        untok_s = untok_s.replace("> >", ">>").replace("< <", "<<")

        return untok_s

    def extract_arguments_using_parentheses(self, function):
        function = function.split(" ")
        types = []
        names = []
        par = 0
        arguments = []
        function = function[function.index("(") :]
        for tok in function:
            if tok == "(":
                par += 1
            elif tok == ")":
                par -= 1
            arguments.append(tok)
            if par == 0:
                break
        arguments = " ".join(arguments[1:-1])
        if arguments == "":
            return ["None"], ["None"]
        arguments = arguments.split(",")
        for arg in arguments:
            bracks = re.findall("\[ \]", arg)
            bracks = " ".join(bracks)
            arg = arg.replace(bracks, "")
            arg = arg.strip()
            arg = re.sub(" +", " ", arg)
            t = " ".join(arg.split(" ")[:-1] + [bracks])
            n = arg.split(" ")[-1]
            types.append(t)
            names.append(n)
        return types, names

    def get_first_token_before_first_parenthesis(self, code):
        assert isinstance(code, str) or isinstance(
            code, list
        ), f"function is not the right type, should be str or list : {code}"
        if isinstance(code, str):
            code = code.split()
        return code[code.index("(") - 1]
