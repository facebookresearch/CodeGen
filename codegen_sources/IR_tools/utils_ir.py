# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import errno
import math
import os
import re
import signal
import subprocess
import time
from functools import partial, wraps
from logging import getLogger
from pathlib import Path

import numpy as np
import uuid

import shutil

from codegen_sources.code_runners.code_runner import RUN_ROOT_DIR
from codegen_sources.code_runners.utils import GO_IMPORTS_PATH
from codegen_sources.model.src.utils import get_java_bin_path
from codegen_sources.preprocessing.lang_processors import LangProcessor

DEFAULT_IR_WORKDIR = RUN_ROOT_DIR.joinpath("ir_generation/tmp_tests_folder")

ERROR_MESSAGE = "subprocess error:"

CPP_TO_IR_COMMAND = "clang++ -c -emit-llvm -S -g1 -O0 {} -o {} -std=c++17 -Xclang -disable-O0-optnone -Wno-narrowing"
RUST_TO_IR_COMMAND = "rustc -C target-feature=-crt-static -C opt-level=z {} --crate-type={} --emit=llvm-ir -C debuginfo=1 -o {}"
JAVA_TO_IR_COMMAND = (
    'export PATH="{}:$PATH"; {}bin/jlangc -cp {}jdk/out/classes {} -d {}'
)
GO_TO_IR_COMMAND = "llvm-goc -g -O0 -S -emit-llvm {} -o {}"

LANG_IMPORTS = {
    "cpp": """#include <iostream>
#include <cstdlib>
#include <string>
#include <vector>
#include <fstream>
#include <iomanip>
#include <bits/stdc++.h>
using namespace std;""",
    "java": """import java.util. *;
import java.lang.*;
""",
    "python": r"import numpy as np \nimport math\nfrom math import *\nimport collections\nfrom collections import *\nimport heapq\nimport itertools\nimport random\nimport sys\n\n",
    "go": """package main
    func min(x int, y int) int {
	if x < y {
		return x
	}
	return y
}
func max(x int, y int) int {
	if x > y {
		return x
	}
	return y
}""",
    "rust": """use std :: io :: { stdin , BufRead , BufReader } ;
    use std::cmp::max;
    use std::cmp::min;
    """,
}
logger = getLogger()


class TimeoutError(BaseException):
    pass


# From https://github.com/glample/ASMR/blob/master/src/utils.py
def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(repeat_id, signum, frame):
            signal.signal(signal.SIGALRM, partial(_handle_timeout, repeat_id + 1))
            signal.alarm(seconds)
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            old_signal = signal.signal(signal.SIGALRM, partial(_handle_timeout, 0))
            old_time_left = signal.alarm(seconds)
            assert type(old_time_left) is int and old_time_left >= 0
            if 0 < old_time_left < seconds:  # do not exceed previous timer
                signal.alarm(old_time_left)
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
            finally:
                if old_time_left == 0:
                    signal.alarm(0)
                else:
                    sub = time.time() - start_time
                    signal.signal(signal.SIGALRM, old_signal)
                    signal.alarm(max(0, math.ceil(old_time_left - sub)))
            return result

        return wraps(func)(wrapper)

    return decorator


def get_lang_processor(lang):
    return LangProcessor.processors[lang]()


@timeout(120)
def demangle_names_cpp(full_file, verbose=False, timeout=120):
    from codegen_sources.external_paths import LLVM_13_PATH

    names_to_demangle = np.unique(re.findall(r"(?<=@)_\w+", full_file))
    demangled = [
        subprocess.check_output(
            LLVM_13_PATH + f"llvm-cxxfilt {el}", shell=True, stderr=subprocess.DEVNULL
        )
        .decode()
        .strip()
        for el in names_to_demangle
    ]
    demangled = [re.sub(r"\(.*\)", "", el) for el in demangled]  # Remove types

    pairs = list(zip(names_to_demangle, demangled))
    for old, new in pairs:
        full_file = re.sub(rf"(?<=@){old}(?=\W)", f'"{new}"', full_file)

    return full_file


@timeout(120)
def demangle_names_rust(full_file):
    from codegen_sources.external_paths import CARGO_PATH

    names_to_demangle = np.unique(re.findall(r"(?<=@)_\w+", full_file))
    demangled = [
        subprocess.check_output(CARGO_PATH + f"rustfilt {el}", shell=True)
        .decode()
        .strip()
        for el in names_to_demangle
    ]

    pairs = list(zip(names_to_demangle, demangled))
    for old, new in pairs:
        new = new.split("::", 1)[-1]
        full_file = re.sub(rf"(?<=@){old}(?=\W)", f'"{new}"', full_file)

    return full_file


