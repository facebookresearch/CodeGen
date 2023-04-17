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
		i int = 0
		j int = int(len(str) - 1)
	)
	for i < j {
		if str[i] != str[j] {
			return false
		}
		i++
		j--
	}
	return true
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("ab"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("303"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("11110000"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("aba"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("404"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("10101"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("abab"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("6366"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("001"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)(""))
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
