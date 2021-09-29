# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from pathlib import Path

from codegen_sources.preprocessing.lang_processors.cpp_processor import CppProcessor
from codegen_sources.preprocessing.tests.tokenization.tokenization_tests_utils import (
    tokenizer_test,
    detokenize_non_invertible,
    detokenize_invertible,
    tokenize_twice,
    compare_funcs,
)

processor = CppProcessor(root_folder=Path(__file__).parents[4].joinpath("tree-sitter"))

TESTS = []
TESTS.append(
    (
        r"""
// This is a   comment
// ------- ******* -------
int main() {
std::cout << "Hello World!";
return 0;
}""",
        [
            "int",
            "main",
            "(",
            ")",
            "{",
            "std",
            "::",
            "cout",
            "<<",
            '" Hello ▁ World ! "',
            ";",
            "return",
            "0",
            ";",
            "}",
        ],
    )
)

TESTS.append(
    (
        r"""
overload((byte)1);
overload(1L);
overload(1.0f);""",
        [
            "overload",
            "(",
            "(",
            "byte",
            ")",
            "1",
            ")",
            ";",
            "overload",
            "(",
            "1L",
            ")",
            ";",
            "overload",
            "(",
            "1.0f",
            ")",
            ";",
        ],
    )
)

TESTS.append(
    (
        r"""auto glambda = [](auto a, auto&& b) { return a < b; };""",
        [
            "auto",
            "glambda",
            "=",
            "[",
            "]",
            "(",
            "auto",
            "a",
            ",",
            "auto",
            "&&",
            "b",
            ")",
            "{",
            "return",
            "a",
            "<",
            "b",
            ";",
            "}",
            ";",
        ],
    )
)

# test reference, pointor
TESTS.append(
    (
        r""" int a = 0;
int * b = new int(0);
int& ref = a;""",
        [
            "int",
            "a",
            "=",
            "0",
            ";",
            "int",
            "*",
            "b",
            "=",
            "new",
            "int",
            "(",
            "0",
            ")",
            ";",
            "int",
            "&",
            "ref",
            "=",
            "a",
            ";",
        ],
    )
)

# test incrementation - equality/uniquality
TESTS.append(
    (
        r"""a = 0;
b = 0;
a += 10;
a ++;
a --;
a -= 100;
if (a == b) {
    cout<<"yes"<<endl;
}
if (a != b) {
    cout << "no" << endl;
}""",
        [
            "a",
            "=",
            "0",
            ";",
            "b",
            "=",
            "0",
            ";",
            "a",
            "+=",
            "10",
            ";",
            "a",
            "++",
            ";",
            "a",
            "--",
            ";",
            "a",
            "-=",
            "100",
            ";",
            "if",
            "(",
            "a",
            "==",
            "b",
            ")",
            "{",
            "cout",
            "<<",
            '" yes "',
            "<<",
            "endl",
            ";",
            "}",
            "if",
            "(",
            "a",
            "!=",
            "b",
            ")",
            "{",
            "cout",
            "<<",
            '" no "',
            "<<",
            "endl",
            ";",
            "}",
        ],
    )
)

TESTS.append(
    (
        "std::unordered_map<MyCustomObject, std::string> hashmap;",
        [
            "std",
            "::",
            "unordered_map",
            "<",
            "MyCustomObject",
            ",",
            "std",
            "::",
            "string",
            ">",
            "hashmap",
            ";",
        ],
    )
)

TESTS.append(
    (
        r"""string s = "Hi I am\nMarie";""",
        ["string", "s", "=", '" Hi ▁ I ▁ am \\n Marie "', ";"],
    )
)

TESTS_KEEP_COMMENTS = [
    (
        r"""
// This is a comment
// ----------*****
int main() {
std::cout << "Hello World!";
return 0;
}""",
        [
            "// ▁ This ▁ is ▁ a ▁ comment ENDCOM",
            "int",
            "main",
            "(",
            ")",
            "{",
            "std",
            "::",
            "cout",
            "<<",
            '" Hello ▁ World ! "',
            ";",
            "return",
            "0",
            ";",
            "}",
        ],
    ),
    (
        r"""
/* This is a
multiline    comment */
/*----------------this is the docstring */
/* ----*----*-*---- ====== *** */
int main() {
std::cout << "Hello World!";
return 0;
}""",
        [
            "/* ▁ This ▁ is ▁ a STRNEWLINE multiline ▁ comment ▁ */",
            "/* - - - - - this ▁ is ▁ the ▁ docstring ▁ */",
            "int",
            "main",
            "(",
            ")",
            "{",
            "std",
            "::",
            "cout",
            "<<",
            '" Hello ▁ World ! "',
            ";",
            "return",
            "0",
            ";",
            "}",
        ],
    ),
]

