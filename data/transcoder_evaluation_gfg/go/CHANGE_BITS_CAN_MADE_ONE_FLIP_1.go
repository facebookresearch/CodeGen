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
		sum int = 0
		n   int = int(len(str))
	)
	for i := int(0); i < n; i++ {
		sum += int(str[i] - byte('0'))
	}
	return sum == n-1 || sum == 1
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("00001"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("0000"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("11"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("111110"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("1"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("111010111010"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("hUInqJXNdbfP"))
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
			copy(t[:], ([]byte)("NupSrU xz"))
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
