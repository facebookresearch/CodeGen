# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import random
import re
import subprocess
import uuid
from pathlib import Path
import typing as tp

import codegen_sources
from codegen_sources.preprocessing.obfuscation import javalang_obfuscator
from codegen_sources.preprocessing.obfuscation.utils_deobfuscation import dico_to_string

# BEWARE: two differente new line tokens?
from .tokenization_utils import ind_iter
from .tree_sitter_processor import (
    TreeSitterLangProcessor,
    TREE_SITTER_ROOT,
    NEWLINE_TOK,
)
import tree_sitter as ts

from ...code_runners.code_runner import RUN_ROOT_DIR
from ...code_runners.utils import MAX_VIRTUAL_MEMORY, limit_virtual_memory
import typing as tp

GOOGLE_JAVA_FORMAT_PATH = (
    Path(codegen_sources.__file__).parents[1]
    / "data"
    / "tools"
    / "google-java-format-1.15.0-all-deps.jar"
)

JAVA_TOKEN2CHAR: tp.Dict[str, str] = {
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
JAVA_CHAR2TOKEN: tp.Dict[str, str] = {
    value: " " + key + " " for key, value in JAVA_TOKEN2CHAR.items()
}


class JavaProcessor(TreeSitterLangProcessor):
    def __init__(self, root_folder: Path = TREE_SITTER_ROOT) -> None:

        super().__init__(
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

    def _get_functions_from_ast(
        self,
        code: str,
        node: ts.Node,
        class_funcs: tp.List[str],
        standalone_funcs: tp.List[str],
        _in_class: bool = False,  # ignored
    ) -> None:
        if node.type == "method_declaration":
            function = code[node.start_byte : node.end_byte]
            # There can be some issues where "{" is not in the function string.
            # In that case, it is not a proper function
            if "{" in function:
                if "static" in function[0 : function.index("{")]:
                    standalone_funcs.append(function)
                else:
                    class_funcs.append(function)

        for child in node.children:
            self._get_functions_from_ast(
                code, child, class_funcs, standalone_funcs,
            )

    @staticmethod
    def remove_annotation(function):
        return re.sub(
            r"^@ (Override|Deprecated|SuppressWarnings) (\( .*? \) )", "", function
        )

    def get_function_name(self, function):
        return self.get_first_token_before_first_parenthesis(function)

    def extract_arguments(self, function):
        return self.extract_arguments_using_parentheses(function)

    @staticmethod
    def get_class_name(tokenized_java):
        if isinstance(tokenized_java, str):
            tokenized_java = tokenized_java.split()
        assert (
            "class" in tokenized_java
        ), f"No class definition or bad tokenization for {tokenized_java}"
        return tokenized_java[tokenized_java.index("class") + 1]

    @staticmethod
    def format(code: str) -> str:
        output_dir = RUN_ROOT_DIR / "formatting" / "java_formatting"
        output_dir.mkdir(exist_ok=True, parents=True)
        filename = f"{uuid.uuid4()}.java"
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


def get_java_compilation_errors(code, timeout=20):
    file = write_java_function(code)
    comp_cmd = (
        f"{limit_virtual_memory(MAX_VIRTUAL_MEMORY)}; module load java; javac {file}"
    )
    timed_out = False
    try:
        proc = subprocess.run(
            comp_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            executable="/bin/bash",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "timeout"
    file.unlink()
    classfile = file.with_suffix(".class")
    assert (
        timed_out or proc.returncode != 0 or classfile.is_file()
    ), "compilation succeeded but .class file does not exist"
    assert "tmp_folder" in str(file.parent), file.parent
    for compiled_f in file.parent.glob("*"):
        compiled_f.unlink()
    file.parent.rmdir()
    if timed_out:
        return "timeout"
    return "success" if proc.returncode == 0 else proc.stderr.decode()


def write_java_function(f: str, out_path: Path = Path("/tmp/java_functions/")) -> Path:
    rand_folder = str(random.getrandbits(64))
    classname = f"JAVA_FUNC"
    tmp_folder = out_path.joinpath(f"tmp_folder_{rand_folder}")
    out_file = tmp_folder.joinpath(classname + ".java")
    tmp_folder.mkdir(parents=True, exist_ok=True)
    java_processor = JavaProcessor()

    with open(out_file, "w") as writefile:
        writefile.write(
            """
import java.util.*;
import java.util.stream.*;
import java.lang.*;
import javafx.util.Pair;
"""
        )
        writefile.write("public class " + classname + "{\n")
        code = f.replace("\r", "")
        writefile.write(java_processor.detokenize_code(code))
        writefile.write("}\n")
    return out_file
