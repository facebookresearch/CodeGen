# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import typing as tp
import re

SEPARATOR = " | "
OBFUSCATED_PREFIXES = ["VAR_", "FUNC_", "CLASS_"]
REPLACE_DICT = {
    protected_name: protected_name.lower() for protected_name in OBFUSCATED_PREFIXES
}


def cleanup_obfuscated_function(func: str, dico: str) -> tp.Tuple[str, str]:
    rename_dict = build_rename_dict(func)
    previous_dict = read_dict(dico)
    assert set(rename_dict.keys()).issubset(
        set(previous_dict.keys())
    ), "invalid keys in rename dict"
    new_func = " ".join([rename_tok(tok, rename_dict) for tok in func.split()])
    func_dico = {
        new_token: previous_dict[prev_token]
        for prev_token, new_token in rename_dict.items()
    }
    return new_func, dico_to_string(func_dico)


def rename_tok(token: str, rename_dict: tp.Dict[str, str]) -> str:
    for prefix in OBFUSCATED_PREFIXES:
        # Replacing tokens with larger numbers first to avoid replacing parts of a token
        for match in sorted(re.findall(f"{prefix}\d+", token), reverse=True):
            assert match in rename_dict, f"{match} was not in rename dictionary"
            token = re.sub(f"{match}(?!\d)", rename_dict[match], token)
    return token


def read_dict(dico: str, separator: str = SEPARATOR) -> tp.Dict[str, str]:
    return dict(entry.strip().split(maxsplit=1) for entry in dico.split(separator))


def build_rename_dict(func: str) -> tp.Dict[str, str]:
    tokens = func.split()
    rename_dict = {}
    for prefix in OBFUSCATED_PREFIXES:
        prefix_count = 0
        for token in tokens:
            for match in re.findall(f"{prefix}\d+", token):
                if match not in rename_dict:
                    rename_dict[token] = f"{prefix}{prefix_count}"
                    prefix_count += 1
    return rename_dict


def replace_function_name(f: str, fname: str) -> str:
    return " ".join(["FUNC_0" if tok == fname else tok for tok in f.split(" ")])


def dico_to_string(dico: tp.Dict[str, str], separator: str = SEPARATOR) -> str:
    return separator.join(f"{k} {dico[k]}" for k in sorted(dico))
