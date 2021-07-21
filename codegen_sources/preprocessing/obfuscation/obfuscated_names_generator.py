# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from enum import Enum


class ObfuscatedNameType(Enum):
    VARIABLE = "VAR"
    FUNCTION = "FUNC"
    CLASS = "CLASS"


class ObfuscatedNamesGenerator:
    def __init__(self, same_name_overloaded_func=True):
        self.same_name_overloaded_func = same_name_overloaded_func
        self.obfuscation_dict = {}
        for var_type in ObfuscatedNameType:
            self.obfuscation_dict[var_type] = {}
        self.funcnames_mapping = {}
        self.attributes_mappings = {}

    def get_new_name(self, varname, var_type, isAttribute=False):
        var_index = len(self.obfuscation_dict[var_type])
        if (
            var_type is ObfuscatedNameType.FUNCTION
            and self.function_is_obfuscated(varname)
            and self.same_name_overloaded_func
        ):
            return self.funcnames_mapping[varname]
        if isAttribute and varname in self.attributes_mappings:
            return self.attributes_mappings[varname]
        obfuscated_name = f"{var_type.value}_{var_index}"
        self.obfuscation_dict[var_type][obfuscated_name] = varname
        if var_type is ObfuscatedNameType.FUNCTION and self.same_name_overloaded_func:
            self.funcnames_mapping[varname] = obfuscated_name
        if isAttribute:
            self.attributes_mappings[varname] = obfuscated_name
        return obfuscated_name

    def get_dictionary(self):
        return {k: v for d in self.obfuscation_dict.values() for k, v in d.items()}

    def function_is_obfuscated(self, varname):
        return varname in self.funcnames_mapping
