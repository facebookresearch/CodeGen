import datetime
import gzip
import json
import os
import re
import subprocess
import time

from submit_jobs_IR_base import build_default_parser, launch_and_monitor_jobs_w_args
from submit_jobs_IR_to_functions import ir_to_functions
from submit_jobs_lang_to_IR import chunk_jsons
from utils_ir import code_to_ir, extract_lang_IR, get_lang_processor
        
        
def code_to_ir_func_level(input_lang_file, lang, lang_processor, output_folder, date_time):
    func_seen = func_success = 0
    code = open(input_lang_file, "r", errors="ignore").read()
    sa, cl = lang_processor.extract_functions(lang_processor.tokenize_code(code))
    funcs = sa + cl
    
    for i, funcs_code in enumerate(funcs):
        fcode = re.sub("^inline ", "", lang_processor.detokenize_code(funcs_code))
        ircode = code_to_ir(fcode, lang, func_level=True, verbose=False, clean_dir=True, cannonize=False)
        func_seen += 1
        if len(ircode) > 0 and (not ircode[0].startswith("subprocess error:")):
            func_success += 1
            os.makedirs(output_folder, exist_ok=True)
            filename = os.path.join(output_folder, f"{i}.ll")
            with open(filename, 'w') as f:
                f.write(ircode[0])
            
    print(f"[{date_time}] {func_seen} functions found, {func_success} extracted in {os.path.basename(input_lang_file)}", flush=True)
    return func_seen, func_success


def lang_to_ir_function(output_path, total_chunks, chunk, lang):

    start_time = time.time()
    broz_lang = f"/private/home/broz/data/new_github_contents/{lang}_deduped/"

    chunk_lang_code = chunk_jsons(total_chunks, chunk, broz_lang, lang)
    IR_files_path = os.path.join(output_path, "IR_files_functions", f"chunk_{chunk}")
    lang_dir = os.path.join(output_path, lang, f"chunk_{chunk}")
    jsons_dir = os.path.join(output_path, "jsons", f"chunk_{chunk}")
    os.makedirs(IR_files_path, exist_ok=True)
    os.makedirs(lang_dir, exist_ok=True)
    os.makedirs(jsons_dir, exist_ok=True)
    
    lang_processor = get_lang_processor(lang)

    errors_count = {}
    errors_count["succeeded"] = errors_count["keyerrors"] = errors_count[
        "calledprocesserrors"
    ] = errors_count["timeouterrors"] = errors_count["recursionerrors"] = 0
    functions_seen = functions_succeeded = 0
    for i, lang_code in enumerate(chunk_lang_code):
        file_base_name = "{}_from_json_{}_line_{}".format(
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
            print(f"[{i} / {len(chunk_lang_code)}]", flush=True)
            output_path_dir = os.path.join(IR_files_path, file_base_name)
            functions_seen_local, functions_succeeded_local = code_to_ir_func_level(
                lang_file, lang, lang_processor, output_path_dir, date_time
            )
            functions_seen += functions_seen_local
            functions_succeeded += functions_succeeded_local
            errors_count["succeeded"] += 1
        except subprocess.CalledProcessError:
            errors_count["calledprocesserrors"] += 1
            print(f"[{date_time}] CalledProcessError for {i}", flush=True)
        except subprocess.TimeoutExpired:
            errors_count["timeouterrors"] += 1
            print(f"[{date_time}] TimeoutExpired for {i}", flush=True)
        except RecursionError:
            errors_count["recursionerrors"] += 1
            print(f"[{date_time}] RecursionError for {i}", flush=True)

    print(
        f"{errors_count['succeeded']}/{len(chunk_lang_code)} successfully transformed to IR in this chunk, that is {100 * errors_count['succeeded'] / len(chunk_lang_code):.3}%"
    )
    print(
        f"There were {errors_count['calledprocesserrors']} CalledProcessError, {errors_count['keyerrors']} KeyError,  {errors_count['timeouterrors']} TimeoutExpired, {errors_count['recursionerrors']} RecursionError"
    )
    print(
        f"Seen {functions_seen} functions, {functions_succeeded} succeeded, that is {100 * functions_succeeded / functions_seen:.3}%"
    )
    print(f"Total time: {int(time.time() - start_time)}s")
            
            
def get_parameters(args):
    if args.chunks_to_run is None:
        chunk = list(range(args.total_chunks))
    else:
        chunk = [int(c) for c in ("".join(args.chunks_to_run.split())).split(",")]
    n_chunks_to_run = len(chunk)
    output_path = [args.output_path] * n_chunks_to_run
    total_chunks = [args.total_chunks] * n_chunks_to_run
    lang = [args.lang] * n_chunks_to_run

    return [output_path, total_chunks, chunk, lang]


def main(function):
    parser = build_default_parser()
    args = parser.parse_args()
    launch_and_monitor_jobs_w_args(function, get_parameters, args)


if __name__ == "__main__":
    main(function=lang_to_ir_function)
