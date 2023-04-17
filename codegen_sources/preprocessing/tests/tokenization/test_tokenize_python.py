# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import ast
import difflib
import typing as tp
from pathlib import Path
import pytest

from codegen_sources.preprocessing.lang_processors import (
    PythonProcessor,
    PythonTreeSitterProcessor,
    LangProcessor,
)
from codegen_sources.preprocessing.tests.tokenization.tokenization_tests_utils import (
    compare_funcs,
)


processors = (PythonProcessor(), PythonTreeSitterProcessor())
with_both_processors = pytest.mark.parametrize("processor", processors)


def test_python_tree_sitter_on_all_codegen_sources() -> None:
    processor = processors[1]
    root = Path(__file__).parents[3]
    assert root.name == "codegen_sources"
    errors = []
    total = 0
    fail = 0
    for fp in root.rglob("**/*.py"):
        if any(f"preprocessing/{x}" in str(fp) for x in ("tests", "lang_processors")):
            continue  # ignore since it's mostly due to token names making a mess
        total += 1
        text = fp.read_text()
        tokens = processor.tokenize_code(text)
        string = processor.detokenize_code(tokens)
        try:
            ast.parse(string)
        except SyntaxError as e:
            fail += 1
            errors.extend([str(fp), text, " ".join(tokens), str(e), string])
            print(fp)
    if errors:
        Path("errors.txt").write_text(
            "\n##################################\n".join(errors), encoding="utf8"
        )
        raise AssertionError(f"{fail} failures out of {total} files. Check error.txt")


TESTS = []
TESTS.append(("a = [3.14,4]", ["a", "=", "[", "3.14", ",", "4", "]", "NEW_LINE"]))

TESTS.append(
    (
        (
            """from src.tokenize import _tok
@decorated
def func1(a):
    assert isinstance(a, int)
    a+=1
    return a"""
        ),
        [
            "from",
            "src",
            ".",
            "tokenize",
            "import",
            "_tok",
            "NEW_LINE",
            "@",
            "decorated",
            "NEW_LINE",
            "def",
            "func1",
            "(",
            "a",
            ")",
            ":",
            "NEW_LINE",
            "INDENT",
            "assert",
            "isinstance",
            "(",
            "a",
            ",",
            "int",
            ")",
            "NEW_LINE",
            "a",
            "+=",
            "1",
            "NEW_LINE",
            "return",
            "a",
            "NEW_LINE",
            "DEDENT",
        ],
    )
)

TESTS.append(
    (
        (
            """#comment blabla
''' lll coo
# kkk ''' """
        ),
        [],
    )
)

TESTS.append(
    (
        (
            """#comment blabla
a = 10 """
        ),
        ["a", "=", "10", "NEW_LINE"],
    )
)


TESTS.append(
    (
        (
            """'''comment
blabla'''
a = 10 """
        ),
        ["a", "=", "10", "NEW_LINE"],
    )
)


TESTS.append(
    (
        (
            """'''comment
blabla'''
a = ('fff',
'fff') """
        ),
        ["a", "=", "(", "' fff '", ",", "' fff '", ")", "NEW_LINE"],
    )
)

TESTS.append(
    (
        (
            """
a = '''fff
fff''' """
        ),
        ["a", "=", "''' fff STRNEWLINE fff '''", "NEW_LINE"],
    )
)

TESTS.append(
    (
        (
            """
a = \"\"\"
'fff'
\"\"\"
"""
        ),
        ["a", "=", '""" STRNEWLINE \' fff \' STRNEWLINE """', "NEW_LINE"],
    )
)


TESTS.append(
    (
        (
            """with open('ff.txt', 'r') as f:
    x = f.read()
line = x.readline()"""
        ),
        [
            "with",
            "open",
            "(",
            "' ff . txt '",
            ",",
            "' r '",
            ")",
            "as",
            "f",
            ":",
            "NEW_LINE",
            "INDENT",
            "x",
            "=",
            "f",
            ".",
            "read",
            "(",
            ")",
            "NEW_LINE",
            "DEDENT",
            "line",
            "=",
            "x",
            ".",
            "readline",
            "(",
            ")",
            "NEW_LINE",
        ],
    )
)

