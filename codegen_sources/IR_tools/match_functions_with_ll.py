import argparse
import typing as tp
from pathlib import Path

from tqdm import tqdm

from codegen_sources.preprocessing.lang_processors import IRProcessor
from codegen_sources.IR_tools.utils_ir import (
    extract_all_ll_funcnames,
    get_lang_processor,
)


def source_path_to_funcpaths(source_path, lang):
    return list(
        Path(
            str(source_path.with_suffix("")).replace(f"/{lang}/", "/cleaned_IRs/")
        ).glob("*.ll")
    )


# def extract_all_ll_funcnames(s):
#     return [extract_ll_funcname(func_s) for func_s in s.split("define")[1:]]


# def extract_ll_funcname(s):
#     try:
#         return s.split("@")[1].split("(")[0]
#     except IndexError:
#         return ""


def signature_match(func_name, code_arguments, ll_func):

    ll_names = [
        name.replace('"', "").replace("'", "")
        for name in extract_all_ll_funcnames(ll_func)
    ]
    ll_names = [
        name
        for name in ll_names
        if name == func_name
        or name.split("::")[-1] == func_name
        or name.split("::")[-1] == func_name.split("::")[-1]
    ]
    for ll_name in ll_names:
        try:
            ll_arguments = ll_func.split(ll_name)[1].split(")")[0][1:].split(",")
            if len(ll_arguments) == len(code_arguments[0]):
                return True
        except KeyboardInterrupt:
            raise
        except:
            continue
        # Ideally should check the return type as well
        # ll_return_type = ll_func.split(ll_name)[0].splitlines()[-1].replace("@", "").strip().split()[-1]
    return False


def match_functions_with_ll(lang: str, output_path: str):
    lang_processor = get_lang_processor(lang)
    ir_processor = IRProcessor()
    print(f"Extracting for language {lang}")
    path = Path(f"/private/home/mszafraniec/codegen/IR/test_IR_generation_{lang}")
    # path = Path("/private/home/mszafraniec/codegen/IR/test_IR_generation_cpp")
    # path = Path("/private/home/mszafraniec/codegen/IR/test_IR_generation_rust/")
    path_ir_func = path.joinpath("cleaned_IRs")
    path_lang_folder = path.joinpath(lang)
    files_path = path.joinpath(lang)
    print("Computing list of files...")
    source_files = list(path_lang_folder.glob(f"chunk_*/*.{lang}"))  # todo: was chunk_*
    ll_funcs = []
    code_funcs = []
    for src_path in tqdm(source_files):
        ll_functions_paths = source_path_to_funcpaths(src_path, lang)
        if len(ll_functions_paths) == 0:
            continue
        try:
            with open(src_path, "r") as source_in:
                source_code = source_in.read()
            tokenized = lang_processor.tokenize_code(source_code)
            sa, cl = lang_processor.extract_functions(tokenized)
            extracted_functions = sa + cl

            function_names = [
                lang_processor.get_function_name(f) for f in extracted_functions
            ]
            longest_name_first = sorted(
                enumerate([fname for fname in function_names if fname != ""]),
                key=lambda x: len(x[1]),
            )[::-1]
            function_names = [name for i, name in longest_name_first if name != ""]
            extracted_functions = [
                extracted_functions[i] for i, e in longest_name_first
            ]
            ll_func_names: tp.List[str] = []
            corresponding_ll_funcs: tp.List[tp.List[tp.Any]] = [
                [] for _ in function_names
            ]
            assert (
                len(function_names)
                == len(extracted_functions)
                == len(corresponding_ll_funcs)
            )
            for ll_fpath in ll_functions_paths:
                with open(ll_fpath, "r") as ll_in:
                    ll_func = ll_in.read()
                ll_fnames = [
                    name.replace('"', "").replace("'", "")
                    for name in extract_all_ll_funcnames(ll_func)
                ]
                for i, code_name in enumerate(function_names):
                    if any(
                        [
                            ll_name == code_name
                            or ll_name.split("::")[-1] == code_name
                            or ll_name.split("::")[-1] == code_name.split("::")[-1]
                            or ll_name.split(".")[-1] == code_name
                            for ll_name in ll_fnames
                        ]
                    ):
                        corresponding_ll_funcs[i].append(ll_func)
            code_funcs.append(extracted_functions)
            ll_funcs.append(corresponding_ll_funcs)
        except KeyboardInterrupt:
            raise
        except RecursionError:
            continue
        except Exception as e:
            print(f"Ignoring exception {e}")
            continue

    assert len(code_funcs) == len(ll_funcs)

    parallel_examples = []
    present_ll = 0
    missing_ll = 0
    several_examples = 0
    several_examples_fixed = 0
    several_examples_becomes_0 = 0
    several_examples_remain = 0
    for code, ll in zip(code_funcs, ll_funcs):
        assert len(code) == len(ll)
        for func, ll_functions in zip(code, ll):
            if len(ll_functions) == 0:
                missing_ll += 1
                continue
            present_ll += 1
            if len(ll_functions) > 1:
                # ll_functions = sorted(ll_functions, key=lambda x: len(extract_all_ll_funcnames(ll_func)[0].split("::")[-1]))

                several_examples += 1
                func_name = lang_processor.get_function_name(func)
                code_arguments = lang_processor.extract_arguments(func)
                ll_functions = [
                    ll_func
                    for ll_func in ll_functions
                    if signature_match(func_name, code_arguments, ll_func)
                ]
                if len(ll_functions) == 1:
                    several_examples_fixed += 1
                elif len(ll_functions) == 0:
                    several_examples_becomes_0 += 1
                    continue
                elif len(ll_functions) > 1:
                    several_examples_remain += 1
                    continue

            parallel_examples.append((func, ll_functions[0]))

    print(
        f"Present ll: {present_ll}\nmissing ll {missing_ll}\nll with several examples {several_examples}"
        f"\nfixed several examples {several_examples_fixed}\n"
        f"remain several examples {several_examples_remain}\n"
        f"several examples becomes 0: {several_examples_becomes_0}"
    )
    print(f"{len(parallel_examples)} parallel function / ll examples")

    output_folder = Path(output_path)
    output_folder.mkdir(exist_ok=True)
    output_path_ir = output_folder.joinpath(f"{lang}.all.ir_func.tok")
    output_path_code = output_folder.joinpath(f"{lang}.all.func.tok")
    output_ir = open(output_path_ir, "w", errors="replace")
    output_code = open(output_path_code, "w", errors="replace")
    for func_code, func_ll in parallel_examples:
        output_code.write(func_code)
        output_code.write("\n")

        output_ir.write(" ".join(ir_processor.tokenize_code(func_ll)))
        output_ir.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Command-line Arguments")
    parser.add_argument(
        "--lang",
        type=str,
        default=None,
        action="store",
        help="The language of the input",
    )
    parser.add_argument(
        "--output_path",
        default=None,
        action="store",
        help="The output dataset path. For instance /private/home/broz/datasets/CodeGen/data/2021_09_08_cleaned_ir_data_with_Oz_cpp_rust_java",
    )
    args = parser.parse_args()
    match_functions_with_ll(args.lang, args.output_path)
