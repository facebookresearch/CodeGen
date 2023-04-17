# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import re
import logging
import itertools
import typing as tp
from pathlib import Path

import tree_sitter as ts
from .lang_processor import LangProcessor
from .lang_processor import NEWLINE_TOK as NEWLINE_TOK
from .tokenization_utils import indent_lines, process_string, replace_tokens

TREE_SITTER_ROOT: Path = Path(__file__).resolve().parents[3] / "tree-sitter"

logger = logging.getLogger(__name__)
COMMENT_TYPES = {"comment", "line_comment", "block_comment", "docstring"}


class TreeSitterLangProcessor(LangProcessor):
    def __init__(
        self,
        ast_nodes_type_string: tp.List[str],
        stokens_to_chars: tp.Dict[str, str],
        chars_to_stokens: tp.Dict[str, str],
        root_folder: Path,  # not default to make sure children implement it
        function_declr: tp.Optional[str] = None,
        new_line_sensitive: bool = False,
    ) -> None:
        self.new_line_sensitive = new_line_sensitive
        self.ast_nodes_type_string = ast_nodes_type_string
        self.stokens_to_chars = stokens_to_chars
        self.chars_to_stokens = chars_to_stokens
        self.root_folder = Path(root_folder)
        assert self.root_folder.is_dir(), f"{self.root_folder} is not a directory."
        self._parser: tp.Optional[ts.Parser] = None
        self.parser  # initialize it
        self.function_declr = function_declr

    @property
    def parser(self) -> ts.Parser:
        if self._parser is not None:
            return self._parser
        lib_path = self.root_folder / f"{self.language}.so"
        repo_path = self.root_folder / f"tree-sitter-{self.language}"
        if not lib_path.exists():
            logger.warning("Building %s parser into %s", self.language, lib_path)
            assert repo_path.is_dir(), repo_path
            ts.Language.build_library(
                # Store the library in the `build` directory
                str(lib_path),
                # Include one or more languages
                [str(repo_path)],
            )
        language = ts.Language(lib_path, self.language)
        self._parser = ts.Parser()
        self._parser.set_language(language)
        return self._parser

    def __getstate__(self) -> tp.Dict[str, tp.Any]:
        attributes = dict(self.__dict__)
        key = "_parser"
        if key not in attributes:
            raise RuntimeError(f"key {key} should be in the attributes")
        attributes[key] = None  # TreeSitter is not picklable
        return attributes

    def tokenize_code(
        self, code: str, keep_comments: bool = False, process_strings: bool = True
    ) -> tp.List[str]:
        tokenized_code = []
        tokens, token_types = self.get_tokens_and_types(code)
        skip_next_new_line = False
        for token, token_type in zip(tokens, token_types):
            if skip_next_new_line and token == NEWLINE_TOK:
                continue
            if token_type in COMMENT_TYPES and not keep_comments:
                token = ""  # Ignored later on
            else:
                # comments at the end of docstring still require skipping
                skip_next_new_line = False
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
                    token = token.replace("\n", NEWLINE_TOK)
                    token = token.replace(NEWLINE_TOK * 2, NEWLINE_TOK)
                tokenized_code.append(token)
            elif token_type == "docstring":
                skip_next_new_line = True  # make sure we remove extraline in python

        tokenized_code2 = []
        for tok1, tok2 in itertools.zip_longest(tokenized_code, tokenized_code[1:]):
            tokenized_code2.append(tok1)
            if (tok1, tok2) == ("INDENT", "DEDENT"):
                tokenized_code2.extend(["pass", NEWLINE_TOK])
        return tokenized_code2

    def get_tokens_and_types(self, code: str) -> tp.Tuple[tp.List[str], tp.List[str]]:
        code = code.replace("\r", "")
        bcode = bytes(code, "utf8")
        tree = self.get_ast(bcode)
        tokens: tp.List[str] = []
        tokens_type: tp.List[str] = []
        self.dfs(bcode, tree.root_node, tokens, tokens_type)
        return tokens, tokens_type

    def get_ast(self, code: tp.Union[str, bytes]) -> ts.Tree:
        assert isinstance(code, (str, bytes))
        if isinstance(code, str):
            code = bytes(code, "utf8")
        tree = self.parser.parse(code)
        return tree

    def dfs(
        self,
        code: bytes,
        node: ts.Node,
        tokens: tp.List[str],
        tokens_type: tp.List[str],
    ) -> None:
        if len(node.children) == 0 or node.type in self.ast_nodes_type_string:
            bsnippet = code[node.start_byte : node.end_byte].strip(b" ")
            snippet = bsnippet.decode("utf8")
            if len(snippet) > 0:
                tokens.append(snippet)
                tokens_type.append(node.type)
            return
        for child in node.children:
            self.dfs(code, child, tokens, tokens_type)

    def detokenize_code(self, code: tp.Union[str, tp.List[str]]) -> str:

        # TODO make this cleaner with tree sitter AST ?
        assert isinstance(code, (list, str))
        if isinstance(code, list):
            code = " ".join(code)
        code = code.replace("ENDCOM", "\n")
        code = code.replace(NEWLINE_TOK, "\n")

        replaced_tokens = []
        # call parser of the tokenizer to find comments and string and
        # detokenize them correctly
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
                    if not self.new_line_sensitive and token in {";", "{", "}"}:
                        replaced_tokens.append("\n")
        except KeyboardInterrupt as e:
            raise e
        except Exception:  # pylint: disable=broad-except
            pass

        code = " ".join(replaced_tokens)
        code = code.replace("\n", NEWLINE_TOK)
        code = code.replace('} "', 'CB_ "')
        code = code.replace('" {', '" OB_')
        code = code.replace("} ;", "CB_COLON")
        code = code.replace("} ,", "CB_COMA")
        code = code.replace("}", "CB_")
        code = code.replace("{", "OB_")
        code = replace_tokens(code, self.stokens_to_chars)
        lines = re.split(NEWLINE_TOK, code)

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

    def _get_functions_from_ast(
        self,
        code: str,
        node: ts.Node,
        class_funcs: tp.List[str],
        standalone_funcs: tp.List[str],
        _in_class: bool = False,
    ) -> None:
        raise NotImplementedError(
            f"Implement _get_functions_from_ast() in {self.__class__.__name__} to extract functions"
        )

    def extract_functions(
        self, code: tp.Union[str, tp.List[str]], tokenized: bool = True,
    ) -> tp.Tuple[tp.List[str], tp.List[str]]:
        """
        Extract functions from python code
        tokenized; whether the code is tokenized or not
        """
        if isinstance(code, list):
            code = " ".join(code)
        if tokenized:
            code = self.detokenize_code(code)
        ast = self.get_ast(code)
        class_funcs: tp.List[str] = []
        standalone_funcs: tp.List[str] = []
        self._get_functions_from_ast(code, ast.root_node, class_funcs, standalone_funcs)
        if tokenized:
            class_funcs = [" ".join(self.tokenize_code(f)) for f in class_funcs]
            standalone_funcs = [
                " ".join(self.tokenize_code(f)) for f in standalone_funcs
            ]
        return standalone_funcs, class_funcs

    @staticmethod
    def extract_arguments_using_parentheses(
        function_str: str,
    ) -> tp.Tuple[tp.List[str], tp.List[str]]:
        function = function_str.split(" ")
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
        arguments_str = " ".join(arguments[1:-1])
        if arguments_str == "":
            return ["None"], ["None"]
        arguments = arguments_str.split(",")
        for arg in arguments:
            bracks = re.findall(r"\[ \]", arg)
            bracks_str = " ".join(bracks)
            arg = arg.replace(bracks_str, "")
            arg = arg.strip()
            arg = re.sub(" +", " ", arg)
            t = " ".join(arg.split(" ")[:-1] + [bracks_str])
            n = arg.split(" ")[-1]
            types.append(t)
            names.append(n)
        return types, names

    @staticmethod
    def get_first_token_before_first_parenthesis(
        code: tp.Union[str, tp.List[str]]
    ) -> str:
        assert isinstance(
            code, (str, list)
        ), f"function is not the right type, should be str or list : {code}"
        if isinstance(code, str):
            code = code.split()
        return code[code.index("(") - 1]


def traverse_tree(tree: ts.Tree, final: tp.Sequence[str] = ()) -> tp.Iterator[ts.Node]:
    """Traverses a tree-sitter tree, yielding final nodes

    Parameters
    ----------
    final: sequence of str
        consider these types as final even if it has children

    Yields
    ------
    Node
        a final node (either with no children, or in the "final" list)
    """
    final = list(final)
    cursor = tree.walk()
    reached_root = False
    while not reached_root:
        yield cursor.node
        if cursor.node.type not in final and cursor.goto_first_child():
            continue
        if cursor.goto_next_sibling():
            continue
        retracing = True
        while retracing:
            if not cursor.goto_parent():
                retracing = False
                reached_root = True
            if cursor.goto_next_sibling():
                retracing = False
