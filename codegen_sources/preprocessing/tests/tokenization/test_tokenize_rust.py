# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from codegen_sources.preprocessing.lang_processors import RustProcessor
from codegen_sources.preprocessing.tests.tokenization.tokenization_tests_utils import (
    compare_funcs,
    detokenize_invertible,
    detokenize_non_invertible,
    tokenize_twice,
    tokenizer_test,
)

processor = RustProcessor()


TESTS = []
TESTS.append(
    (
        r"""
// This is a   comment
// ------- ******* -------
fn main() {
    println!("Hello World!");
}""",
        [
            "fn",
            "main",
            "(",
            ")",
            "{",
            "println",
            "!",
            "(",
            '" Hello ▁ World ! "',
            ")",
            ";",
            "}",
        ],
    )
)

TESTS.append(
    (
        r"""
/* This is a multiline comment
// ------- ******* ------- */
fn main() {
    println!("Hello World!");
}""",
        [
            "fn",
            "main",
            "(",
            ")",
            "{",
            "println",
            "!",
            "(",
            '" Hello ▁ World ! "',
            ")",
            ";",
            "}",
        ],
    )
)


TESTS.append(
    (
        r"""let closure_annotated = |i: i32| -> i32 { i + 1 };""",
        [
            "let",
            "closure_annotated",
            "=",
            "|",
            "i",
            ":",
            "i32",
            "|",
            "->",
            "i32",
            "{",
            "i",
            "+",
            "1",
            "}",
            ";",
        ],
    )
)

# test reference, pointor
TESTS.append(
    (
        r"""let a: i32 = 10;
let a_ptr: *const i32 = &a;
""",
        [
            "let",
            "a",
            ":",
            "i32",
            "=",
            "10",
            ";",
            "let",
            "a_ptr",
            ":",
            "*",
            "const",
            "i32",
            "=",
            "&",
            "a",
            ";",
        ],
    )
)

TESTS.append(
    (
        """use std::collections::HashMap;
let mut book_reviews = HashMap::new();
book_reviews.insert(
    "b1".to_string(),
    "My favorite book.".to_string(),
);""",
        [
            "use",
            "std",
            "::",
            "collections",
            "::",
            "HashMap",
            ";",
            "let",
            "mut",
            "book_reviews",
            "=",
            "HashMap",
            "::",
            "new",
            "(",
            ")",
            ";",
            "book_reviews",
            ".",
            "insert",
            "(",
            '" b1"',
            ".",
            "to_string",
            "(",
            ")",
            ",",
            '" My ▁ favorite ▁ book . "',
            ".",
            "to_string",
            "(",
            ")",
            ",",
            ")",
            ";",
        ],
    )
)


TESTS.append(
    (
        r"""let s = "Hi I am\nMarie";""",
        ["let", "s", "=", '" Hi ▁ I ▁ am \\n Marie "', ";"],
    )
)

TESTS_PRINTING = [
    (
        r"""println!("{}", var1 + var2);""",
        ["println", "!", "(", '" { } "', ",", "var1", "+", "var2", ")", ";"],
    )
]

