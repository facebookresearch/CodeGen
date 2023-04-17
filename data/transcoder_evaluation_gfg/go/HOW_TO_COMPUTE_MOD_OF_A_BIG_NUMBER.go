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


func f_gold(num []byte, a int) int {
	var res int = 0
	for i := int(0); i < int(len(num)); i++ {
		res = (res*10 + int(num[i]) - int('0')) % a
	}
	return res
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("RElCP"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("0139035510"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("00011110"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("TwanZWwLNXhFN"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("6247009752778"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("0100001011011"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("NCh"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("00714746542"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("101000100"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("MSTkXmlbPkV"))
			return t
		}()}
		param1 []int = []int{13, 44, 86, 66, 55, 33, 75, 54, 93, 78}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i][:], param1[i]) == f_gold(param0[i][:], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
