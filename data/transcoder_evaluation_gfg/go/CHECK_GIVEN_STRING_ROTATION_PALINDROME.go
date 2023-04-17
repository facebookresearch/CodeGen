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
	var (
		l int = 0
		h int = int(len(str) - 1)
	)
	for h > l {
		if str[func() int {
			p := &l
			x := *p
			*p++
			return x
		}()] != str[func() int {
			p := &h
			x := *p
			*p--
			return x
		}()] {
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
			copy(t[:], ([]byte)("aadaa"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("2674377254"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("11"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("0011000"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("26382426486138"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("111010111010"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("abccba"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("5191"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("1110101101"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("abcdecbe"))
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
