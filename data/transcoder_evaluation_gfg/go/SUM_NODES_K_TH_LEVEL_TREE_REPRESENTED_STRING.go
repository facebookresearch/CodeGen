package main

import (
		"fmt"
	"os"
	"unsafe"
)

func min(x int, y int) int {
	if x < y {
		return x
	}
	return y
}
func max(x int, y int) int {
	if x > y {
		return x
	}
	return y
}
func cmpfunc(a unsafe.Pointer, b unsafe.Pointer) int {
	return *(*int)(a) - *(*int)(b)
}


func f_gold(tree []byte, k int) int {
	var (
		level int = -1
		sum   int = 0
		n     int = int(len(tree))
	)
	for i := int(0); i < n; i++ {
		if tree[i] == byte('(') {
			level++
		} else if tree[i] == byte(')') {
			level--
		} else {
			if level == k {
				sum += int(tree[i] - byte('0'))
			}
		}
	}
	return sum
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("(0(5(6()())(4()(9()())))(7(1()())(3()())))"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("(8(3(2()())(6(5()())()))(5(10()())(7(13()())())))"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("(0(5(6()())(4()(9()())))(7(1()())(3()())))"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("(8(3(2()())(6(5()())()))(5(10()())(7(13()())())))"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("(8(3(2()())(6(5()())()))(5(10()())(7(13()())())))"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("(8(3(2()())(6(5()())()))(5(10()())(7(13()())())))"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("(0(5(6()())(4()(9()())))(7(1()())(3()())))"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("(0(5(6()())(4()(9()())))(7(1()())(3()())))"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("0010"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("kjtdgmy"))
			return t
		}()}
		param1 []int = []int{2, 3, 1, 2, 4, 100, 3, 0, 12, 97}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i][:], param1[i]) == f_gold(param0[i][:], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
