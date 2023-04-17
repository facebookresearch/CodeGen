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


func f_gold(str []byte) int {
	var checker int = 0
	for i := int(0); i < int(len(str)); i++ {
		var val int = int(str[i] - byte('a'))
		if (checker & (1 << val)) > 0 {
			return i
		}
		checker |= 1 << val
	}
	return -1
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("XFGfXTDgpIuerN"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("5621946166"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("11010110"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("xL"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("2575"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("0100010"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("SZmmQ"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("9735892999350"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("1001101101101"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("oEXDbOU"))
			return t
		}()}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i][:]) == f_gold(param0[i][:]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
