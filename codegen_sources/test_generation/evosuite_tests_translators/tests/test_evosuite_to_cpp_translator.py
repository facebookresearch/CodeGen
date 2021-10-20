from .test_utils import read_inputs, translation_testing
from ..evosuite_to_cpp import EvosuiteToCpp


ARRAYS = ["integer_array_casting"]

JAVA_ARRAYS = ["java_list"]

TEST_STRINGS = ["strings", "strings_null_casting"]

TEST_FLOATS = ["floats", "doubles"]

translator = EvosuiteToCpp()


def test_array_translation():
    translations_list = [read_inputs(filename, "cpp") for filename in ARRAYS]
    translation_testing(translations_list, translator)


def test_lists_translation():
    translations_list = [read_inputs(filename, "cpp") for filename in JAVA_ARRAYS]
    translation_testing(translations_list, translator)


def test_floats():
    translations_list = [read_inputs(filename, "cpp") for filename in TEST_FLOATS]
    translation_testing(translations_list, translator)


def test_string_translation():
    translations_list = [read_inputs(filename, "cpp") for filename in TEST_STRINGS]
    translation_testing(translations_list, translator)


def test_different_object_name():
    translations_list = [
        read_inputs(filename, "cpp") for filename in ["different_object_name"]
    ]
    translation_testing(translations_list, translator)
