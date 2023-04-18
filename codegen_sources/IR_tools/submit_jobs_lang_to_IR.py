import datetime
import gzip
import json
import os
import subprocess

from codegen_sources.IR_tools.submit_jobs_IR_base import (
    build_default_parser,
    launch_and_monitor_jobs_w_args,
)
from codegen_sources.IR_tools.submit_jobs_IR_to_functions import ir_to_functions
from codegen_sources.IR_tools.utils_ir import extract_lang_IR


def chunk_jsons(total_chunks, chunk, source_files_path, lang="cpp"):

    all_lang_jsons = sorted(os.listdir(source_files_path))
    jsons_per_chunk = len(all_lang_jsons) / total_chunks
    first_json, last_json = (
        int(chunk * jsons_per_chunk),
        int((chunk + 1) * jsons_per_chunk),
    )
    jsons_to_read = all_lang_jsons[first_json : last_json + 1]
    perc_start_in_first_chunk = chunk * jsons_per_chunk % 1.0
    perc_end_in_last_chunk = (chunk + 1) * jsons_per_chunk % 1.0

    print(
        f"Transforming {lang} to IR for jsons {first_json} ({perc_start_in_first_chunk * 100:.3}%) to {last_json} ({perc_end_in_last_chunk * 100:.3}%)"
    )

    all_lang_code = []
    for i, json_file in enumerate(jsons_to_read):
        with gzip.open(os.path.join(source_files_path, json_file), "r") as f:
            n_lines = 0
            for line in f:
                n_lines += 1

        first_el = int(n_lines * perc_start_in_first_chunk)
        last_el = int(n_lines * perc_end_in_last_chunk)
        if i == 0:
            print(f"Starting json {first_json} at file {first_el}")
        else:
            first_el = 0
        if i == len(jsons_to_read) - 1 and last_json != len(all_lang_jsons):
            print(f"Ending json {last_json} at file {last_el}")
        else:
            last_el = n_lines + 1

        with gzip.open(os.path.join(source_files_path, json_file), "r") as f:
            line_count = 0
            for line in f:
                if first_el <= line_count < last_el:
                    element = json.loads(line)
                    element["original_n_file"] = first_json + i
                    element["original_n_element"] = str(line_count)
                    all_lang_code.append(element)
                line_count += 1

    print(f"All code loaded, totaling {len(all_lang_code)} files")
    return all_lang_code


def lang_to_ir(output_path, total_chunks, chunk, extract_functions, lang):

    broz_lang = f"/private/home/broz/data/new_github_contents/{lang}_deduped/"

    all_lang_code = chunk_jsons(total_chunks, chunk, broz_lang, lang)
    IR_files_path = os.path.join(output_path, "IR_files", f"chunk_{chunk}")
    lang_dir = os.path.join(output_path, lang, f"chunk_{chunk}")
    jsons_dir = os.path.join(output_path, "jsons", f"chunk_{chunk}")
    os.makedirs(IR_files_path, exist_ok=True)
    os.makedirs(lang_dir, exist_ok=True)
    os.makedirs(jsons_dir, exist_ok=True)

    errors_count = {}
    errors_count["succeeded"] = errors_count["keyerrors"] = errors_count[
        "calledprocesserrors"
    ] = errors_count["timeouterrors"] = 0
    for i, lang_code in enumerate(all_lang_code):
        file_base_name = "{}_from_json_{}_line_{}_O0".format(
            lang, lang_code["original_n_file"], lang_code["original_n_element"]
        )
        lang_file = f"{os.path.join(lang_dir, file_base_name)}.{lang}"
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metadata = {k: v for k, v in lang_code.items() if k != "content"}
        with open(f"{os.path.join(jsons_dir, file_base_name)}.json", "w") as f:
            json.dump(metadata, f)
        try:
            with open(lang_file, "w") as f:
                f.write(lang_code["content"])
        except KeyError:
            print(f"[{date_time}] KeyError for {i}", flush=True)
            errors_count["keyerrors"] += 1
            continue
        try:
            output_path_file = os.path.join(IR_files_path, file_base_name)
            # Timeout in seconds
            extract_lang_IR(
                lang_file, output_path_file + ".ll", lang, verbose=True, timeout=120
            )
            errors_count["succeeded"] += 1
        except subprocess.CalledProcessError:
            errors_count["calledprocesserrors"] += 1
            print(f"[{date_time}] CalledProcessError for {i}", flush=True)
        except subprocess.TimeoutExpired:
            errors_count["timeouterrors"] += 1
            print(f"[{date_time}] TimeoutExpired for {i}", flush=True)

    print(
        f"{errors_count['succeeded']}/{len(all_lang_code)} successfully transformed to IR in this chunk, that is {100 * errors_count['succeeded'] / len(all_lang_code):.3}%"
    )
    print(
        f"There were {errors_count['calledprocesserrors']} CalledProcessError, {errors_count['keyerrors']} KeyError and {errors_count['timeouterrors']} TimeoutExpired"
    )

    if extract_functions:
        print(f"\n\nLaunching extraction of the functions", flush=True)
        ir_to_functions(
            output_path,
            total_chunks,
            chunk,
            IR_files_path[:-1].rsplit("/", 1)[0],
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
    extract_functions = [args.extract_functions] * n_chunks_to_run
    lang = [args.lang] * n_chunks_to_run

    return [output_path, total_chunks, chunk, extract_functions, lang]


def main(function):
    parser = build_default_parser()
    parser.add_argument(
        "--extract_functions",
        default=False,
        action="store_true",
        help="The base path of the videos",
    )
    args = parser.parse_args()
    launch_and_monitor_jobs_w_args(function, get_parameters, args)


if __name__ == "__main__":
    main(function=lang_to_ir)
