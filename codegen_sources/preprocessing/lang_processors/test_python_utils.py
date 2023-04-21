# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import typing as tp
import pytest
from . import python_tree_sitter_processor as ptsp


STAR_IMPORT = "from typing import *"
DICT_IMPORT = "from typing import Dict"
TWO_IMPORTS = "from typing import Dict, List"
IMPORTED = "import typing"
IMPORTED_AS = "import typing as x"
TWO_LINES = "from typing import Dict"


@pytest.mark.parametrize(
    "imports",
    [[STAR_IMPORT], [DICT_IMPORT], [STAR_IMPORT, DICT_IMPORT], [IMPORTED_AS, IMPORTED]],
)
def test_type_cleaner_imports(imports: tp.List[str]) -> None:
    other_import = ["from blublu import Dict"]
    function = ["def hello():", "    print('Hello')"]
    cleaner = ptsp.TypeCleaner()
    lines = other_import + imports + other_import + function
    output = cleaner.get_imports("\n".join(lines))
    assert output == imports


@pytest.mark.parametrize(
    "line", ["from __future__ import division, print_function, absolute_import",],
)
def test_type_cleaner_imports_none(line: str) -> None:
    other_import = ["from blublu import Dict"]
    function = ["def hello():", "    print('Hello')"]
    cleaner = ptsp.TypeCleaner()
    lines = other_import + [line] + other_import + function
    output = cleaner.get_imports("\n".join(lines))
    assert not output


COMM = """Tuple[  # my comment
str]"""


@pytest.mark.parametrize(
    "typestr,expected",
    [
        ("Dict[Text, tp.List[Any]]", "Dict[str,List[Any]]"),
        ("x.Dict[x.Text, tp.List[Any]]", "Dict[str,List[Any]]"),
        ("x.Optional[x.TextIO]", "Optional[TextIO]"),
        ("str|int|List[float]", "Union[int,str,List[float]]"),
        ("str|List[float|None]", "Union[str,List[Optional[float]]]"),
        ("str|Union[int,float]", "Union[float,int,str]"),
        ("Union[int,str,None]", "Optional[Union[int,str]]"),
        ("str|Union[int,float]", "Union[float,int,str]"),
        ("typing.List[list]", "List[List[Any]]"),
        ("x.Union[list, list]", "List[Any]"),
        ("x.Union[list, tuple]", "Union[List[Any],Tuple[Any,...]]"),
        ("tuple", "Tuple[Any,...]"),
        (COMM, "Tuple[str]"),
        ("x." + COMM, "Tuple[str]"),
        ("Set[tp.Type['MyCls']]", "Set[Type[MyCls]]"),
        ('"MyObj"', "MyObj"),
        ("x.Union[str, Union[Text, Path], Union[Path, str]]", "Union[Path,str]",),
    ],
)
def test_type_cleaner(typestr: str, expected: str) -> None:
    cleaner = ptsp.TypeCleaner()
    output = cleaner.clean(typestr)
    assert output == expected


def test_extract_hints() -> None:
    code = """def blublu(x: int, y=3, t, w: int = 4):
    z: int = x + y
    return z

def blublu2() -> int:
    pass"""
    proc = ptsp.PythonTreeSitterProcessor()
    code2, hints = proc.extract_type_hints(code)
    repl = {h.uid: h.to_string() for h in hints}
    hint0 = hints[0].with_value("Whatever")
    assert hint0.uid == hints[0].uid
    assert hint0.value != hints[0].value
    code3 = code2.format(**repl)
    assert code3 == code
    assert hints[5].name == "blublu.z"
    assert hints[1].default == "3"
    assert hints[0].default is None


def test_extract_hints_method() -> None:
    code = """class Cls:
    def __init__(self):
        self.var: int

    def stuff(self, x):
    """
    proc = ptsp.PythonTreeSitterProcessor()
    code2, hints = proc.extract_type_hints(code)
    repl = {h.uid: h.to_string() for h in hints}
    code3 = code2.format(**repl)
    assert code3 == code
    expected = ("Cls.__init__", "Cls.var", "Cls.stuff.x", "Cls.stuff")
    assert tuple(h.name for h in hints) == expected
