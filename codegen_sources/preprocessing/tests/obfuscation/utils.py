# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import difflib
import typing as tp


def diff_tester(
    expected: tp.Union[str, tp.Iterable[tp.Any]],
    res: tp.Union[str, tp.Iterable[tp.Any]],
    split: str = "\n",
    normalization: tp.Optional[tp.Callable] = str,
) -> None:
    d = difflib.Differ()
    if expected != res:
        print("Expected:")
        print(expected)
        print("#" * 50)
        print("Got:")
        print(res)
        print("#" * 50)
        if isinstance(expected, str):
            expected_split = expected.split(split)
        else:
            expected_split = expected  # type: ignore
        if isinstance(res, str):
            res_split = res.split(split)
        else:
            res_split = res  # type: ignore
        if normalization is not None:
            expected_split = [normalization(x) for x in expected_split]
            res_split = [normalization(x) for x in res_split]
        diff = d.compare(expected_split, res_split)
        for line in diff:
            print(line)
        assert split.join(expected_split) == split.join(
            res_split
        ), f"EXPECTED: \n{split.join(expected_split)}\n\nGOT: \n{split.join(res_split)}\n"