TESTS_CHARS = [
    (
        r"""
char a = 'a' ;
""",
        ["char", "a", "=", "' a '", ";"],
    )
]

TESTS_DETOKENIZE_CHARS = [
    (
        "char a = 'a';",
        r"""char a = 'a' ;
""",
    )
]

TESTS_STRINGS = [
    (
        r"""
string s = "Hello !" ;""",
        ["string", "s", "=", f'" Hello ▁ ! "', ";"],
    ),
    (
        r"""
string s = L"Hello !" ;""",
        ["string", "s", "=", f'L" Hello ▁ ! "', ";"],
    ),
]

TESTS_MULTILINE_STRINGS = [
    (
        r"""
string s =
"First line"
"Second line";
""",
        ["string", "s", "=", f'" First ▁ line "', '" Second ▁ line "', ";"],
    )
]

TESTS_DETOKENIZE_MULTILINE_STRINGS = [
    (
        r"""
string s =
"First line"
"Second line";
""",
        r"""string s = "First line" "Second line" ;
""",
    )
]

TESTS_DETOKENIZE_SPECIAL_STRINGS = [
    (
        r'L"Hello world";',
        r"""L"Hello world" ;
""",
    )
]

DETOKENIZE_WITH_DEFINE_TEST = [
    (
        r"""
#define sf scanf
#define pf printf
int main ( ) {
    int i;
    sf ( "%d" , & i ) ;
    pf ( "%d\n" , i ) ;
}""",
        r"""#define sf scanf
#define pf printf
int main ( ) {
  int i ;
  sf ( "%d" , & i ) ;
  pf ( "%d\n" , i ) ;
}
""",
    ),
    (
        r"""#define rep(p, q)  for(int i = p; i < q;i++)""",
        """#define rep( p , q ) for(int i = p; i < q;i++)""",
    ),
]

DETOKENIZE_TESTS = []
DETOKENIZE_TESTS.append(
    (
        r"""
// This is a comment
int main() {
std::cout << "Hello World!";
return 0;
}""",
        r"""int main ( ) {
  std :: cout << "Hello World!" ;
  return 0 ;
}
""",
    )
)

DETOKENIZE_TESTS.append(
    (
        r"""int a = 0;
int * b = new int(0);
int& ref = a;""",
        r"""int a = 0 ;
int * b = new int ( 0 ) ;
int & ref = a ;
""",
    )
)

DETOKENIZE_TESTS.append(
    (
        r"""a = 0;
b = 0
a += 10;
a ++;
a --;
a -= 100;
if (a == b) {
    cout<<"yes"<<endl;
}
if (a != b) {
    cout << "no" << endl;
}
""",
        r"""a = 0 ;
b = 0 a += 10 ;
a ++ ;
a -- ;
a -= 100 ;
if ( a == b ) {
  cout << "yes" << endl ;
}
if ( a != b ) {
  cout << "no" << endl ;
}
""",
    )
)

TESTS_INCLUDES = [
    (
        """// basic file operations
#include <iostream>
#include <fstream>
using namespace std;

int main () {
  ofstream myfile;
  myfile.open ("example.txt");
  myfile << "Writing this to a file.\n";
  myfile.close();
  return 0;
}""",
        [
            "#include",
            "<iostream>",
            "NEW_LINE",
            "#include",
            "<fstream>",
            "NEW_LINE",
            "using",
            "namespace",
            "std",
            ";",
            "int",
            "main",
            "(",
            ")",
            "{",
            "ofstream",
            "myfile",
            ";",
            "myfile",
            ".",
            "open",
            "(",
            '" example . txt "',
            ")",
            ";",
            "myfile",
            "<<",
            '" Writing ▁ this ▁ to ▁ a ▁ file . STRNEWLINE "',
            ";",
            "myfile",
            ".",
            "close",
            "(",
            ")",
            ";",
            "return",
            "0",
            ";",
            "}",
        ],
    ),
    (
        '#include "berryDefaultActivator.h"\n\nnamespace berry {\n\nvoid\nDefaultActivator::Start(IBundleContext::Pointer /*context*/)\n{\n\n}\n\nvoid\nDefaultActivator::Stop(IBundleContext::Pointer /*context*/)\n{\n\n}\n\n}\n',
        [
            "#include",
            '" berryDefaultActivator . h "',
            "NEW_LINE",
            "namespace",
            "berry",
            "{",
            "void",
            "DefaultActivator",
            "::",
            "Start",
            "(",
            "IBundleContext",
            "::",
            "Pointer",
            ")",
            "{",
            "}",
            "void",
            "DefaultActivator",
            "::",
            "Stop",
            "(",
            "IBundleContext",
            "::",
            "Pointer",
            ")",
            "{",
            "}",
            "}",
        ],
    ),
]

