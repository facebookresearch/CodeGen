# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from pathlib import Path

import pytest
from codegen_sources.preprocessing.lang_processors.javascript_processor import (
    JavascriptProcessor,
)

processor = JavascriptProcessor(
    root_folder=Path(__file__).parents[4].joinpath("tree-sitter")
)

TESTS_COMMENTS_STRINGS = []

TESTS_COMMENTS_STRINGS.append(
    (
        r"""
function myFunction() { // Declare a function
  document.getElementById("demo").innerHTML = "Hello World!";
}

myFunction(); // Call the function""",
        [
            "function",
            "myFunction",
            "(",
            ")",
            "{",
            "document",
            ".",
            "getElementById",
            "(",
            '" demo "',
            ")",
            ".",
            "innerHTML",
            "=",
            '" Hello ▁ World ! "',
            ";",
            "}",
            "myFunction",
            "(",
            ")",
            ";",
        ],
    )
)

TESTS_COMMENTS_STRINGS.append(
    (
        r"""
public function getExample(): string {
    return static::METADATA['example'];
}""",
        [
            "public",
            "function",
            "getExample",
            "(",
            ")",
            ":",
            "string",
            "{",
            "return",
            "static",
            ":",
            ":",
            "METADATA",
            "[",
            "' example '",
            "]",
            ";",
            "}",
        ],
    )
)

TESTS_COMMENTS_STRINGS.append(
    (
        r"""
function myFunction(p1, p2) {
  return p1 * p2;   // The function returns the product of p1 and p2
}""",
        [
            "function",
            "myFunction",
            "(",
            "p1",
            ",",
            "p2",
            ")",
            "{",
            "return",
            "p1",
            "*",
            "p2",
            ";",
            "}",
        ],
    )
)


TESTS2 = []

TESTS2.append(
    r"""
BmpDecoder.prototype.parseBGR = function() {
  this.pos = this.offset;
  try {
    var bitn = "bit" + this.bitPP;
    var len = this.width * this.height * 4;
    this.data = new Uint8Array(len);

    this[bitn]();
  } catch (e) {
    console.log("bit decode error:" + e);
  }
};

BmpDecoder.prototype.bit1 = function() {
  var xlen = Math.ceil(this.width / 8);
  var mode = xlen % 4;
  var y;
  for (y = this.height - 1; y >= 0; y--) {
    var line = this.bottom_up ? y : this.height - 1 - y;
    for (var x = 0; x < xlen; x++) {
      var b = this.datav.getUint8(this.pos++, true);
      var location = line * this.width * 4 + x * 8 * 4;
      for (var i = 0; i < 8; i++) {
        if (x * 8 + i < this.width) {
          var rgb = this.palette[(b >> (7 - i)) & 0x1];
          this.data[location + i * 4] = rgb.blue;
          this.data[location + i * 4 + 1] = rgb.green;
          this.data[location + i * 4 + 2] = rgb.red;
          this.data[location + i * 4 + 3] = 0xff;
        } else {
          break;
        }
      }
    }
"""
)

# The tests below use java code. We may need to replace them if we find out that javascript tokenization should be different in similar cases
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
overload(1); // this is my comfff
""",
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
            "1",
            ")",
            ";",
            "// ▁ this ▁ is ▁ my ▁ comfff ENDCOM",
        ],
    )
)

TESTS_TOKENIZE_DETOKENIZE_STRING = [
    r"""public int read ( ) throws IOException {
  int current = super . read ( ) ;
  if ( current == '\r' || ( current == '\n' && lastChar != '\r' ) ) {
    lineCounter ++ ;
  }
  lastChar = current ;
  return lastChar ;
}""",
    r"""public int curly_brackets ( ) throws IOException {
  System . out . println ( "This } is the output" ) ;
  System . out . println ( "This {} is the output" ) ;
  System . out . println ( '}' ) ;
}""",
    r"""public int commas ( ) throws IOException {
  System . out . println ( "This ; is the output" ) ;
  System . out . println ( "This , is the output" ) ;
  System . out . println ( ';' ) ;
  System . out . println ( ',' ) ;
}""",
    r"""public void inException ( ) {
  throw new IllegalArgumentException ( "Type \'" + typeToEvaluate + "\' is not a Class, " + "ParameterizedType, GenericArrayType or TypeVariable. Can't extract type." ) ;
}
""",
]


def test_javascript_tokenizer_discarding_comments():
    for i, (x, y) in enumerate(TESTS_COMMENTS_STRINGS):
        y_ = processor.tokenize_code(x)
        if y_ != y:
            line_diff = [
                j for j, (line, line_) in enumerate(zip(y, y_)) if line != line_
            ]
            line_diff = line_diff[-1] if len(line_diff) > 0 else -1
            raise Exception(
                f"Difference at {line_diff}\nExpected:\n==========\n{y}\nbut found:\n==========\n{y_}"
            )


def test_javascript_detokenizer_discarding_comments():
    for i, x in enumerate(
        [x[0] for x in TESTS_COMMENTS_STRINGS] + [x[0] for x in TESTS3] + TESTS2
    ):
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


def test_javascript_tokenizer_keeping_comments():
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


def test_javascript_detokenizer_keeping_comments():
    for i, x in enumerate(
        [x[0] for x in TESTS_COMMENTS_STRINGS] + [x[0] for x in TESTS3] + TESTS2
    ):
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
    test_detokenize_invertible(TESTS_TOKENIZE_DETOKENIZE_STRING)


@pytest.mark.skip("Helper function")
def test_detokenize_invertible(test_examples):
    for i, x in enumerate(test_examples):
        x_ = processor.detokenize_code(processor.tokenize_code(x, keep_comments=True))
        if x_.strip() != x.strip():
            raise Exception(
                f"Expected:\n==========\n{x.strip()}\nbut found:\n==========\n{x_.strip()}"
            )
