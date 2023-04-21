# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from codegen_sources.preprocessing.lang_processors import GoProcessor
from codegen_sources.preprocessing.tests.tokenization.tokenization_tests_utils import (
    compare_funcs,
    detokenize_invertible,
    detokenize_non_invertible,
    tokenize_twice,
    tokenizer_test,
)

processor = GoProcessor()


TESTS = []
TESTS.append(
    (
        r"""
func main() {
    fmt.Println("hello world")
}""",
        [
            "func",
            "main",
            "(",
            ")",
            "{",
            "fmt",
            ".",
            "Println",
            "(",
            '" hello ▁ world "',
            ")",
            "NEW_LINE",
            "}",
        ],
    )
)

TESTS.append(
    (
        r"""
/* This is a multiline comment
// ------- ******* ------- */
func main() {
    fmt.Println("hello world")
}""",
        [
            "func",
            "main",
            "(",
            ")",
            "{",
            "fmt",
            ".",
            "Println",
            "(",
            '" hello ▁ world "',
            ")",
            "NEW_LINE",
            "}",
        ],
    )
)


TESTS.append(
    (r"""var b, c int = 1, 2""", ["var", "b", ",", "c", "int", "=", "1", ",", "2"],)
)

# test reference, pointor
TESTS.append(
    (
        r"""var a = 10
*a_ptr := &a""",
        ["var", "a", "=", "10", "NEW_LINE", "*", "a_ptr", ":=", "&", "a"],
    )
)

TESTS.append((r"""s := "Hi I am\nMarie" """, ["s", ":=", '" Hi ▁ I ▁ am \\n Marie "'],))

TESTS_KEEP_COMMENTS = [
    (
        r"""
// This is a comment
// ----------*****
func main() {
    fmt.Println("hello world")
}""",
        [
            "// ▁ This ▁ is ▁ a ▁ comment ENDCOM",
            "func",
            "main",
            "(",
            ")",
            "{",
            "fmt",
            ".",
            "Println",
            "(",
            '" hello ▁ world "',
            ")",
            "NEW_LINE",
            "}",
        ],
    ),
]


TEST_FUNC_EXTRACTION = [
    (
        r"""
package Main

func Get_sum(num1 int, num2 int) int {
  var num3 = num1 + num2
  return num3
}

""",
        [
            [
                "func Get_sum ( num1 int , num2 int ) int { var num3 = num1 + num2 NEW_LINE return num3 NEW_LINE }"
            ],
            [],
        ],
    ),
    (
        r"""
 package doubleLinkedList

type List struct {
    head, tail *Node
}

type Node struct {
    value      string
    next, prev *Node
}

func (l *List) First() *Node {
    return l.head
}

func (n *Node) Next() *Node {
    return n.next
}

func (n *Node) Prev() *Node {
    return n.prev
}

func (l *List) Push(val string) *List {
    n := &Node{value: val}
    if l.head == nil { //first node
        l.head = n
    } else {
        l.tail.next = n
        n.prev = l.tail
    }

    l.tail = n
    return l
}

func (l *List) Pop() string {
    if l.tail == nil {
        return ""
    }
    value := l.tail.value
    l.tail = l.tail.prev
    if l.tail == nil {
        l.head = nil
    }
    return value
}

func (l *List) Find(val string) *Node {
    for n := l.First(); n != nil; n = n.Next() {
        if n.value == val {
            return n
        }
    }
    return nil
}

func (l *List) Erase(val string) bool {
    node := l.Find(val)
    if node != nil {
        node.prev.next = node.next
        node.next.prev = node.prev
        return true
    }
    return false
}
""",
        [
            [
                "func ( l * List ) First ( ) * Node { return l . head NEW_LINE }",
                "func ( n * Node ) Next ( ) * Node { return n . next NEW_LINE }",
                "func ( n * Node ) Prev ( ) * Node { return n . prev NEW_LINE }",
                "func ( l * List ) Push ( val string ) * List { n := & Node { value : val } NEW_LINE if l . head == nil { l . head = n NEW_LINE } else { l . tail . next = n NEW_LINE n . prev = l . tail NEW_LINE } NEW_LINE l . tail = n NEW_LINE return l NEW_LINE }",
                'func ( l * List ) Pop ( ) string { if l . tail == nil { return " " NEW_LINE } NEW_LINE value := l . tail . value NEW_LINE l . tail = l . tail . prev NEW_LINE if l . tail == nil { l . head = nil NEW_LINE } NEW_LINE return value NEW_LINE }',
                "func ( l * List ) Find ( val string ) * Node { for n := l . First ( ) ; n != nil ; n = n . Next ( ) { if n . value == val { return n NEW_LINE } NEW_LINE } NEW_LINE return nil NEW_LINE }",
                "func ( l * List ) Erase ( val string ) bool { node := l . Find ( val ) NEW_LINE if node != nil { node . prev . next = node . next NEW_LINE node . next . prev = node . prev NEW_LINE return true NEW_LINE } NEW_LINE return false NEW_LINE }",
            ],
            [],
        ],
    ),
]


def test_go_tokenizer_discarding_comments():
    tokenizer_test(TESTS, processor, keep_comments=False)


def test_go_tokenizer_keep_comments():
    tokenizer_test(TESTS_KEEP_COMMENTS, processor, keep_comments=True)


def test_extract_go_functions():
    for input_file, expected_funcs in TEST_FUNC_EXTRACTION:
        actual_funcs_sa, actual_funcs_cl = processor.extract_functions(
            processor.tokenize_code(input_file)
        )
        print(actual_funcs_sa, actual_funcs_cl)
        expected_sa, expected_cl = expected_funcs
        compare_funcs(actual_funcs_sa, expected_sa)
        compare_funcs(actual_funcs_cl, expected_cl)
