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


func f_gold(s []byte) bool {
	var n int = int(len(s))
	for i := int(1); i < n; i++ {
		if s[i] != s[0] {
			return false
		}
	}
	return true
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)(""))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("ggg"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("11"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("KoYIHns"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("232"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("10111000011101"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("DDDD"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("11"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("11111"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("ewJvixQzu"))
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
