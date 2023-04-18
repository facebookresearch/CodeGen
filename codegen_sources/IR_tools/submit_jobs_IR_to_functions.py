import datetime
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from codegen_sources.IR_tools.submit_jobs_cannonize_IRs import cannonize_irs
from codegen_sources.IR_tools.submit_jobs_IR_base import (
    build_default_parser,
    launch_and_monitor_jobs_w_args,
)
from codegen_sources.IR_tools.utils_ir import (
    TimeoutError,
    extract_function,
    extract_relevant_functions,
)

# ir_files_path = "/private/home/mszafraniec/codegen/IR/test_IR_generation/IR_files/"
# llvm_12_path = "/private/home/broz/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-20.04/bin/"
llvm_14_path = "/private/home/mszafraniec/llvm-project/build/bin/"


def ir_to_functions(
    output_path, total_chunks, chunk, ir_files_path, lang="cpp", do_cannonize=True
):
    #     all_ir_files = os.listdir(ir_files_path)
    #     all_ir_files = sorted([el for el in all_ir_files if el.endswith('.ll')])
    #     files_per_chunk = len(all_ir_files) / total_chunks
    #     start_file = int(chunk * files_per_chunk)
    #     end_file = int((chunk + 1) * files_per_chunk)
    #     chunk_files = all_ir_files[start_file : end_file]
    #     print(f"There are {len(all_ir_files)} IR files.")
    #     print(f"This chunk will start at file {start_file} and end at file {end_file}.")

    ir_files_path = os.path.join(ir_files_path, f"chunk_{chunk}")
    chunk_files = os.listdir(ir_files_path)
    chunk_files = sorted([el for el in chunk_files if el.endswith(".ll")])

    ll_functions_dir = os.path.join(output_path, "ll_functions", f"chunk_{chunk}")

    os.makedirs(ll_functions_dir, exist_ok=True)
    #     bc_file_name = os.path.join(ll_functions_dir, f"bc_chunk_{chunk}.bc")
    lang_processor = get_lang_processor(lang)
    n_all_funcs = []
    all_files_w_funcs = []
    for n_file, ir_file in enumerate(chunk_files):

        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"[{date_time}] Searching for functions in file {n_file}/{len(chunk_files)}",
            flush=True,
        )

        #         subprocess.check_output(f'{llvm_14_path}llvm-as {os.path.join(ir_files_path, ir_file)} -o {bc_file_name}', shell=True)
        #         out = subprocess.check_output(f'{llvm_14_path}llvm-nm test.bc --demangle -U -p', shell=True)
        #         out_mangled = subprocess.check_output(f'{llvm_14_path}llvm-nm {bc_file_name} -U -p', shell=True)

        #         funcs = re.findall('(?<=---------------- T ).*', out.decode())
        #         mangled_funcs = re.findall('(?<=---------------- T ).*', out_mangled.decode())
        full_file = open(os.path.join(ir_files_path, ir_file), "r").read()

        #         mangled_funcs = extract_all_ll_funcnames(full_file)
        try:
            mangled_funcs = extract_relevant_functions(
                full_file, ir_file.replace("ll", lang), lang_processor, lang
            )
            n_all_funcs.append(len(mangled_funcs))
            all_files_w_funcs.append([ir_file, mangled_funcs])
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"Exception getting mangled function names: {e}")
            continue
        except TimeoutError:
            print(f"TimeoutError for file {ir_file} when searching for functions")
            continue

    all_files_w_funcs = sorted(
        all_files_w_funcs, key=lambda x: len(x[1])
    )  # With more functions has more chances to crash

    for n_file, [ir_file, mangled_funcs] in enumerate(all_files_w_funcs):
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"[{date_time}] Processing file {n_file}/{len(chunk_files)} - {len(mangled_funcs)} functions",
            flush=True,
        )
        original_file_funcs_dir = os.path.join(ll_functions_dir, ir_file[:-3])
        os.makedirs(original_file_funcs_dir, exist_ok=True)

        for n_func, func in enumerate(mangled_funcs):
            output_ll_file = os.path.join(original_file_funcs_dir, f"{n_func}.ll")
            try:
                extract_function(
                    func, os.path.join(ir_files_path, ir_file), output_ll_file
                )
            except subprocess.CalledProcessError:
                print(f"Failure for file {ir_file} and func {func}", flush=True)
            except subprocess.TimeoutExpired:
                print(f"TimeoutExpired for file {ir_file} and func {func}", flush=True)
            except TimeoutError:
                print(f"TimeoutError for file {ir_file} and func {func}", flush=True)
            except OSError:
                print(f"OSError for file {ir_file} and func {func}", flush=True)

    #             func_file = open(output_ll_file, 'r').read()

    #             glob_variables = re.findall('(?<=@).*(?= =)', func_file)
    #             glob_variables = [el.replace('$', '\$') for el in glob_variables]
    #             glob_variables = np.setdiff1d(glob_variables, ['0'])  # Forbidden name ?
    #             glob_variables = [el for el in glob_variables if '\\' not in el]

    #             try:
    #                 subprocess.check_call(extract_command.format(func, output_ll_file, os.path.join(ir_files_path, ir_file)) + ' '.join([f' --glob {el}' for el in glob_variables]), shell=True)
    #             except OSError:  # Argument list too long
    #                 continue

    # Keep head and tail for having valid function to canonicalize
    #             func_file_w_globals = open(output_ll_file, 'r').read()
    #             func_file_wo_head_tail = re.split('\n\n(?=attributes #0)', func_file_w_globals.split('\n\n', 1)[1])[0]
    #             open(output_ll_file, 'w').write(func_file_wo_head_tail)

    print(
        f"Extracted {sum(n_all_funcs)} functions out of {len(chunk_files)} files, or {sum(n_all_funcs) / len(chunk_files):.3} per file",
        flush=True,
    )
    print(
        f"There were between {min(n_all_funcs)} and {max(n_all_funcs)} functions per file",
        flush=True,
    )

    if do_cannonize:
        print(f"\n\nLaunching cannonizing/cleaning of the functions", flush=True)
        cannonize_irs(
            output_path,
            total_chunks,
            chunk,
            ll_functions_dir[:-1].rsplit("/", 1)[0],
            lang=lang,
        )  # Remove the /chunk_xxx


def get_parameters(args):
    if args.chunks_to_run is None:
        chunk = list(range(args.total_chunks))
    else:
        chunk = [int(c) for c in ("".join(args.chunks_to_run.split())).split(",")]
    n_chunks_to_run = len(chunk)
    output_path = [args.output_path] * n_chunks_to_run
    total_chunks = [args.total_chunks] * n_chunks_to_run
    ir_files_path = [args.ir_files_path] * n_chunks_to_run
    lang = [args.lang] * n_chunks_to_run
    do_cannonize = [args.do_cannonize] * n_chunks_to_run

    return [output_path, total_chunks, chunk, ir_files_path, lang, do_cannonize]


def main():
    parser = build_default_parser()
    parser.add_argument(
        "--ir_files_path",
        default=None,
        action="store",
        help="The path of the .ll files",
    )
    parser.add_argument(
        "--do_cannonize",
        default=False,
        action="store_true",
        help="The base path of the videos",
    )
    args = parser.parse_args()
    launch_and_monitor_jobs_w_args(ir_to_functions, get_parameters, args)


if __name__ == "__main__":
    main()