TESTS.append(
    (
        (r'''WELCOME_MSG = "Hello you!\n what's up?"'''),
        ["WELCOME_MSG", "=", '" Hello ▁ you ! \\n ▁ what \' s ▁ up ? "', "NEW_LINE"],
    )
)

TESTS.append(
    (
        (
            r"""'''this is a
docstring on 2 lines '''"""
        ),
        [],
    )
)
TESTS.append(
    (
        r"""tab = ['a',
    'b',
    'c']""",
        ["tab", "=", "[", "' a '", ",", "' b '", ",", "' c '", "]", "NEW_LINE"],
    )
)

TESTS.append(
    (
        r"""import xxx
a='Hello \n word'""",
        ["import", "xxx", "NEW_LINE", "a", "=", "' Hello ▁ \\n ▁ word '", "NEW_LINE"],
    )
)


TESTS.append(
    (
        r"""def gen(num: int) -> tp.Iterable[int]:
    for k in range(3):  # commented
       out = \
           yield k""",
        [
            "def",
            "gen",
            "(",
            "num",
            ":",
            "int",
            ")",
            "->",
            "tp",
            ".",
            "Iterable",
            "[",
            "int",
            "]",
            ":",
            "NEW_LINE",
            "INDENT",
            "for",
            "k",
            "in",
            "range",
            "(",
            "3",
            ")",
            ":",
            "NEW_LINE",
            "INDENT",
            "out",
            "=",
            "yield",
            "k",
            "NEW_LINE",
            "DEDENT",
            "DEDENT",
        ],
    )
)
TESTS.append(
    (
        '''def myfunc():
    """my doc with comment""" # my comment
    return 1
''',
        [
            "def",
            "myfunc",
            "(",
            ")",
            ":",
            "NEW_LINE",
            "INDENT",
            "return",
            "1",
            "NEW_LINE",
            "DEDENT",
        ],
    )
)

# TESTS.append(
#     ('''bin_path = path.with_suffix("")
# out = f'{param_type_filled.replace("&", "")}'
# ''',
#      ['bin_path', '=', 'path', '.', 'with_suffix', '(', '" "', ')', 'NEW_LINE', 'out', '=',
#       'f\' { param _ type _ filled . replace ( " & " , ▁ " " ) } \'', 'NEW_LINE'])
# )


TESTS2 = []
TESTS2.append(
    r"""''' module with one class and one function
'''
import torch
from ..src.nnnn import jjj
import .knpon.module

class myclass:
# comment blala
# comment blabl2
        def geometric_suite():
            i = 0
            j = 1
            for i in range(2):
            # this function will print "Hello Word\nI am boby ! what's up ?"
                i += 1
                j += 3
                l = module.function()
                print("Hello Word\nI am boby !")
        return i, j"""
)


TESTS3 = []

TESTS3.append(
    (
        (
            """'''comment
blabla'''
a = ('fff',
'fff') """
        ),
        [
            "''' comment STRNEWLINE blabla '''",
            "NEW_LINE",
            "a",
            "=",
            "(",
            "' fff '",
            ",",
            "' fff '",
            ")",
            "NEW_LINE",
        ],
    )
)

TESTS3.append(
    (
        (
            """'''comment
blabla'''
a = 10 """
        ),
        ["''' comment STRNEWLINE blabla '''", "NEW_LINE", "a", "=", "10", "NEW_LINE"],
    )
)


TESTS3.append(
    (
        (
            """
a = '''fff
fff''' """
        ),
        ["a", "=", "''' fff STRNEWLINE fff '''", "NEW_LINE"],
    )
)


TESTS3.append(
    (
        (
            """#comment   blabla
# --- ** *
a = 10 """
        ),
        ["# comment ▁ blabla ENDCOM", "a", "=", "10", "NEW_LINE"],
    )
)


TESTS3.append(
    (
        ("""a = 10 #comment   blabla"""),
        ["a", "=", "10", "# comment ▁ blabla ENDCOM", "NEW_LINE"],
    )
)


TESTS3.append(
    (
        (
            """def my_func():
    ''' ********'''
    return 0"""
        ),
        [
            "def",
            "my_func",
            "(",
            ")",
            ":",
            "NEW_LINE",
            "INDENT",
            "return",
            "0",
            "NEW_LINE",
            "DEDENT",
        ],
    )
)