def demangle_names_jlang_name_only(mangled_name):

    # From https://github.com/polyglot-compiler/JLang/blob/4cc09d966e2bdae814f21792811c34af589c8f77/compiler/src/jlang/util/JLangMangler.java

    POLYGLOT_PREFIX = "Polyglot_"
    UNDERSCORE_ESCAPE = "_1"

    if not mangled_name.startswith(POLYGLOT_PREFIX):
        return mangled_name

    mangled_name = mangled_name.replace(POLYGLOT_PREFIX, "", 1)
    mangled_name = mangled_name.replace(UNDERSCORE_ESCAPE, "~")
    class_name, func_name, _, args_mangled = mangled_name.split("_", 3)
    class_name = class_name.replace("~", "_")
    func_name = func_name.replace("~", "_")

    return f"{class_name}.{func_name}"


@timeout(120)
def demangle_names_java(full_file):
    POLYGLOT_PREFIX = "Polyglot_"
    names_to_demangle = np.unique(
        [
            el.rsplit(" ", 1)[1][1:]
            for el in re.findall(
                rf"(?<=\n)define .*? @{POLYGLOT_PREFIX}\w+", "\n" + full_file
            )
        ]
    )
    demangled = [demangle_names_jlang_name_only(el).strip() for el in names_to_demangle]

    pairs = list(zip(names_to_demangle, demangled))
    for old, new in pairs:
        full_file = re.sub(rf"(?<=@){old}(?=\W)", f'"{new}"', full_file)

    #     return full_file
    return trim_java_file(full_file)


@timeout(120)
def demangle_names_go(full_file):
    GO_PREFIX = "go_0"
    names_to_demangle = set(
        [
            el.rsplit(" ", 1)[1][1:]
            for el in re.findall(
                rf"(?<=\n)define .*? @{GO_PREFIX}[\w.]+", "\n" + full_file
            )
        ]
    )
    demangled = [
        name.replace("go_0", "", 1).replace("__", "_") for name in names_to_demangle
    ]
    demangled = [
        name.rsplit(".", 1)[1] for name in names_to_demangle
    ]  # Would return package.func

    pairs = list(zip(names_to_demangle, demangled))
    for old, new in pairs:
        full_file = re.sub(rf"(?<=@){old}(?=\W)", f'"{new}"', full_file)

    return full_file


def get_demangle_func(lang):
    if lang == "rust":
        return demangle_names_rust
    elif lang == "java":
        return demangle_names_java
    elif lang == "go":
        return demangle_names_go
    else:
        assert lang == "cpp"
        return demangle_names_cpp


def multiple_replace(substitutions, string):
    match_dict = {
        re.sub(r"\(.*?\)", "", k, flags=re.DOTALL): v for k, v in substitutions.items()
    }

    def rep(match):
        what_matched = match.group()
        return match_dict.get(what_matched, what_matched)

    return re.sub("|".join(substitutions.keys()), rep, string)


def remove_semicolumn_lines(full_file):
    return re.sub("\n;.*(?=\n)", "", "\n" + full_file).strip()


@timeout(120)
def clean_file(full_file):
    # Remove !tbaa ...
    full_file = re.sub(", !tbaa ![0-9]+", "", full_file)
    # Remove beginning of file
    full_file = full_file.split("\n\n", 1)[1]
    # Remove end of file (attributes etc)
    full_file = full_file.rsplit("\n\n", 3)[0]
    # Rename blocks
    full_file = rename_blocks(full_file)
    # Remove semicolumn lines
    full_file = remove_semicolumn_lines(full_file)

    return full_file


def rename_blocks(full_file):
    # Rename all blocks (entry, start, if.then... in bb1, bb2, ...)
    all_blocks = [
        el[:-1] for el in re.findall(r"(?<=\n)\w\S+", full_file) if el.endswith(":")
    ]
    replace_dict = {
        **{rf"(?<=\n){el}(?=\W)": f"bb{i + 1}" for i, el in enumerate(all_blocks)},
        **{rf"%{el}(?=\W)": f"%bb{i + 1}" for i, el in enumerate(all_blocks)},
    }
    full_file = multiple_replace(replace_dict, full_file)
    return full_file


def extract_lang_IR(lang_file, output_path, lang, verbose=False, timeout=120):
    lang_dict = {
        "cpp": extract_cpp_IR,
        "go": extract_go_IR,
        "java": extract_java_IR,
        "rust": extract_rust_IR,
    }
    return lang_dict[lang](lang_file, output_path, verbose=verbose, timeout=timeout)


