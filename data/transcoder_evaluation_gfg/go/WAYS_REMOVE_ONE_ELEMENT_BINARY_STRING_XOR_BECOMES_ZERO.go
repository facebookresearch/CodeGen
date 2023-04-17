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
	var (
		one_count  int = 0
		zero_count int = 0
		n          int = int(len(str))
	)
	for i := int(0); i < n; i++ {
		if str[i] == byte('1') {
			one_count++
		} else {
			zero_count++
		}
	}
	if one_count%2 == 0 {
		return zero_count
	}
	return one_count
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("KfcTJNP"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("05312505872"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("100111"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("tDEEhKxrQ"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("50824233019"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("10001110010"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("T SEZaNm MYQ"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("838415739"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("01110100"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("WYQiAey H"))
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