TESTS_DONT_PROCESS_STRINGS = [
    (
        r"""import xxx
    # this is a comment
a='Hello \nworld'
""",
        [
            "import",
            "xxx",
            "NEW_LINE",
            "# this is a comment ENDCOM",
            "a",
            "=",
            "'Hello \\nworld'",
            "NEW_LINE",
        ],
    ),
    (
        (
            """from src.tokenize import _tok
def func1(a):
    a+=1
    return a"""
        ),
        [
            "from",
            "src",
            ".",
            "tokenize",
            "import",
            "_tok",
            "NEW_LINE",
            "def",
            "func1",
            "(",
            "a",
            ")",
            ":",
            "NEW_LINE",
            "INDENT",
            "a",
            "+=",
            "1",
            "NEW_LINE",
            "return",
            "a",
            "NEW_LINE",
            "DEDENT",
        ],
    ),
    (
        r"""import xxx
a='''
Hello
world'''""",
        ["import", "xxx", "NEW_LINE", "a", "=", "'''\\nHello\\nworld'''", "NEW_LINE"],
    ),
    (
        (
            """from src.tokenize import _tok
def func1(a):
    a+=1
    return a"""
        ),
        [
            "from",
            "src",
            ".",
            "tokenize",
            "import",
            "_tok",
            "NEW_LINE",
            "def",
            "func1",
            "(",
            "a",
            ")",
            ":",
            "NEW_LINE",
            "INDENT",
            "a",
            "+=",
            "1",
            "NEW_LINE",
            "return",
            "a",
            "NEW_LINE",
            "DEDENT",
        ],
    ),
]

TESTS_SPECIAL_STRINGS = [
    """m = re.match ( r'(?:py.*-)?([\d\.]+)(?:-(\w+))?' , vers )
""",
    """print ( f"{epoch} : {score}" )
""",
]

TESTS_IMPORTS = [
    (
        """import numpy as np
from math import sqrt
print(sqrt(2))
""",
        [
            "import",
            "numpy",
            "as",
            "np",
            "NEW_LINE",
            "from",
            "math",
            "import",
            "sqrt",
            "NEW_LINE",
            "print",
            "(",
            "sqrt",
            "(",
            "2",
            ")",
            ")",
            "NEW_LINE",
        ],
    )
]

TEST_EXTRACT_FUNCTIONS = [
    (
        (
            """from src.tokenize import _tok
def func1(a):
    return a

class Foo():
    def bar(self):
        return 1
""",
            (
                ["def func1 ( a ) : NEW_LINE INDENT return a NEW_LINE DEDENT"],
                ["def bar ( self ) : NEW_LINE INDENT return 1 NEW_LINE DEDENT"],
            ),
        )
    )
]


def assert_tokens_equal(
    actual: tp.List[str], expected: tp.List[str], code: tp.Optional[str] = None
) -> None:
    if actual == expected:
        return
    line_diff = [
        j for j, (line, line_) in enumerate(zip(actual, expected)) if line != line_
    ]
    line_num = line_diff[-1] if len(line_diff) > 0 else -1
    strings = [
        f"Difference at {line_num}\nExpected:\n==========\n{expected}\nbut found:\n==========\n{actual}"
    ]
    if code is not None:
        strings.append(f"# # for input # #\n{code!r}")
        strings.append(f"# # which prints as follows # #\n{code}")
    raise Exception("\n\n".join(strings))


@with_both_processors
@pytest.mark.parametrize("code,expected", TESTS)
def test_python_tokenizer(
    code: str, expected: tp.List[str], processor: LangProcessor
) -> None:
    if isinstance(processor, PythonProcessor) and "my doc with comment" in code:
        pytest.skip("TODO")
    y_ = processor.tokenize_code(code)
    assert_tokens_equal(y_, expected, code)


@with_both_processors
@pytest.mark.parametrize("code,expected", TESTS_IMPORTS)
def test_imports(code: str, expected: tp.List[str], processor: LangProcessor) -> None:
    y_ = processor.tokenize_code(code)
    assert_tokens_equal(y_, expected, code)