def extract_cpp_IR(cpp_file, output_path, verbose=False, timeout=120):
    from codegen_sources.external_paths import LLVM_13_PATH

    cmd = LLVM_13_PATH + "/" + CPP_TO_IR_COMMAND.format(cpp_file, output_path)
    subprocess.check_call(
        cmd,
        shell=True,
        timeout=timeout,
        stderr=None if verbose else subprocess.DEVNULL,
        stdout=None if verbose else subprocess.DEVNULL,
    )


def extract_rust_IR_base(rust_file, output_path, crate, verbose=False, timeout=120):
    from codegen_sources.external_paths import CARGO_PATH, LLVM_13_PATH

    EXPORT_PATH = f"export PATH={LLVM_13_PATH}:$PATH; "
    cmd = (
        EXPORT_PATH
        + CARGO_PATH
        + "/"
        + RUST_TO_IR_COMMAND.format(rust_file, crate, output_path)
    )
    subprocess.check_call(
        cmd,
        shell=True,
        timeout=timeout,
        stderr=None if verbose else subprocess.DEVNULL,
        stdout=None if verbose else subprocess.DEVNULL,
    )


def extract_rust_IR(rust_file, output_path, verbose=False, timeout=120):
    try:
        # Timeout in seconds
        extract_rust_IR_base(
            rust_file, output_path, crate="bin", verbose=verbose, timeout=timeout
        )
        if verbose:
            print(f"{rust_file} extracted with bin", flush=True)
    except subprocess.CalledProcessError:
        # Timeout in seconds
        extract_rust_IR_base(
            rust_file, output_path, crate="dylib", verbose=verbose, timeout=timeout
        )
        if verbose:
            print(f"{rust_file} extracted with dylib", flush=True)


def extract_java_IR(java_file, output_path, verbose=False, timeout=120):
    from codegen_sources.external_paths import JLANG_PATH, LLVM_5_PATH, LLVM_13_PATH

    # We remove the "package" lines...
    full_java_file = open(java_file).read()
    full_java_file = re.sub(r"(\n|^)package \S+;(\n|$)", "", full_java_file)
    with open(java_file, "w") as f:
        f.write(full_java_file)

    cmd = JAVA_TO_IR_COMMAND.format(
        get_java_bin_path(),
        JLANG_PATH,
        JLANG_PATH,
        java_file,
        os.path.dirname(output_path),
    )
    output_channel = None if verbose else subprocess.DEVNULL
    subprocess.check_call(
        cmd, shell=True, timeout=timeout, stderr=output_channel, stdout=output_channel
    )
    # JLang produces LLVM v5, which is not comparible with LLVM v14
    # To make the conversion, we do LLVM v5 -> Bitcode -> LLVM v14, as Bitcode
    # doesn't change between versions of LLVM
    subprocess.check_call(
        f"{LLVM_5_PATH}llvm-as {output_path}; rm {output_path}",
        shell=True,
        timeout=timeout,
        stderr=output_channel,
        stdout=output_channel,
    )
    file_wo_ext = str(output_path)[:-3]
    subprocess.check_call(
        f"{LLVM_13_PATH}llvm-dis {file_wo_ext}.bc; rm {file_wo_ext}.bc",
        shell=True,
        timeout=timeout,
        stderr=output_channel,
        stdout=output_channel,
    )


def extract_go_IR(go_file, output_path, verbose=False, timeout=120):
    from codegen_sources.external_paths import GOLLVM_PATH

    output = None if verbose else subprocess.DEVNULL
    _ = subprocess.check_call(
        f"{GO_IMPORTS_PATH} -w {go_file}",
        stdout=output,
        stderr=output,
        shell=True,
        executable="/bin/bash",
    )
    subprocess.check_call(
        GOLLVM_PATH + GO_TO_IR_COMMAND.format(go_file, output_path),
        shell=True,
        timeout=timeout,
        stderr=output,
        stdout=output,
    )


def find_globals(ll_file):
    with open(ll_file) as f:
        globs = re.findall("(?<=\n@).*?(?= =)", "\n" + f.read())
    return globs