TESTS_KEEP_COMMENTS = [
    (
        r"""
// This is a comment
// ----------*****
fn main() {
    println!("Hello World!");
}""",
        [
            "// ▁ This ▁ is ▁ a ▁ comment ENDCOM",
            "fn",
            "main",
            "(",
            ")",
            "{",
            "println",
            "!",
            "(",
            '" Hello ▁ World ! "',
            ")",
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
fn main() {
    println!("Hello World!");
}""",
        [
            "/* ▁ This ▁ is ▁ a STRNEWLINE multiline ▁ comment ▁ */",
            "/* - - - - - this ▁ is ▁ the ▁ docstring ▁ */",
            "fn",
            "main",
            "(",
            ")",
            "{",
            "println",
            "!",
            "(",
            '" Hello ▁ World ! "',
            ")",
            ";",
            "}",
        ],
    ),
]

TESTS_CHARS = [
    (
        r"""
let a_char = 'a' ;
""",
        ["let", "a_char", "=", "' a '", ";"],
    )
]

TESTS_STRINGS = [
    (
        r"""
let s = "Hello !" ;""",
        ["let", "s", "=", f'" Hello ▁ ! "', ";"],
    ),
]

TESTS_MULTILINE_STRINGS = [
    (
        r"""
let s =
"First line
Second line \
End second line";
""",
        [
            "let",
            "s",
            "=",
            '" First ▁ line STRNEWLINE Second ▁ line ▁ \\ STRNEWLINE End ▁ second ▁ line "',
            ";",
        ],
    )
]

TESTS_DETOKENIZE_MULTILINE_STRINGS = [
    (
        r"""
let s =
"First line
Second line \
End second line";
""",
        r"""let s = "First line
Second line \
End second line" ;
""",
    )
]

DETOKENIZE_TESTS = []
DETOKENIZE_TESTS.append(
    (
        r"""
// This is a comment
fn main() {
    println!("Hello World!");
}
""",
        r"""fn main ( ) {
  println ! ( "Hello World!" ) ;
}
""",
    )
)

DETOKENIZE_TESTS.append(
    (
        r"""let a : i32 = 10;
let a_ptr : *const i32 = &a;
""",
        r"""let a : i32 = 10 ;
let a_ptr : * const i32 = & a ;
""",
    )
)


def test_rust_tokenizer_discarding_comments():
    tokenizer_test(TESTS, processor, keep_comments=False)


def test_print_tokenization():
    tokenizer_test(TESTS_PRINTING, processor, keep_comments=False)


def test_rust_tokenizer_keep_comments():
    tokenizer_test(TESTS_KEEP_COMMENTS, processor, keep_comments=True)


def test_rust_chars():
    tokenizer_test(TESTS_CHARS, processor, keep_comments=False)


def test_rust_strings():
    tokenizer_test(
        TESTS_STRINGS + TESTS_MULTILINE_STRINGS, processor, keep_comments=False
    )


def test_rust_detokenize():
    detokenize_non_invertible(DETOKENIZE_TESTS, processor)


def test_detokenize_rust_chars():
    detokenize_invertible(TESTS_CHARS, processor)


def test_detokenize_string():
    detokenize_invertible(TESTS_STRINGS, processor)


def test_detokenize_multiline_string():
    detokenize_non_invertible(TESTS_DETOKENIZE_MULTILINE_STRINGS, processor)


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
        """struct Point {
    x: f64,
    y: f64,
}

// Implementation block, all `Point` methods go in here
impl Point {
    // This is a static method
    // Static methods don't need to be called by an instance
    // These methods are generally used as constructors
    fn origin() -> Point {
        Point { x: 0.0, y: 0.0 }
    }

    // Another static method, taking two arguments:
    fn new(x: f64, y: f64) -> Point {
        Point { x: x, y: y }
    }
}
fn hello() {
    println!("Hello World!");
}""",
        [
            ["""fn hello ( ) { println ! ( " Hello ▁ World ! " ) ; }"""],
            [
                "fn origin ( ) -> Point { Point { x : 0.0 , y : 0.0 } }",
                "fn new ( x : f64 , y : f64 ) -> Point { Point { x : x , y : y } }",
            ],
        ],
    ),
    (
        """trait Quack {
    fn quack(&self);
}

struct Duck ();

impl Quack for Duck {
    fn quack(&self) {
        println!("quack!");
    }
}

struct RandomBird {
    is_a_parrot: bool
}

impl Quack for RandomBird {
    fn quack(&self) {
        if ! self.is_a_parrot {
            println!("quack!");
        } else {
            println!("squawk!");
        }
    }
}

let duck1 = Duck();
let duck2 = RandomBird{is_a_parrot: false};
let parrot = RandomBird{is_a_parrot: true};

let ducks: Vec<&Quack> = vec![&duck1,&duck2,&parrot];

for d in &ducks {
    d.quack();
}""",
        [
            [],
            [
                'fn quack ( & self ) { println ! ( " quack ! " ) ; }',
                'fn quack ( & self ) { if ! self . is_a_parrot { println ! ( " quack ! " ) ; } else { println ! ( " squawk ! " ) ; } }',
            ],
        ],
    ),
]


def test_extract_rust_functions():
    for input_file, expected_funcs in TEST_FUNC_EXTRACTION:
        actual_funcs_sa, actual_funcs_cl = processor.extract_functions(
            processor.tokenize_code(input_file)
        )
        print(actual_funcs_sa, actual_funcs_cl)
        expected_sa, expected_cl = expected_funcs
        compare_funcs(actual_funcs_sa, expected_sa)
        compare_funcs(actual_funcs_cl, expected_cl)