@with_both_processors
@pytest.mark.parametrize("code,expected", TESTS3)
def test_python_tokenizer_with_coms(
    code: str, expected: tp.List[str], processor: LangProcessor
) -> None:
    y_ = processor.tokenize_code(code, keep_comments=True)
    assert_tokens_equal(y_, expected, code)


@with_both_processors
@pytest.mark.parametrize("code,expected", TESTS_DONT_PROCESS_STRINGS)
def test_python_dont_process_strings(
    processor: LangProcessor, code: str, expected: tp.List[str]
) -> None:
    y_ = processor.tokenize_code(code, keep_comments=True, process_strings=False)
    assert_tokens_equal(y_, expected, code)


@with_both_processors
@pytest.mark.parametrize("code", [x[0] for x in TESTS] + TESTS2)
def test_python_detokenizer(code: str, processor: LangProcessor) -> None:
    if isinstance(processor, PythonProcessor) and "my doc with comment" in code:
        pytest.skip("TODO")
    tokens = processor.tokenize_code(code)
    x_ = processor.detokenize_code(tokens)
    tokens_ = processor.tokenize_code(x_)
    print("# Rebuilding #\n", x_, "\n# from #\n", code)
    assert_tokens_equal(tokens_, tokens, code)


@with_both_processors
def test_detokenizer_output(processor: LangProcessor) -> None:
    for i, x in enumerate(TESTS_SPECIAL_STRINGS):
        tokens = processor.tokenize_code(x)
        x_ = processor.detokenize_code(tokens)
        d = difflib.Differ()
        if x != x_:
            diff = d.compare(x.split("\n"), x_.split("\n"))
            for line in diff:
                print(line)
            raise Exception(
                f"Differences between\n========== Original:\n{x}\n========== \n and actual Detokenized:\n{x_}"
            )


@with_both_processors
def test_extract_functions(processor: LangProcessor) -> None:
    for input_file, expected_funcs in TEST_EXTRACT_FUNCTIONS:
        actual_funcs_sa, actual_funcs_cl = processor.extract_functions(
            processor.tokenize_code(input_file)
        )
        print(actual_funcs_sa, actual_funcs_cl)
        expected_sa, expected_cl = expected_funcs
        compare_funcs(actual_funcs_sa, expected_sa, normalization=lambda x: x.strip())
        compare_funcs(actual_funcs_cl, expected_cl, normalization=lambda x: x.strip())


def test_extract_functions_without_tok() -> None:
    processor = PythonTreeSitterProcessor()
    for input_file, expected_funcs in TEST_EXTRACT_FUNCTIONS:
        actual_funcs_sa, actual_funcs_cl = processor.extract_functions(
            input_file, tokenized=False
        )
        print(actual_funcs_sa, actual_funcs_cl)
        expected_sa, expected_cl = expected_funcs
        compare_funcs(
            [" ".join(processor.tokenize_code(x)) for x in actual_funcs_sa], expected_sa
        )
        compare_funcs(
            [" ".join(processor.tokenize_code(x)) for x in actual_funcs_cl], expected_cl
        )


AST_ERRORS = [
    """test_out_path = Path(__file__).parent.joinpath(
    "test_output_should_not_be_written_go.out"
)
if test_out_path.exists():
    os.remove(test_out_path)
""",
    '''class Test:
    """docstring"""  # comment
    def __init__(self):
        pass
''',
    '''
class Error(RuntimeError):
    """doc"""

def _check_command(command: str):
    pass
''',
    """
bin_path = path.with_suffix("")
out = f'{param_type_filled.replace("&", "")}'
""",
]


@with_both_processors
@pytest.mark.parametrize("code", AST_ERRORS)
def test_ast_errors(processor: LangProcessor, code: str) -> None:
    if isinstance(processor, PythonProcessor):
        pytest.skip("Standard Python tokenizer does not work for now")
    ast.parse(code)
    tokens = processor.tokenize_code(code)
    string = processor.detokenize_code(tokens)
    try:
        ast.parse(string)
    except SyntaxError:
        print("\n########\n".join([code, " ".join(tokens), string]))
        raise AssertionError("Cannot parse output")
