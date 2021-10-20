from .test_utils import read_inputs, translation_testing
from ..evosuite_to_python import EvosuiteToPython


ARRAYS = ["integer_array_test", "integer_array_casting"]

JAVA_ARRAYS = ["java_list"]

TEST_STRINGS = ["strings", "strings_null_casting"]

TEST_FLOATS = ["floats", "doubles"]

translator = EvosuiteToPython()


def test_array_translation():
    translations_list = [read_inputs(filename, "python") for filename in ARRAYS]
    translation_testing(translations_list, translator, True)


def test_lists_translation():
    translations_list = [read_inputs(filename, "python") for filename in JAVA_ARRAYS]
    translation_testing(translations_list, translator, True)


def test_floats():
    translations_list = [read_inputs(filename, "python") for filename in TEST_FLOATS]
    translation_testing(translations_list, translator, True)


def test_string_translation():
    translations_list = [read_inputs(filename, "python") for filename in TEST_STRINGS]
    translation_testing(translations_list, translator, True)
