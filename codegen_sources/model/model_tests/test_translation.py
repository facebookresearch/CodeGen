# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import subprocess
import uuid
from pathlib import Path

import pytest
import requests
import torch

import codegen_sources
from ..src.constants import EXT
from ..translate import Translator
from ...code_runners.python_code_runner import PYTHON_ENV
from ...preprocessing.tests.obfuscation.utils import diff_tester

DELIMITER = "=" * 20
OUTPUT_DELIMITER = f"""Translated %s function:
{DELIMITER}"""
TRANSCODER_MODEL_1_URL = "https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/TransCoder_model_1.pth"
ROOT_FOLDER = Path(codegen_sources.__file__).parents[1]
model_folder = ROOT_FOLDER.joinpath("data", "sample_model")
model_folder.mkdir(exist_ok=True)
MODEL_PATH = model_folder.joinpath("TransCoder_model_1.pth")
BPE_PATH = ROOT_FOLDER / "data/bpe/cpp-java-python/codes"
if not MODEL_PATH.exists():
    r = requests.get(TRANSCODER_MODEL_1_URL, allow_redirects=True)
    open(MODEL_PATH, "wb").write(r.content)


def translation_generic_tester(
    input_function: str,
    src_lang: str,
    tgt_lang: str,
    expected: str,
    model_path: Path = MODEL_PATH,
    beam_size: int = 1,
):
    if os.environ.get("CI", False):
        # This test doesn't work on the CI while it works on ssh for unknown reasons
        return
    hash_value = uuid.uuid4()
    code_path = f"/tmp/{hash_value}{EXT[tgt_lang]}"
    with open(code_path, "w") as f:
        f.write(input_function)

    cmd = f"cd {ROOT_FOLDER};NPY_MKL_FORCE_INTEL=1 python -m codegen_sources.model.translate --input {code_path} --src_lang {src_lang} --tgt_lang {tgt_lang} --model_path {model_path} --gpu false --beam_size {beam_size}"
    print(f"Running: {cmd}")
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=180,
            shell=True,
            env=PYTHON_ENV,
        )
    except:
        Path(code_path).unlink()
        raise

    assert proc.returncode == 0, f"Translation failed with error {proc.stderr.decode()}"
    output = proc.stdout.decode()
    delimiter = OUTPUT_DELIMITER % tgt_lang
    assert (
        delimiter in output
    ), f"was successful but couldn't find translation in {output}"
    output = output.split(delimiter)[-1]
    diff_tester(expected.strip(), output.strip())


def translation_class_tester(
    input_function: str,
    src_lang: str,
    tgt_lang: str,
    expected: str,
    model_path: Path = MODEL_PATH,
    beam_size: int = 1,
):
    hash_value = uuid.uuid4()
    code_path = f"/tmp/{hash_value}{EXT[tgt_lang]}"
    with open(code_path, "w") as f:
        f.write(input_function)

    cmd = f"cd {ROOT_FOLDER};NPY_MKL_FORCE_INTEL=1 python -m codegen_sources.model.translate --input {code_path} --src_lang {src_lang} --tgt_lang {tgt_lang} --model_path {model_path} --gpu false --beam_size {beam_size}"
    print(f"Running: {cmd}")

    # Initialize translator
    translator = Translator(MODEL_PATH, BPE_PATH, gpu=False, efficient_attn=None,)

    # read input code from stdin

    print(input_function)
    with torch.no_grad():
        output = translator.translate(
            input_function, lang1=src_lang, lang2=tgt_lang, beam_size=beam_size,
        )
    output = DELIMITER.join([x.strip() for x in output])
    expected = DELIMITER.join([x.strip() for x in expected.split(DELIMITER)])
    diff_tester(expected, output)


CPP_FACTORIAL = """int factorial ( int n ) {
  if ( n > 1 ) return n * factorial ( n - 1 ) ;
  else return 1 ;
}"""

JAVA_FACTORIAL = """public static int factorial ( int n ) {
  if ( n > 1 ) {
    return n * factorial ( n - 1 ) ;
  }
  else {
    return 1 ;
  }
}
"""

PYTHON_FACTORIAL = """def factorial ( n ) :
    if n > 1 :
        return n * factorial ( n - 1 )
    else :
        return 1
"""


@pytest.mark.parametrize("from_class", (False, True))
def test_cpp_to_python_translation(from_class: bool):
    input_function = CPP_FACTORIAL
    expected_output = PYTHON_FACTORIAL
    if from_class:
        translation_class_tester(input_function, "cpp", "python", expected_output)
    else:
        translation_generic_tester(input_function, "cpp", "python", expected_output)


@pytest.mark.parametrize("from_class", (False, True))
def test_cpp_to_java_translation(from_class: bool):
    expected_output = JAVA_FACTORIAL
    if from_class:
        translation_class_tester(CPP_FACTORIAL, "cpp", "java", expected_output)
    else:
        translation_generic_tester(CPP_FACTORIAL, "cpp", "java", expected_output)


@pytest.mark.parametrize("from_class", (False, True))
def test_java_to_python_translation(from_class: bool):
    if from_class:
        translation_class_tester(JAVA_FACTORIAL, "java", "python", PYTHON_FACTORIAL)
    else:
        translation_generic_tester(JAVA_FACTORIAL, "java", "python", PYTHON_FACTORIAL)


@pytest.mark.parametrize("from_class", (False, True))
def test_java_to_cpp_translation(from_class: bool):
    if from_class:
        translation_class_tester(JAVA_FACTORIAL, "java", "cpp", CPP_FACTORIAL)
    else:
        translation_generic_tester(JAVA_FACTORIAL, "java", "cpp", CPP_FACTORIAL)


@pytest.mark.parametrize("from_class", (False, True))
def test_python_to_java_translation(from_class: bool):
    expected = """public static int factorial ( int n ) {
  if ( n > 1 ) return n * factorial ( n - 1 ) ;
  else return 1 ;
}"""
    if from_class:
        translation_class_tester(PYTHON_FACTORIAL, "python", "java", expected)
    else:
        translation_generic_tester(PYTHON_FACTORIAL, "python", "java", expected)


@pytest.mark.parametrize("from_class", (False, True))
def test_python_to_cpp_translation(from_class: bool):
    if from_class:
        translation_class_tester(PYTHON_FACTORIAL, "python", "cpp", CPP_FACTORIAL)
    else:
        translation_generic_tester(PYTHON_FACTORIAL, "python", "cpp", CPP_FACTORIAL)


@pytest.mark.parametrize("from_class", (False, True))
def test_translation_with_beam_decoding(from_class: bool):
    expected = """int factorial ( int n ) {
  if ( n > 1 ) return n * factorial ( n - 1 ) ;
  else return 1 ;
}

====================
public : int factorial ( int n ) {
  if ( n > 1 ) return n * factorial ( n - 1 ) ;
  else return 1 ;
}

====================
int factorial ( int n ) {
  if ( n > 1 ) {
    return n * factorial ( n - 1 ) ;
  }
  else {
    return 1 ;
  }
}

====================
inline int factorial ( int n ) {
  if ( n > 1 ) return n * factorial ( n - 1 ) ;
  else return 1 ;
}

====================
long long factorial ( long long n ) {
  if ( n > 1 ) return n * factorial ( n - 1 ) ;
  else return 1 ;
}"""
    if from_class:
        translation_class_tester(
            PYTHON_FACTORIAL, "python", "cpp", expected, beam_size=5
        )
    else:
        translation_generic_tester(
            PYTHON_FACTORIAL, "python", "cpp", expected, beam_size=5
        )