@timeout(120)
def extract_function(
    funcname, input_ll_file, output_ll_file, verbose=False, timeout=120
):
    from codegen_sources.external_paths import LLVM_13_PATH

    # --keep-const-init would keep ALL the globals, not only the ones we need
    extract_command = (  # This says which globs we need but does not extract them
        LLVM_13_PATH + "llvm-extract --func={} {} -S -o {}"
    )
    subprocess.check_call(
        extract_command.format(funcname, input_ll_file, output_ll_file),
        shell=True,
        stderr=None if verbose else subprocess.DEVNULL,
        stdout=None if verbose else subprocess.DEVNULL,
        timeout=timeout,
    )

    globs = find_globals(output_ll_file)
    init_globs = find_globals(input_ll_file)
    globs = [g for g in globs if g in init_globs]
    extract_w_globs_command = LLVM_13_PATH + "llvm-extract {} --func={} {} -S -o {}"
    subprocess.check_call(
        extract_w_globs_command.format(
            " ".join([f"--glob={el}" for el in globs]),
            funcname,
            input_ll_file,
            output_ll_file,
        ),
        shell=True,
        stderr=None if verbose else subprocess.DEVNULL,
        stdout=None if verbose else subprocess.DEVNULL,
        timeout=timeout,
    )


def clean_mangled_funcs(mangled_funcs, full_file):
    file_glob_variables = re.findall("(?<=@).*(?= =)", full_file)
    mangled_funcs = np.setdiff1d(
        mangled_funcs, file_glob_variables
    )  # The funcs that are global variables are aliases
    mangled_funcs = [
        el.split("@@")[0] for el in mangled_funcs
    ]  # sometimes things like @@0 get added to the func names ?
    mangled_funcs = [el.replace("$", r"\$") for el in mangled_funcs]
    mangled_funcs = [el for el in mangled_funcs if "\\" not in el]
    return mangled_funcs


def trim_java_file(full_java_file):
    full_java_file = re.sub('(^|\n)%"?class.java_lang.*', "", full_java_file)
    full_java_file = re.sub("(^|\n)%cdv_ty.*", "", full_java_file)

    words_to_remove = [
        "jni_JNIEnv",
        "getGlobalMutexObject",
        "jni_MonitorEnter",
        "jni_MonitorExit",
    ]
    for w in words_to_remove:
        full_java_file = re.sub(f".*{w}.*\n?", "", full_java_file)

    return full_java_file.strip()


def get_funcnames(code, lang_processor):
    sa, cl = lang_processor.extract_functions(lang_processor.tokenize_code(code))
    funcs = sa + cl
    return [lang_processor.get_function_name(f) for f in funcs]


@timeout(120)
def _split_names(name, lang):
    split = name.split('name: "')[1].split('"')[0].split("(")[0]

    if lang == "java":
        split = split.split("#")[-1]
    elif lang == "go":
        split = split.rsplit(".")[-1]

    return split


def extract_relevant_functions(llfile, original_file_name, lang_processor, lang):
    """
    Extract only functions defined in the original cpp file from the debug info
    original_file_name example: `cpp_from_json_0_line_1096_Oz.cpp`
    """
    debug = llfile.rsplit("\n\n", 1)[1]
    files = re.findall("(?<=!).*!DIFile.*filename:.*", debug)
    complete_file_names = [
        re.search('(?<=filename: ").*?(?=")', el).group() for el in files
    ]
    directory_names = [
        re.search('(?<=directory: ").*?(?=")', el).group() for el in files
    ]
    complete_file_names = [
        os.path.join(directory_names[i], complete_file_names[i])
        if directory_names[i]
        else complete_file_names[i]
        for i in range(len(complete_file_names))
    ]

    file_names = [os.path.basename(el) for el in complete_file_names]
    original_fn_noext = os.path.splitext(os.path.basename(original_file_name))[0]
    relevant_files = [os.path.splitext(el)[0] == original_fn_noext for el in file_names]

    # The exact original file name is the longest one because it contains the full path
    complete_original_file_name = sorted(
        [el for i, el in enumerate(complete_file_names) if relevant_files[i]], key=len
    )[-1]
    original_file = open(complete_original_file_name, "r", errors="ignore").read()
    original_functions = set(
        get_funcnames(original_file, lang_processor=lang_processor)
    )

    file_ids = [el.split(" ", 1)[0] for i, el in enumerate(files) if relevant_files[i]]

    subprograms = re.findall(".*!DISubprogram.*", debug)
    relevant_subprograms = [
        el
        for fid in file_ids
        for el in subprograms
        if f"file: !{fid}," in el
        and 'name: "' in el
        and _split_names(el, lang) in original_functions
    ]

    indices_to_keep = [el.split(" ", 1)[0] for el in relevant_subprograms]
    relevant_defines = sum(
        [re.findall(f".* !dbg {itk} " + "{", llfile) for itk in indices_to_keep], []
    )

    mangled_funcs = extract_all_ll_funcnames("\n".join([""] + relevant_defines))
    return clean_mangled_funcs(mangled_funcs, llfile)


