# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
# Translate sentences from the input stream.
# The model will be faster is sentences are sorted by length.
# Input sentences must have the same tokenization and BPE codes than the ones used in the model.
#


import re

from .evosuite_translator import EvosuiteTranslator


class EvosuiteToCpp(EvosuiteTranslator):
    def __init__(self):
        super().__init__()
        self.imports = """#include <iostream>
#include <cstdlib>
#include <string>
#include <vector>
#include <fstream>
#include <iomanip>
#include <bits/stdc++.h>
#include "gtest/gtest.h"
#include "gmock/gmock.h"

using namespace std;
"""
        self.cpp_tests_main = """int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}"""
        self.java_standard_types_translations = {
            "Double": "double",
            "Float": "float",
            "String": "string",
            "Integer": "int",
            "Boolean": "bool",
            "boolean": "bool",
            "byte": "unsigned char",
            "Byte": "unsigned char",
            "Long": "long",
            "Short": "short",
            "Character": "char",
        }
        self.cpp_supported_types = list(
            self.java_standard_types_translations.values()
        ) + [f"{t}\*" for t in self.java_standard_types_translations.values()]
        # + [f"vector\<{t}\>" for t in self.java_standard_types_translations.values()]
        self.remove_casting_null = {
            t: re.compile(r"\(%s\)[ ]*null" % t) for t in self.cpp_supported_types
        }

    def translate(self, code):
        code = self.translate_class_method_name(code)
        code = code.replace("[]", "*")
        code = self.replace_asserts(code)
        code = self.translate_arrays(code)
        code = self.translate_variable_definitions(code)
        code = self.translate_type_casting(code)
        code = self.translate_equals(code)
        code = self.translate_value_initializations(code)
        code = self.translation_wrapup(code)
        return code

    def translate_class_method_name(self, code):
        assert "_ESTest" in code, code
        classname = code.split("_ESTest")[0].split()[-1].strip()
        #         print(classname)
        code = self.method_name_regexp.sub(r"TEST(EvoSuiteTest, test\1){", code)
        code = code.replace(
            f"public class {classname}_ESTest extends {classname}_ESTest_scaffolding "
            + "{",
            "",
        )
        code = self.replace_func_calls(classname, code)
        r = f"([{classname[0].lower()}, {classname[0]}]{classname[1:]}(0|1|_0)?)"
        code = re.sub(r + r"\s*" + r + r"\s*=\s*new\s*" + r + r"\s*\(.*\);", "", code)

        return code

    def translation_wrapup(self, code):
        tests = code.split("@Test(timeout = ")[1:]
        for t in tests:
            if "f_filled" not in t:
                code = code.replace(t, "")
        code = code.replace("  @Test(timeout = 4000)\n", "")
        code_lines = code.splitlines()

        code_lines = [
            l
            for l in code_lines
            if not l.startswith("import")
            and not l.startswith("@RunWith")
            and not l.startswith("  @Test(timeout =")
            and not l.startswith("      System.setCurrentTimeMillis(")
        ]
        assert len(code_lines) > 0, "input to translation_wrapup is empty"

        for i, l in enumerate(code_lines):
            if "*/" in l:
                break
        code_lines = code_lines[i + 1 :]
        return "\n".join(
            [self.imports]
            + ["\n", "//TOFILL"]
            + code_lines
            + ["\n"]
            + [self.cpp_tests_main]
        )

    def replace_asserts(self, code):
        assert_args = self.get_asserts_arguments(code)
        assert_that_num = 0
        for assert_name, arguments_list in assert_args.items():
            for args in arguments_list:
                #             print(assert_name, args, len(args))
                assert_string = f"{assert_name}({self.args_to_string(args)});"
                if assert_name == "assertTrue":
                    assert len(args) == 1, args
                    code = code.replace(assert_string, f"ASSERT_TRUE ({args[0]});")
                elif assert_name == "assertFalse":
                    assert len(args) == 1, args
                    code = code.replace(assert_string, f"ASSERT_FALSE ({args[0]});")
                elif assert_name == "assertEquals":
                    assert len(args) == 2 or len(args) == 3, args
                    if len(args) == 2:
                        code = code.replace(
                            assert_string, f"ASSERT_EQ ({args[0]}, {args[1]});",
                        )
                    if len(args) == 3:
                        code = code.replace(
                            assert_string,
                            f"ASSERT_NEAR ({args[0]},{args[1]},{args[2]});",
                        )
                elif assert_name == "assertArrayEquals":
                    if args[0].startswith("new "):
                        args[0] = re.sub(
                            r"new\s*(.+)\*",
                            f"vector<\g<1>> assert_array{assert_that_num} =",
                            args[0],
                        )
                        code = code.replace(
                            assert_string,
                            f"{args[0]};\nASSERT_THAT(assert_array{assert_that_num}, ::testing::ContainerEq({args[1]}));",
                        )
                        assert_that_num += 1
                    else:
                        code = code.replace(
                            assert_string,
                            f"ASSERT_THAT({args[0]}, ::testing::ContainerEq({args[1]}));",
                        )
                elif assert_name == "assertSame":
                    assert len(args) == 2, args
                    code = code.replace(
                        assert_string, f"ASSERT_EQ(*{args[0]}, *{args[1]});",
                    )
                elif assert_name == "assertNotSame":
                    assert len(args) == 2, args
                    code = code.replace(
                        assert_string, f"ASSERT_NE(*{args[0]}, *{args[1]});",
                    )
                elif assert_name == "assertNull":
                    assert len(args) == 1, args
                    code = code.replace(
                        assert_string,
                        "",
                        # assert_string, f"ASSERT_EQ ({args[0]}, nullptr);",
                    )
                elif assert_name == "assertNotNull":
                    assert len(args) == 1, args
                    code = code.replace(
                        assert_string,
                        "",
                        # assert_string, f"ASSERT_NE ({args[0]}, nullptr);",
                    )
                else:
                    raise NotImplementedError(f"cannot translate {assert_name}")

        code = code.strip()
        c = "".join(code.split())
        if len(c) >= 2 and c[-2:] == "}}":
            code = code[:-1]
        return code

    def translate_arrays(self, code):
        code = code.replace("ArrayList", "vector")
        code = re.sub(f" = new vector<" + r".+" + ">\(\);", ";", code)

        # code = re.sub(
        #     r"(\s*)(.+)\* (.+) = new\s*(.+)\[(.*)\];",
        #     f"\g<1>vector<\g<2>> \g<3>(\g<5>);",
        #     code,
        # )

        # for t in self.java_simple_types:
        #     code = self.regexp_match_array_content_definition[t].sub(
        #         r"// C++ array with elements [\1]", code
        #     )
        #     code = self.regexp_match_array_definition_with_length[t].sub(
        #         r"// C++ array definition with name \1 and \2 elements of default value %s;"
        #         % self.get_default_value(t),
        #         code,
        #     )
        #     code = self.regexp_match_array_length_getter[t].sub(
        #         r"// C++ to get length of array \1", code
        #     )

        for t, regexp in self.list_objects_definitions.items():
            pass
        for t in self.java_simple_types:
            for regexp in self.regexp_match_list_definition[t].values():
                # code = regexp.sub(r"[]", code)
                pass
        for t, regexp in self.regexp_match_add_to_list.items():
            # code = regexp.sub(r'\1.append(', code)
            pass
        for t, regexp in self.regexp_match_list_contains.items():
            # code = regexp.sub(r'\2 in \1', code)
            pass
        return code

    def translate_variable_definitions(self, code):
        for t, regexp in self.object_variable_definition.items():
            translated_type = self.java_standard_types_translations[t]
            code = regexp.sub(translated_type + r" \1 = \2;", code)
        for t, regexp in self.primitive_variable_definition.items():
            # no need to translate
            pass
        for t, translated_type in self.java_standard_types_translations.items():
            code = code.replace(t, translated_type)
        return code

    def translate_type_casting(self, code):
        for t in self.java_standard_types:
            translated_type = self.java_standard_types_translations[t]
            code = self.type_casting_regexp[t].sub(
                f"({translated_type}) " + r"\1", code
            )

        code = self.type_casting_regexp["Object"].sub(r"\1", code)

        # for t in self.java_arrays_regexp | self.java_list_objects:
        #     code = self.type_casting_regexp[t].sub(r"list(\1)", code)
        #
        # code = self.type_casting_regexp[t].sub(r"\1", code)
        #
        for t, regexp in self.remove_casting_null.items():
            code = regexp.sub(r"NULL", code)
        return code

    def translate_equals(self, code):
        code = self.equals_regexp.sub(r" == (\1)", code)
        return code

    def translate_value_initializations(self, code):
        # Translate null pointer to C++, it is NULL
        code = self.null_pointers_regexp.sub(r"\1NULL\2", code)

        return code
