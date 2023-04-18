import difflib
from pathlib import Path

import sys


root_folder = Path(__file__).parents[3]
sys.path.append(str(root_folder))
print(f"adding to path {root_folder}")

from codegen_sources.model.src.constants import EXT
from codegen_sources.IR_tools.utils_ir import (
    source_file_to_cleaned_IR,
    code_to_ir,
    ERROR_MESSAGE,
)

RESOURCES_PATH = Path(__file__).parent.joinpath("resources")


def diff_printer(lang1_content, lang2_content, lang1, lang2, split="\n"):
    d = difflib.Differ()
    if lang1_content != lang2_content:
        print(f"{lang1}:")
        print(lang1_content)
        print("#" * 50)
        print(f"{lang2}:")
        print(lang2_content)
        print("#" * 50)
        diff = d.compare(lang1_content.split(split), lang2_content.split(split))
        for line in diff:
            print(line)


def test_cpp_addition_function():
    input_filepath = RESOURCES_PATH.joinpath("cpp").joinpath("addition.cpp")
    clean_ir = get_single_element(
        source_file_to_cleaned_IR(
            input_filepath,
            "cpp",
            cannonize=False,
            work_dir=RESOURCES_PATH.joinpath("cpp").joinpath("addition"),
        )
    )
    assert "get_sum" in clean_ir
    print(clean_ir)


def test_cpp_max_function():
    input_filepath = RESOURCES_PATH.joinpath("cpp").joinpath("max.cpp")
    clean_ir = get_single_element(
        code_to_ir(
            open(input_filepath).read(),
            "cpp",
            cannonize=False,
            func_level=True,
            work_dir=RESOURCES_PATH.joinpath("cpp").joinpath("addition"),
        )
    )
    print(clean_ir)


def test_cpp_conditions_function():
    input_filepath = RESOURCES_PATH.joinpath("cpp").joinpath("conditions.cpp")
    clean_ir = get_single_element(
        source_file_to_cleaned_IR(
            input_filepath,
            "cpp",
            cannonize=False,
            work_dir=RESOURCES_PATH.joinpath("cpp").joinpath("conditions"),
        )
    )
    assert "f" in clean_ir
    print(clean_ir)


def test_cpp_for_sums_function():
    input_filepath = RESOURCES_PATH.joinpath("cpp").joinpath("for_sum.cpp")
    clean_ir = get_single_element(
        source_file_to_cleaned_IR(
            input_filepath,
            "cpp",
            cannonize=False,
            work_dir=RESOURCES_PATH.joinpath("cpp").joinpath("for_sum"),
        )
    )
    assert "sum" in clean_ir
    print(clean_ir)


def test_rust_addition_function():
    input_filepath = RESOURCES_PATH.joinpath("rust").joinpath("addition.rs")
    clean_ir = get_single_element(
        source_file_to_cleaned_IR(
            input_filepath,
            "rust",
            cannonize=False,
            work_dir=RESOURCES_PATH.joinpath("rust").joinpath("addition"),
        )
    )
    print(clean_ir)
    assert "get_sum" in clean_ir


def get_differences_irs(file_basename, lang1, lang2):
    lang1_file = RESOURCES_PATH.joinpath(lang1).joinpath(f"{file_basename}{EXT[lang1]}")
    lang2_file = RESOURCES_PATH.joinpath(lang2).joinpath(f"{file_basename}{EXT[lang2]}")
    lang1_content = open(lang1_file).read()
    lang2_content = open(lang2_file).read()

    clean_lang1_ir = get_single_element(
        code_to_ir(
            lang1_content,
            lang1,
            cannonize=False,
            func_level=True,
            work_dir=RESOURCES_PATH.joinpath(lang1)
            .joinpath("IR")
            .joinpath(file_basename + "_diff"),
        )
    )

    clean_lang2_ir = get_single_element(
        code_to_ir(
            lang2_content,
            lang2,
            cannonize=False,
            func_level=True,
            work_dir=RESOURCES_PATH.joinpath(lang2)
            .joinpath("IR")
            .joinpath(file_basename + "_diff"),
        )
    )
    diff_printer(clean_lang1_ir, clean_lang2_ir, lang1, lang2)