def extract_all_ll_funcnames(full_file):
    return [
        el.split()[-1][1:]
        for el in re.findall(r"(?<=\ndefine ).*? @.*?(?=\()", "\n" + full_file)
    ]


def source_file_to_cleaned_IR(
    source_path,
    lang,
    work_dir=DEFAULT_IR_WORKDIR,
    verbose=False,
    timeout=120,
    clean_dir=True,
):
    hash_value = uuid.uuid4()
    work_dir_full = Path(work_dir).joinpath(f"{str(int(time.time()))}_{hash_value}")
    work_dir_full.mkdir(parents=True, exist_ok=True)
    if verbose:
        print("Work dir:", work_dir_full)

    ir_path_file = work_dir_full.joinpath(
        os.path.splitext(os.path.basename(source_path))[0]
    ).with_suffix(".ll")
    extract_lang_IR(source_path, ir_path_file, lang, verbose, timeout)
    if verbose:
        with open(ir_path_file, "r") as f:
            print(f"Full IR:\n{f.read()}")

    lang_processor = get_lang_processor(lang)

    full_file = open(ir_path_file, "r").read()
    mangled_funcs = extract_relevant_functions(
        full_file, source_path, lang_processor, lang
    )

    original_file_funcs_dir = os.path.join(work_dir_full, "ll_functions")
    os.makedirs(original_file_funcs_dir, exist_ok=True)

    all_output_funcs = []
    for n_func, func in enumerate(mangled_funcs):
        output_ll_file = os.path.join(original_file_funcs_dir, f"{n_func}.ll")
        extract_function(func, ir_path_file, output_ll_file)

        func_names = extract_all_ll_funcnames(open(output_ll_file, "r").read())
        assert len(func_names) == 1  # Should be only one

        full_file = open(output_ll_file, "r").read()
        demangle_fn = get_demangle_func(lang)
        all_output_funcs.append(demangle_fn(clean_file(full_file)))

    if clean_dir and work_dir_full.is_dir():
        shutil.rmtree(work_dir_full)
    return all_output_funcs


def adapt_func_level(code: str, lang: str):
    if lang == "java":
        code = "public class UniqueFunc\n{" + code + "}"
    if lang == "cpp":
        code = re.sub("^inline ", "", code)
        code = code.replace("public : ", "")
    if lang == "rust":
        code = re.sub("(?<!pub )fn ", "pub unsafe fn ", code)
    if lang == "go":
        assert not code.startswith(
            "package "
        ), f"Code contains package, not at function level:\n{code}\n"
    return "\n".join([LANG_IMPORTS[lang], code])


def code_to_ir(
    input_code,
    lang,
    func_level=False,
    verbose=False,
    timeout=120,
    work_dir=DEFAULT_IR_WORKDIR,
    clean_dir=True,
):
    work_dir = Path(work_dir)
    hash_value = uuid.uuid4()
    time_str = str(int(time.time()))
    tmp_work_dir = work_dir.joinpath(f"{time_str}_{hash_value}")
    output_file = tmp_work_dir.joinpath(f"tmp_code.{lang}")
    if func_level:
        input_code = adapt_func_level(input_code, lang)
    tmp_work_dir.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        f.write(input_code)
    try:
        out = source_file_to_cleaned_IR(
            output_file, lang, verbose=verbose, timeout=timeout, clean_dir=clean_dir,
        )
        if clean_dir:
            shutil.rmtree(tmp_work_dir)
        if lang == "go" and func_level:
            out = [
                s
                for s in out
                if not re.search("^define (hidden )?i64 @main.(min|max)\(", s)
            ]
        if len(out) != 1:
            logger.warn(
                f"Language {lang}, found {len(out)} functions. Input was:\n {input_code}"
            )
        return out
    except subprocess.CalledProcessError as e:
        return [f"{ERROR_MESSAGE} {e}"]
    except subprocess.TimeoutExpired:
        return [f"{ERROR_MESSAGE} timeout"]
    except TimeoutError:
        return [f"{ERROR_MESSAGE} timeout"]
    finally:
        if clean_dir:
            if tmp_work_dir.is_dir():
                shutil.rmtree(tmp_work_dir)


def ir_had_errors(ir):
    return ir.startswith(ERROR_MESSAGE)
