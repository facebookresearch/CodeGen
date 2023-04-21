# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from .. import dataset_modes


def test_modes_dict() -> None:
    must_be_avail = {
        "obfuscation",
        "monolingual",
        "monolingual_functions",
        "obfuscation_functions",
        "ir_functions",
        "ir_full_files",
    }
    avail = dataset_modes.DatasetMode.modes
    remain = must_be_avail - set(avail.keys())
    assert not remain
