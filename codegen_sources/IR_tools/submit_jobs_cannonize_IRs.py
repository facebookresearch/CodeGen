import datetime
import os
import subprocess
from collections import defaultdict
from pathlib import Path

from codegen_sources.IR_tools.submit_jobs_IR_base import (
    bool_flag,
    build_default_parser,
    launch_and_monitor_jobs_w_args,
)
from codegen_sources.IR_tools.utils_ir import (
    TimeoutError,
    cannonize_IR,
    clean_file,
    extract_all_ll_funcnames,
    get_demangle_func,
)


def cannonize_irs(
    output_path, total_chunks, chunk, ir_functions_files_path, lang, cannonize=False
):
    chunkpath = os.path.join(ir_functions_files_path, f"chunk_{chunk}")
    print(f"Computing cannonized IRs for chunk {chunk} in {chunkpath}")
    all_irs = sorted([str(el) for el in list(Path(chunkpath).rglob("*.ll"))])
    cannonized_irs_path = os.path.join(output_path, "cannonized_IRs", f"chunk_{chunk}")
    cleaned_irs_path = os.path.join(output_path, "cleaned_IRs", f"chunk_{chunk}")

    errors_count = defaultdict(int)
    for i, original_ir_file in enumerate(all_irs):
        file_base_name = original_ir_file
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{date_time}] Processing functions file {i}/{len(all_irs)}", flush=True)

        func_names = extract_all_ll_funcnames(open(file_base_name, "r").read())
        print(file_base_name, "\n", func_names, flush=True)
        #         assert len(func_names) == 1  # Should be only one

        cannonized_path = os.path.join(
            cannonized_irs_path, file_base_name.split(f"chunk_{chunk}/")[1]
        )
        os.makedirs(os.path.dirname(cannonized_path), exist_ok=True)
        cleaned_path = os.path.join(
            cleaned_irs_path, file_base_name.split(f"chunk_{chunk}/")[1]
        )
        os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)

        try:
            cannonize_IR(original_ir_file, cannonized_path, cannonize, verbose=True)
            errors_count["succeeded"] += 1
        except subprocess.CalledProcessError:
            errors_count["calledprocesserrors"] += 1
            print(f"[{date_time}] CalledProcessError for {i}", flush=True)
        except subprocess.TimeoutExpired:
            errors_count["timeouterrors"] += 1
            print(f"[{date_time}] TimeoutExpired for {i}", flush=True)
        except TimeoutError:
            errors_count["timeouterrors"] += 1
            print(f"[{date_time}] TimeoutError for {i}", flush=True)

        if os.path.isfile(cannonized_path):
            full_cannonized_file = open(cannonized_path, "r").read()
            with open(cleaned_path, "w") as f:
                demangle_fn = get_demangle_func(lang)
                try:
                    f.write(demangle_fn(clean_file(full_cannonized_file)))
                except TimeoutError:
                    errors_count["timeouterrors"] += 1
                    print(f"[{date_time}] TimeoutError for {i}", flush=True)

        print("\n", flush=True)

    print(
        f"{errors_count['succeeded']}/{len(all_irs)} successfully cannonized in this chunk, that is {100 * errors_count['succeeded'] / len(all_irs):.3}%"
    )
    print(
        f"There were {errors_count['calledprocesserrors']} CalledProcessError, {errors_count['keyerrors']} KeyError and {errors_count['timeouterrors']} TimeoutExpired"
    )


def get_parameters(args):
    assert args.lang in {
        "rust",
        "java",
        "go",
        "cpp",
    }, f"lang parameter should be set to rust, go, java or cpp, it was {args.lang}"

    if args.chunks_to_run is None:
        chunk = list(range(args.total_chunks))
    else:
        chunk = [int(c) for c in ("".join(args.chunks_to_run.split())).split(",")]
    n_chunks_to_run = len(chunk)
    output_path = [args.output_path] * n_chunks_to_run
    total_chunks = [args.total_chunks] * n_chunks_to_run
    ir_functions_files_path = [args.ir_functions_files_path] * n_chunks_to_run
    lang = [args.lang] * n_chunks_to_run

    return [output_path, total_chunks, chunk, ir_functions_files_path, lang]


def main():
    parser = build_default_parser()
    parser.add_argument(
        "--ir_functions_files_path",
        default=None,
        action="store",
        help="The path of the .ll files",
    )
    args = parser.parse_args()

    launch_and_monitor_jobs_w_args(
        cannonize_irs, get_parameters, args, slurm_partition="learnlab"
    )


if __name__ == "__main__":
    main()
