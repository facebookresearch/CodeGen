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
	var n int = int(len(str))
	return n * (n + 1) / 2
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("gZFGZsHCimLf"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("505357"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("011011101"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("ovfwP Osauz"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("92132238746026"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("01100"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("RaOWYQRfiWKSyC"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("861330202"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("001100010"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("uvpKlGUBLOMba"))
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
