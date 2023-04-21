# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

REF = "REF"
OUT = "OUT"
HYPO = "HYPO"
IR = "IR"
SOURCE = "SOURCE"
SUPPORTED_LANGUAGES_FOR_TESTS = {"java", "python", "cpp", "rust", "go"}
EXT = {"rust": ".rs", "cpp": ".cpp", "java": ".java", "python": ".py", "go": ".go"}
FALSY_STRINGS = {"off", "false", "0"}
TRUTHY_STRINGS = {"on", "true", "1"}
TOKENIZATION_MODES = {"fastbpe", "roberta", "sentencepiece"}
