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


func f_gold(str []byte) bool {
	var n int = int(len(str))
	if n == 0 {
		return false
	}
	if n == 1 {
		return (str[0]-byte('0'))%4 == 0
	}
	var last int = int(str[n-1] - byte('0'))
	var second_last int = int(str[n-2] - byte('0'))
	return (second_last*10+last)%4 == 0
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("PjAFZXQgN"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("12325195609714"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("00101111101"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("xOtbXZiA"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("980"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("000000100"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("zFacc W"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("8"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("110011"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("afiutekeSfYrX"))
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
