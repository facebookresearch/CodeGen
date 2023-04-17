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
		n int = int(len(str))
		i int
	)
	for i = 0; i < n; i++ {
		if str[i] != byte('a') {
			break
		}
	}
	if i*2 != n {
		return false
	}
	var j int
	for j = i; j < n; j++ {
		if str[j] != byte('b') {
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
			copy(t[:], ([]byte)("ba"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("aabb"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("abab"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("aaabb"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("aabbb"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("abaabbaa"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("abaababb"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("bbaa"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("11001000"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("ZWXv te"))
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
