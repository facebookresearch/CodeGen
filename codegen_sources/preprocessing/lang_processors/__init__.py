# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from .lang_processor import LangProcessor as LangProcessor  # for explicit reimport
from .tree_sitter_processor import TREE_SITTER_ROOT as TREE_SITTER_ROOT
from .cpp_processor import CppProcessor as CppProcessor
from .go_processor import GoProcessor as GoProcessor
from .java_processor import JavaProcessor as JavaProcessor
from .python_processor import PythonProcessor as PythonProcessor
from .python_tree_sitter_processor import (
    PythonTreeSitterProcessor as PythonTreeSitterProcessor,
)
from .rust_processor import RustProcessor as RustProcessor
from .ir_processor import IRProcessor as IRProcessor
