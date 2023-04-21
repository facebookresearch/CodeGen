# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import re
import subprocess
import uuid
from pathlib import Path
from .tree_sitter_processor import (
    TreeSitterLangProcessor,
    NEWLINE_TOK,
    TREE_SITTER_ROOT,
)
from .java_processor import JAVA_CHAR2TOKEN, JAVA_TOKEN2CHAR
from .tokenization_utils import ind_iter
import typing as tp
import tree_sitter as ts

from ...code_runners.code_runner import RUN_ROOT_DIR

IDENTIFIERS = {"identifier", "field_identifier"}

CPP_TOKEN2CHAR = JAVA_TOKEN2CHAR.copy()
CPP_CHAR2TOKEN = JAVA_CHAR2TOKEN.copy()


class CppProcessor(TreeSitterLangProcessor):
    def __init__(self, root_folder: Path = TREE_SITTER_ROOT) -> None:
        super().__init__(
            ast_nodes_type_string=["comment", "string_literal", "char_literal"],
            stokens_to_chars=CPP_TOKEN2CHAR,
            chars_to_stokens=CPP_CHAR2TOKEN,
            root_folder=root_folder,
        )

    def get_function_name(self, function: tp.Union[str, tp.List[str]]) -> str:
        return self.get_first_token_before_first_parenthesis(function)

    def extract_arguments(self, function: str) -> tp.Tuple[tp.List[str], tp.List[str]]:
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
            r"[#][ ][d][e][f][i][n][e][ ][^ ]*[ ]([(][ ])?\d*\.?\d*([ ][+-/*][ ]?\d*\.?\d*)?([ ][)])?",
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

    def _get_functions_from_ast(
        self,
        code: str,
        node: ts.Node,
        class_funcs: tp.List[str],
        standalone_funcs: tp.List[str],
        _in_class: bool = False,
    ) -> None:
        if node.type == "function_definition":
            function = code[node.start_byte : node.end_byte]
            # Avoid incorrect functions
            if (
                not function.strip().startswith("class")
                and "(" in function
                and "{" in function
            ):
                if (
                    not _in_class or "static" in function[0 : function.index("{")]
                ) and "::" not in function[0 : function.index("(")]:
                    standalone_funcs.append(function)
                else:
                    class_funcs.append(function)

        for child in node.children:
            self._get_functions_from_ast(
                code,
                child,
                class_funcs,
                standalone_funcs,
                node.type == "class_specifier" or _in_class,
            )

    def detokenize_code(self, code):
        fix_func_defines_pattern = re.compile(r"#define (.*) \(")
        detokenized = super().detokenize_code(code)
        detokenized = fix_func_defines_pattern.sub(r"#define \1(", detokenized)
        return detokenized

    @staticmethod
    def format(code: str) -> str:
        output_dir = RUN_ROOT_DIR / "formatting" / "cpp_formatting"
        output_dir.mkdir(exist_ok=True, parents=True)
        filename = f"{uuid.uuid4()}.cpp"
        filepath = output_dir / filename
        try:
            with open(filepath, "w") as f:
                f.write(code)
            cmd = f"clang-format {filepath}"
            proc = subprocess.run(
                cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True
            )
            if proc.returncode != 0:
                raise ValueError(
                    f"Failed to format code with error: {proc.stderr.decode()}\nThe code was:\n{code}\nFull command: {cmd}"
                )
        except Exception:
            raise
        finally:
            filepath.unlink(missing_ok=True)
        return proc.stdout.decode()
