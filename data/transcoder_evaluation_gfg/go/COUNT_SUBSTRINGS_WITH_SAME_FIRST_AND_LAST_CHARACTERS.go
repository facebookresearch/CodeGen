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


func f_gold(s []byte) int {
	var (
		result int = 0
		n      int = int(len(s))
	)
	for i := int(0); i < n; i++ {
		for j := int(i); j < n; j++ {
			if s[i] == s[j] {
				result++
			}
		}
	}
	return result
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("LZIKA"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("0556979952"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("110010"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("kGaYfd"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("413567670657"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("01001"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("EQPuFa"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("48848378"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("110"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("PLehNeP"))
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
