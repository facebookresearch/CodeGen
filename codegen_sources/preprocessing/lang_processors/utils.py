# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import typing as tp

from codegen_sources.model.src.data.dictionary import (
    OBF,
    OBFS,
)


def obfuscation_tokens(raise_finished: bool = True) -> tp.Iterator[str]:
    """Iterates on all obfuscation tokens"""
    for name in ["VAR", "FUNC", "CLASS"]:
        for k in range(OBFS[name]):
            yield OBF[name] % k
    if raise_finished:
        raise RuntimeError("Running out of obfuscation tokens")
