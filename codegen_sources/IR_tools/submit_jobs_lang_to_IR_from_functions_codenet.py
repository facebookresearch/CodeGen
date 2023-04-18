import datetime
import os
import subprocess
import time

from submit_jobs_IR_base import build_default_parser, launch_and_monitor_jobs_w_args
from submit_jobs_IR_to_functions import ir_to_functions
from submit_jobs_lang_to_IR_from_functions import code_to_ir_func_level, get_parameters
from utils_ir import code_to_ir, extract_lang_IR, get_lang_processor


def chunk_list(list_, chunk, total_chunks):
    elements_per_chunk = len(list_) / total_chunks
    first_element, last_element = (
        int(chunk * elements_per_chunk),
        int((chunk + 1) * elements_per_chunk),
    )
    return list_[first_element : last_element + 1]
    
    
def list_all_files_codenet(lang, data_path):
    
    print(f"Searching for all problem files in {data_path} for lang {lang}", flush=True)
    lang_name_dict = {"cpp": "C++", "java": "Java", "rs": "Rust", "go": "Go"}
    
    all_problems = os.listdir(data_path)
    all_files = []
    for p in all_problems:
        lang_path = os.path.join(data_path, p, lang_name_dict[lang])
        if os.path.exists(lang_path):
            all_files.extend([os.path.join(lang_path, el) for el in os.listdir(lang_path)])
            
    return sorted(all_files)
            
            
def lang_to_ir_function_codenet(output_path, total_chunks, chunk, lang):
    
    start_time = time.time()
    data_path = "/private/home/broz/datasets/CodeGen/data/Project_CodeNet/data"
    all_lang_code = list_all_files_codenet(lang, data_path)
    chunk_lang_code = chunk_list(all_lang_code, chunk, total_chunks)
    IR_files_path = os.path.join(output_path, "IR_files_functions_codenet", f"chunk_{chunk}")
    os.makedirs(IR_files_path, exist_ok=True)
    
    lang_processor = get_lang_processor(lang)

    errors_count = {}
    errors_count["succeeded"] = errors_count["keyerrors"] = errors_count[
        "calledprocesserrors"
    ] = errors_count["timeouterrors"] = errors_count["recursionerrors"] = 0
    functions_seen = functions_succeeded = 0
    for i, lang_file in enumerate(chunk_lang_code):
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_base_name = lang_file.replace(data_path, "").rsplit(".", 1)[0].replace("/", "_")[1:]
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


def main(function):
    parser = build_default_parser()
    args = parser.parse_args()
    launch_and_monitor_jobs_w_args(function, get_parameters, args)


if __name__ == "__main__":
    main(function=lang_to_ir_function_codenet)
