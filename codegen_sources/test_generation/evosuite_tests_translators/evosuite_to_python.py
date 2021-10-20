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


class EvosuiteToPython(EvosuiteTranslator):
    def __init__(self):
        super().__init__()
        self.imports = "import numpy as np \nimport math\nfrom math import *\nimport collections\nfrom collections import *\nimport heapq\nimport itertools\nimport random\nimport sys\nimport unittest\n"
        self.remove_casting_null = {
            t: re.compile(r"%s\(null\)" % t)
            for t in ["int", "str", "float", "bool", "list"]
        }

    def translate(self, code):
        code = self.translate_class_method_name(code)
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
        code = self.method_name_regexp.sub(r"def test\1(self):", code)
        code = code.replace(
            f"public class {classname}_ESTest extends {classname}_ESTest_scaffolding "
            + "{",
            f"class {classname}(unittest.TestCase):",
        )

        code = self.replace_func_calls(classname, code)
        #         code = code.replace(f'{classname}.', "")
        return code

    def translation_wrapup(self, code):
        tests = code.split("@Test(timeout = ")[1:]
        for t in tests:
            if "f_filled" not in t:
                code = code.replace(t, "")
        # removing tests that don't call the method
        code = code.replace("}", "")
        codelines = [
            l
            for l in code.splitlines()
            if not l.startswith("import")
            and not l.startswith("@RunWith")
            and not l.startswith("  @Test(timeout =")
        ]
        for i, l in enumerate(codelines):
            if "*/" in l:
                break
        code = "\n".join(codelines[i + 1 :])
        code = "\n".join(
            [self.imports]
            + ["\n\n#TOFILL\n"]
            + [code]
            + ["\nif __name__ == '__main__':\n    unittest.main()"]
        )
        return code

    def replace_asserts(self, code):
        assert_args = self.get_asserts_arguments(code)
        for assert_name, arguments_list in assert_args.items():
            for args in arguments_list:
                #             print(assert_name, args, len(args))
                assert_string = f"{assert_name}({self.args_to_string(args)});"
                if assert_name == "assertTrue":
                    assert len(args) == 1, args
                    code = code.replace(assert_string, f"assert {args[0]}")
                elif assert_name == "assertFalse":
                    assert len(args) == 1, args
                    code = code.replace(assert_string, f"assert not ({args[0]})")
                elif (
                    assert_name == "assertEquals" or assert_name == "assertArrayEquals"
                ):
                    assert len(args) == 2 or len(args) == 3, args
                    if len(args) == 2:
                        code = code.replace(
                            assert_string, f"assert {args[0]} == {args[1]}"
                        )
                    if len(args) == 3:
                        code = code.replace(
                            assert_string,
                            f"assert abs({args[0]} - {args[1]}) <= {args[2]}",
                        )
                elif assert_name == "assertSame":
                    assert len(args) == 2, args
                    code = code.replace(assert_string, f"assert {args[0]} is {args[1]}")
                elif assert_name == "assertNotSame":
                    assert len(args) == 2, args
                    code = code.replace(
                        assert_string, f"assert {args[0]} is not {args[1]}"
                    )
                elif assert_name == "assertNull":
                    assert len(args) == 1, args
                    code = code.replace(assert_string, f"assert {args[0]} is None")
                elif assert_name == "assertNotNull":
                    assert len(args) == 1, args
                    code = code.replace(assert_string, f"assert {args[0]} is not None")
                else:
                    raise NotImplementedError(f"cannot translate {assert_name}")
        return code

    def translate_arrays(self, code):

        for t in self.java_simple_types:
            code = self.regexp_match_array_content_definition[t].sub(r"[\1]", code)
            code = self.regexp_match_array_definition_with_length[t].sub(
                r"\1 = [%s] * \2;" % self.get_default_value(t), code
            )
            code = self.regexp_match_array_length_getter[t].sub(r" len(\1)", code)

        for t, regexp in self.list_objects_definitions.items():
            code = regexp.sub(r"\1 = []", code)
        for t in self.java_simple_types:
            for regexp in self.regexp_match_list_definition[t].values():
                code = regexp.sub(r"[]", code)
        for t, regexp in self.regexp_match_add_to_list.items():
            code = regexp.sub(r"\1.append(", code)
        for t, regexp in self.regexp_match_list_contains.items():
            code = regexp.sub(r"\2 in \1", code)

        return code

    def translate_variable_definitions(self, code):
        for t, regexp in self.object_variable_definition.items():
            code = regexp.sub(r"\1 = \2", code)
        for t, regexp in self.primitive_variable_definition.items():
            code = regexp.sub(r"\1 = \2", code)

        return code

    def translate_type_casting(self, code):
        for t in ["short", "int", "long", "Integer", "Long", "Short"]:
            code = self.type_casting_regexp[t].sub(r"int(\1)", code)
        for t in ["boolean", "Boolean"]:
            code = self.type_casting_regexp[t].sub(r"bool(\1)", code)

        for t in ["float", "Float", "double", "Double"]:
            code = self.type_casting_regexp[t].sub(r"float(\1)", code)

        for t in ["String", "char", "Character"]:
            code = self.type_casting_regexp[t].sub(r"str(\1)", code)

        for t in self.java_arrays_regexp | self.java_list_objects:
            code = self.type_casting_regexp[t].sub(r"list(\1)", code)

        code = self.type_casting_regexp["Object"].sub(r"\1", code)

        for t, regexp in self.remove_casting_null.items():
            code = regexp.sub(r"None", code)
        return code

    def translate_equals(self, code):
        code = self.equals_regexp.sub(r" == (\1)", code)
        return code

    def translate_value_initializations(self, code):
        code = self.double_initialization_regexp.sub(r"\1\2\3", code)
        code = self.long_initialization_regexp.sub(r"\1\2\3", code)
        code = self.null_pointers_regexp.sub(r"\1None\2", code)

        return code
