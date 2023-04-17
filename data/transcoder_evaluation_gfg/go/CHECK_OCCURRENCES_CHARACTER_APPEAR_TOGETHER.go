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


func f_gold(s []byte, c int8) bool {
	var (
		oneSeen bool = false
		i       int  = 0
		n       int  = int(len(s))
	)
	for i < n {
		if s[i] == byte(c) {
			if oneSeen {
				return false
			}
			for i < n && s[i] == byte(c) {
				i++
			}
			oneSeen = true
		} else {
			i++
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
			copy(t[:], ([]byte)("gILrzLimS"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("307471222"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("110"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("GcAB"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("113"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("011110010"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("wcwob"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("74571582216153"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("100000011"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("ryPErkzY"))
			return t
		}()}
		param1 []byte = []byte{byte('m'), byte('2'), byte('0'), byte('v'), byte('3'), byte('0'), byte('w'), byte('1'), byte('0'), byte('q')}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i][:], int8(param1[i])) == f_gold(param0[i][:], int8(param1[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