def test_get_differences_rust_cpp_addition():
    get_differences_irs("addition", "cpp", "rust")


def test_get_differences_rust_java_addition():
    get_differences_irs("addition", "cpp", "rust")


def test_get_differences_rust_cpp_conditions():
    get_differences_irs("conditions", "cpp", "rust")


def test_get_differences_cpp_java_addition():
    get_differences_irs("addition", "cpp", "java")


def test_get_differences_cpp_go_addition():
    get_differences_irs("addition", "cpp", "go")


def test_get_differences_cpp_java_for_sum():
    get_differences_irs("for_sum", "cpp", "java")


def test_get_differences_cpp_java_conditions():
    get_differences_irs("conditions", "cpp", "java")


def get_single_element(l):
    assert len(l) == 1
    return l[0]


def test_java_addition_function():
    input_code = open(RESOURCES_PATH.joinpath("java").joinpath("addition.java")).read()
    clean_ir = get_single_element(
        code_to_ir(
            input_code,
            "java",
            func_level=True,
            cannonize=False,
            work_dir=RESOURCES_PATH.joinpath("java").joinpath("addition"),
        )
    )
    print(clean_ir)
    assert "get_sum" in clean_ir, clean_ir


def test_java_func_level_function():
    input_code = """public static int kthgroupsum ( int k ) {
  return k * k * k ;
}"""
    clean_ir = get_single_element(
        code_to_ir(
            input_code,
            "java",
            func_level=True,
            cannonize=False,
            work_dir=RESOURCES_PATH.joinpath("java").joinpath("addition"),
            clean_dir=False,
        )
    )
    print(clean_ir)
    assert not clean_ir.startswith(ERROR_MESSAGE), clean_ir


def test_addition_template():
    input_filepath = RESOURCES_PATH.joinpath("cpp").joinpath("addition_template.cpp")
    clean_ir = source_file_to_cleaned_IR(
        input_filepath,
        "cpp",
        cannonize=False,
        work_dir=RESOURCES_PATH.joinpath("cpp").joinpath("addition_template"),
        verbose=1,
    )
    # assert len(clean_ir) == 2
    # assert "get_sum" in clean_ir
    for ir in clean_ir:
        print("#" * 10)
        print(ir)
    assert len(clean_ir) == 2


def test_java_function_level_no_issue_with_global_var():
    ex = """public static long f_gold ( int f , int d , int s ) {
      long mem [ ] [ ] = new long [ d + 1 ] [ s + 1 ] ;
      mem [ 0 ] [ 0 ] = 1 ;
      for ( int i = 1 ;
      i <= d ;
      i ++ ) {
        for ( int j = i ;
        j <= s ;
        j ++ ) {
          mem [ i ] [ j ] = mem [ i ] [ j - 1 ] + mem [ i - 1 ] [ j - 1 ] ;
          if ( j - f - 1 >= 0 ) mem [ i ] [ j ] -= mem [ i - 1 ] [ j - f - 1 ] ;
        }
      }
      return mem [ d ] [ s ] ;
    }"""
    clean_ir = code_to_ir(ex, "java", func_level=True, verbose=False)
    print(clean_ir[0])
    assert len(clean_ir) == 1
    assert not clean_ir[0].startswith("subprocess error:")


def test_go_function_level():
    ex = """func kthgroupsum ( k int ) int { return k * k * k}"""
    clean_ir = get_single_element(code_to_ir(ex, "go", func_level=True, verbose=False))
    print(clean_ir)
    assert not clean_ir.startswith("subprocess error:")


def test_rust_function_level_without_pub():
    ex = """fn kthgroupsum ( mut k : i32 ) -> i32 {
  return k * k * k ;
}"""
    clean_ir = get_single_element(
        code_to_ir(ex, "rust", func_level=True, verbose=False)
    )
    print(clean_ir)
    assert not clean_ir.startswith("subprocess error:")


def test_rust_function_level_with_pub():
    ex = """pub fn kthgroupsum ( mut k : i32 ) -> i32 {
  return k * k * k ;
}"""
    clean_ir = get_single_element(
        code_to_ir(ex, "rust", func_level=True, verbose=False)
    )
    print(clean_ir)
    assert not clean_ir.startswith("subprocess error:")
