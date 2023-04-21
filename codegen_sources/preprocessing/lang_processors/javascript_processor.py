# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from pathlib import Path
from .java_processor import JAVA_CHAR2TOKEN, JAVA_TOKEN2CHAR
from .tree_sitter_processor import TreeSitterLangProcessor, TREE_SITTER_ROOT

JS_TOKEN2CHAR = JAVA_TOKEN2CHAR.copy()
JS_CHAR2TOKEN = JAVA_CHAR2TOKEN.copy()


class JavascriptProcessor(TreeSitterLangProcessor):
    def __init__(self, root_folder: Path = TREE_SITTER_ROOT) -> None:

        super().__init__(
            ast_nodes_type_string=["comment", "string"],
            stokens_to_chars=JS_TOKEN2CHAR,
            chars_to_stokens=JS_CHAR2TOKEN,
            root_folder=root_folder,
        )
