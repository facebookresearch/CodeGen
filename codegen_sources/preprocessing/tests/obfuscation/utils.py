# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import difflib


def diff_tester(expected, res, split="\n"):
    d = difflib.Differ()
    if expected != res:
        print("Expected:")
        print(expected)
        print("#" * 50)
        print("Got:")
        print(res)
        print("#" * 50)
        diff = d.compare(expected.split(split), res.split(split))
        for line in diff:
            print(line)
        assert expected == res
