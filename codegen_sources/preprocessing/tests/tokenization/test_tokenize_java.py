# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import pytest

from codegen_sources.preprocessing.lang_processors.java_processor import JavaProcessor
from pathlib import Path

from codegen_sources.preprocessing.tests.tokenization.tokenization_tests_utils import (
    tokenizer_test,
    detokenize_non_invertible,
    detokenize_invertible,
    compare_funcs,
)

processor = JavaProcessor(root_folder=Path(__file__).parents[4].joinpath("tree-sitter"))
TESTS = []

TESTS.append(
    (
        r"""
public class HelloWorld
{
	public void main(String[] args) {
		System.out.println("Hello \n World!");
	}
}""",
        [
            "public",
            "class",
            "HelloWorld",
            "{",
            "public",
            "void",
            "main",
            "(",
            "String",
            "[",
            "]",
            "args",
            ")",
            "{",
            "System",
            ".",
            "out",
            ".",
            "println",
            "(",
            '" Hello ▁ \\n ▁ World ! "',
            ")",
            ";",
            "}",
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
        r"""Runnable r = ()-> System.out.print("Run method");""",
        [
            "Runnable",
            "r",
            "=",
            "(",
            ")",
            "->",
            "System",
            ".",
            "out",
            ".",
            "print",
            "(",
            '" Run ▁ method "',
            ")",
            ";",
        ],
    )
)

TESTS.append(
    (
        r"""String s = "Hi I am\nMarie";""",
        ["String", "s", "=", '" Hi ▁ I ▁ am \\n Marie "', ";"],
    )
)


TESTS2 = []

TESTS2.append(
    r"""
import java.util.concurrent.TimeUnit;

public class Mensuration{ //mensuration of a child

    private int height;
    private int weight;
    private String child_name;

    public Mensuration(int height, int weight, String name):{
        this.height = height;
        this.weight = weight;
        this.child_name = name;
    }

    public int get_height(){
        return height;
    }

    public int get_weight(){
        return weight;
    }

    public String get_name(){
        String s = "Name:\n" + child_name;
        return s;
    }

}"""
)

TESTS2.append(
    r"""
private enum Answer {
  YES {
    @Override public String toString() {
      return "yes";
    }
  },
  NO,
  MAYBE
}"""
)

TESTS2.append(
    r"""
return new MyClass() {
  @Override public void method() {
    if (condition()) {
      try {
        something();
      } catch (ProblemException e) {
        recover();
      }
    } else if (otherCondition()) {
      somethingElse();
    } else {
      lastThing();
    }
  }
};"""
)

TESTS2.append(
    r"""
public boolean equals(Object o_) {

      if ( o_ == null ) {
        return false;
      }
      if ( o_.getClass() != this.getClass() ) {
        return false;
      }
      Pair<?, ?> o = (Pair<?, ?>) o_;
      return x.equals(o.x) && y.equals(o.y);
    }
  }
"""
)

TESTS3 = []

TESTS3.append(
    (
        r"""/*
This    is    the    docstring !!
*/
/* ---------- */
public class HelloWorld
{
	public void main(String[] args) {
		System.out.println("Hello \n World!");
	}
}""",
        [
            "/* STRNEWLINE This ▁ is ▁ the ▁ docstring ▁ ! ! STRNEWLINE */",
            "public",
            "class",
            "HelloWorld",
            "{",
            "public",
            "void",
            "main",
            "(",
            "String",
            "[",
            "]",
            "args",
            ")",
            "{",
            "System",
            ".",
            "out",
            ".",
            "println",
            "(",
            '" Hello ▁ \\n ▁ World ! "',
            ")",
            ";",
            "}",
            "}",
        ],
    )
)

TESTS3.append(
    (
        r"""
overload((byte)1);
// this is my  comfff
// ----- ***
overload(1L); // this is my comfff
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
            "// ▁ this ▁ is ▁ my ▁ comfff ENDCOM",
            "overload",
            "(",
            "1L",
            ")",
            ";",
            "// ▁ this ▁ is ▁ my ▁ comfff ENDCOM",
            "overload",
            "(",
            "1.0f",
            ")",
            ";",
        ],
    )
)

TESTS_TOKENIZE_DETOKENIZE_STRING = [
    (
        r"""public int read ( ) throws IOException {
  int current = super . read ( ) ;
  if ( current == '\r' || ( current == '\n' && lastChar != '\r' ) ) {
    lineCounter ++ ;
  }
  lastChar = current ;
  return lastChar ;
}""",
        """""",
    ),
    (
        r"""public int curly_brackets ( ) throws IOException {
  System . out . println ( "This } is the output" ) ;
  System . out . println ( "This {} is the output" ) ;
  System . out . println ( '}' ) ;
}""",
        """""",
    ),
    (
        r"""public int commas ( ) throws IOException {
  System . out . println ( "This ; is the output" ) ;
  System . out . println ( "This , is the output" ) ;
  System . out . println ( ';' ) ;
  System . out . println ( ',' ) ;
}""",
        """""",
    ),
    (
        r"""public void inException ( ) {
  throw new IllegalArgumentException ( "Type \'" + typeToEvaluate + "\' is not a Class, " + "ParameterizedType, GenericArrayType or TypeVariable. Can't extract type." ) ;
}
""",
        """""",
    ),
]

TESTS_DONT_PROCESS_STRINGS = [
    (
        r"""
public class HelloWorld
{
    // This is a comment
	public void main(String[] args) {
		System.out.println("Hello \n World!");
	}
}""",
        [
            "public",
            "class",
            "HelloWorld",
            "{",
            "// This is a comment ENDCOM",
            "public",
            "void",
            "main",
            "(",
            "String",
            "[",
            "]",
            "args",
            ")",
            "{",
            "System",
            ".",
            "out",
            ".",
            "println",
            "(",
            '"Hello \\n World!"',
            ")",
            ";",
            "}",
            "}",
        ],
    ),
    (
        r"""
    public class HelloEarth
    {
        /* This is a
        multiline
        comment */
        public void main(String[] args) {
            System.out.println("Hello \nEarth!");
        }
    }""",
        [
            "public",
            "class",
            "HelloEarth",
            "{",
            "/* This is a\\n multiline\\n comment */",
            "public",
            "void",
            "main",
            "(",
            "String",
            "[",
            "]",
            "args",
            ")",
            "{",
            "System",
            ".",
            "out",
            ".",
            "println",
            "(",
            '"Hello \\nEarth!"',
            ")",
            ";",
            "}",
            "}",
        ],
    ),
]

TESTS_BACK_R_CHAR = [
    (
        """
public class HelloWorld
{\r
	public void main(String[] args) {
		System.out.println("Hello \rWorld!");
	}
}""",
        [
            "public",
            "class",
            "HelloWorld",
            "{",
            "public",
            "void",
            "main",
            "(",
            "String",
            "[",
            "]",
            "args",
            ")",
            "{",
            "System",
            ".",
            "out",
            ".",
            "println",
            "(",
            '"Hello World!"',
            ")",
            ";",
            "}",
            "}",
        ],
    )
]

TESTS_IMPORTS = [
    (
        (
            r"""
import java.lang.*;
import javafx.util.Pair;
public class HelloWorld
{
	public void main(String[] args) {
		System.out.println("Hello \n World!");
	}
}""",
            [
                "import",
                "java",
                ".",
                "lang",
                ".",
                "*",
                ";",
                "import",
                "javafx",
                ".",
                "util",
                ".",
                "Pair",
                ";",
                "public",
                "class",
                "HelloWorld",
                "{",
                "public",
                "void",
                "main",
                "(",
                "String",
                "[",
                "]",
                "args",
                ")",
                "{",
                "System",
                ".",
                "out",
                ".",
                "println",
                "(",
                '" Hello ▁ \\n ▁ World ! "',
                ")",
                ";",
                "}",
                "}",
            ],
        )
    )
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
        r"char a='a';",
        r"""char a = 'a' ;
""",
    )
]


def test_java_tokenizer_discarding_comments():
    for i, (x, y) in enumerate(TESTS):
        y_ = processor.tokenize_code(x)
        if y_ != y:
            line_diff = [
                j for j, (line, line_) in enumerate(zip(y, y_)) if line != line_
            ]
            line_diff = line_diff[-1] if len(line_diff) > 0 else -1
            raise Exception(
                f"Difference at {line_diff}\nExpected:\n==========\n{y}\nbut found:\n==========\n{y_}"
            )


def test_tokenize_imports():
    for i, (x, y) in enumerate(TESTS_IMPORTS):
        y_ = processor.tokenize_code(x)
        if y_ != y:
            line_diff = [
                j for j, (line, line_) in enumerate(zip(y, y_)) if line != line_
            ]
            line_diff = line_diff[-1] if len(line_diff) > 0 else -1
            raise Exception(
                f"Difference at {line_diff}\nExpected:\n==========\n{y}\nbut found:\n==========\n{y_}"
            )


def test_java_detokenizer_discarding_comments():
    for i, x in enumerate([x[0] for x in TESTS] + [x[0] for x in TESTS3] + TESTS2):
        tokens = processor.tokenize_code(x)
        x_ = processor.detokenize_code(tokens)
        tokens_ = processor.tokenize_code(x_)
        if tokens != tokens:
            line_diff = [
                j
                for j, (line, line_) in enumerate(zip(tokens, tokens_))
                if line != line_
            ]
            raise Exception(
                f"Difference at {line_diff}\n========== Original:\n{x}\n========== Tokenized {tokens} \n Detokenized:\n{x_} \n Retokenized {tokens_}"
            )


def test_java_tokenizer_keeping_comments():
    for i, (x, y) in enumerate(TESTS3):
        y_ = processor.tokenize_code(x, keep_comments=True)
        if y_ != y:
            line_diff = [
                j for j, (line, line_) in enumerate(zip(y, y_)) if line != line_
            ]
            line_diff = line_diff[-1] if len(line_diff) > 0 else -1
            raise Exception(
                f"Difference at {line_diff}\nExpected:\n==========\n{y}\nbut found:\n==========\n{y_}"
            )


def test_dont_process_strings():
    for i, (x, y) in enumerate(TESTS_DONT_PROCESS_STRINGS):
        y_ = processor.tokenize_code(x, keep_comments=True, process_strings=False)
        print(y_)
        if y_ != y:
            line_diff = [
                j for j, (line, line_) in enumerate(zip(y, y_)) if line != line_
            ]
            line_diff = line_diff[-1] if len(line_diff) > 0 else -1
            raise Exception(
                f"Difference at {line_diff}\nExpected:\n==========\n{y}\nbut found:\n==========\n{y_}"
            )


def test_backr_chars():
    for i, (x, y) in enumerate(TESTS_BACK_R_CHAR):
        y_ = processor.tokenize_code(x, keep_comments=True, process_strings=False)
        print(y_)
        if y_ != y:
            line_diff = [
                j for j, (line, line_) in enumerate(zip(y, y_)) if line != line_
            ]
            line_diff = line_diff[-1] if len(line_diff) > 0 else -1
            raise Exception(
                f"Difference at {line_diff}\nExpected:\n==========\n{y}\nbut found:\n==========\n{y_}"
            )


def test_java_detokenizer_keeping_comments():
    for i, x in enumerate([x[0] for x in TESTS] + [x[0] for x in TESTS3] + TESTS2):
        tokens = processor.tokenize_code(x, keep_comments=True)
        x_ = processor.detokenize_code(tokens)
        tokens_ = processor.tokenize_code(x_, keep_comments=True)
        if tokens != tokens_:
            line_diff = [
                j
                for j, (line, line_) in enumerate(zip(tokens, tokens_))
                if line != line_
            ]
            raise Exception(
                f"Difference at {line_diff}\n========== Original:\n{x}\n========== Tokenized {tokens} \n Detokenized:\n{x_} \n Retokenized {tokens_}"
            )


def test_tokenize_detokenize():
    detokenize_invertible(TESTS_TOKENIZE_DETOKENIZE_STRING, processor)


def test_java_chars():
    tokenizer_test(TESTS_CHARS, processor, keep_comments=False)


def test_detokenize_chars():
    detokenize_non_invertible(TESTS_DETOKENIZE_CHARS, processor)


FUNC_EXTRACTION = [
    (
        """
@SuppressWarnings("resource")
public class Main {
	public static void main(String args[]) {
	return 0;
	}
}""",
        (["public static void main ( String args [ ] ) { return 0 ; }"], []),
    ),
    (
        """
public class Room {
    double length;
    double breadth;

	public static int return_zero() {
	return 0;
	}
	public double area(){
	    return length * breadth;
	}
}""",
        [
            ["public static int return_zero ( ) { return 0 ; }"],
            ["public double area ( ) { return length * breadth ; }"],
        ],
    ),
]


def test_extract_java_functions():
    for input_file, expected_funcs in FUNC_EXTRACTION:
        actual_funcs_sa, actual_funcs_cl = processor.extract_functions(
            processor.tokenize_code(input_file)
        )
        print(actual_funcs_sa, actual_funcs_cl)
        expected_sa, expected_cl = expected_funcs
        compare_funcs(actual_funcs_sa, expected_sa)
        compare_funcs(actual_funcs_cl, expected_cl)
