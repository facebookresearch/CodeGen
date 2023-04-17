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


func f_gold(s []byte, c int8) int {
	var res int = 0
	for i := int(0); i < int(len(s)); i++ {
		if s[i] == byte(c) {
			res++
		}
	}
	return res
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("mhjnKfd"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("716662107"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("01"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("wPHSxIbnHakGRO"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("721106"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("111"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("TIBFU"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("0"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("10"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("lqq"))
			return t
		}()}
		param1 []byte = []byte{byte('l'), byte('6'), byte('1'), byte('n'), byte('8'), byte('0'), byte('Q'), byte('3'), byte('0'), byte('d')}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i][:], int8(param1[i])) == f_gold(param0[i][:], int8(param1[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