TESTS_DETOKENIZE_INCLUDES = [
    (
        r"""// basic file operations
#include <iostream>
#include <fstream>
using namespace std;

int main () {
  ofstream myfile;
  myfile.open ("example.txt");
  myfile << "Writing this to a file.\n";
  myfile.close();
  return 0;
}""",
        r"""#include <iostream>
#include <fstream>
using namespace std ;
int main ( ) {
  ofstream myfile ;
  myfile . open ( "example.txt" ) ;
  myfile << "Writing this to a file.\n" ;
  myfile . close ( ) ;
  return 0 ;
}
""",
    )
]


def test_cpp_tokenizer_discarding_comments():
    tokenizer_test(TESTS, processor, keep_comments=False)


def test_cpp_tokenizer_keep_comments():
    tokenizer_test(TESTS_KEEP_COMMENTS, processor, keep_comments=True)


def test_cpp_chars():
    tokenizer_test(TESTS_CHARS, processor, keep_comments=False)


def test_detokenize_chars():
    detokenize_non_invertible(TESTS_DETOKENIZE_CHARS, processor)


def test_cpp_strings():
    tokenizer_test(
        TESTS_STRINGS + TESTS_MULTILINE_STRINGS, processor, keep_comments=False
    )


def test_cpp_includes():
    tokenizer_test(TESTS_INCLUDES, processor, keep_comments=False)


def test_detokenize_includes():
    detokenize_non_invertible(TESTS_DETOKENIZE_INCLUDES, processor)


def test_cpp_detokenize():
    detokenize_non_invertible(DETOKENIZE_TESTS, processor)


def test_cpp_detokenize_defines():
    detokenize_non_invertible(DETOKENIZE_WITH_DEFINE_TEST, processor)


def test_detokenize_cpp_chars():
    detokenize_invertible(TESTS_CHARS, processor)


def test_detokenize_string():
    detokenize_invertible(TESTS_STRINGS, processor)


def test_detokenize_multiline_string():
    detokenize_non_invertible(TESTS_DETOKENIZE_MULTILINE_STRINGS, processor)


def test_detokenize_special_string():
    detokenize_non_invertible(TESTS_DETOKENIZE_SPECIAL_STRINGS, processor)


def test_tokenize_twice_equal_tokenize_remove_comments():
    tokenize_twice(TESTS + TESTS_STRINGS + TESTS_CHARS, processor)


def test_tokenize_twice_equal_tokenize_keep_comments():
    tokenize_twice(
        TESTS + TESTS_STRINGS + TESTS_CHARS + TESTS_KEEP_COMMENTS,
        processor,
        keep_comments=True,
    )


TEST_FUNC_EXTRACTION = [
    (
        """class Room {
    public:
        double length;
        double breadth;
        double height;

        double calculateArea(){
            return length * breadth;
        }

        double calculateVolume(){
            return length * breadth * height;
        }

};
// sample function
void sampleFunction() {
    // create objects
    Room room1, room2;
}
""",
        [
            ["void sampleFunction ( ) { Room room1 , room2 ; }"],
            [
                "double calculateArea ( ) { return length * breadth ; }",
                "double calculateVolume ( ) { return length * breadth * height ; }",
            ],
        ],
    ),
    (
        """#include<iostream>

int main(){
    return 0;
}
""",
        (["int main ( ) { return 0 ; }"], []),
    ),
    (
        """#include<cstdio>
#include<cstring>
#include<cstdlib>
#include<algorithm>
#include<set>
using namespace std;

#define mem(Arr,x) memset(Arr,x,sizeof(Arr))
const int maxN=1010000*2;
const int maxM=maxN<<1;
const int Mod=1e9+7;
int n;
pair<int,int> P[maxN];
set<pair<int,int> > S;
int Nxt[maxN],St[maxN],vis[maxN];
int edgecnt=-1,Head[maxN],Next[maxM],V[maxM];

void Add_Edge(int u,int v);
void dfs(int u,int w);
int func0()
{
	return 0;
}
int func1(int u,int v)
{
	return 1; 
}
void func2()
{
	return
}""",
        (
            [
                "int func0 ( ) { return 0 ; }",
                "int func1 ( int u , int v ) { return 1 ; }",
                "void func2 ( ) { return }",
            ],
            [],
        ),
    ),
]


def test_extract_cpp_functions():
    for input_file, expected_funcs in TEST_FUNC_EXTRACTION:
        actual_funcs_sa, actual_funcs_cl = processor.extract_functions(
            processor.tokenize_code(input_file)
        )
        print(actual_funcs_sa, actual_funcs_cl)
        expected_sa, expected_cl = expected_funcs
        compare_funcs(actual_funcs_sa, expected_sa)
        compare_funcs(actual_funcs_cl, expected_cl)
