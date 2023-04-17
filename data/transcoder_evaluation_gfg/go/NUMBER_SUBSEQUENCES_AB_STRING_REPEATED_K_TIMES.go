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


func f_gold(s []byte, K int) int {
	var (
		n  int = int(len(s))
		C  int
		c1 int = 0
		c2 int = 0
	)
	for i := int(0); i < n; i++ {
		if s[i] == byte('a') {
			c1++
		}
		if s[i] == byte('b') {
			c2++
			C += c1
		}
	}
	return C*K + (K*(K-1)/2)*c1*c2
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("KdJ"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("031"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("11000"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("zPbB"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("9"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("1010"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("c"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("06064629743411"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("1111"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("PFXAhru"))
			return t
		}()}
		param1 []int = []int{96, 70, 59, 60, 80, 41, 87, 4, 18, 83}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i][:], param1[i]) == f_gold(param0[i][:], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
