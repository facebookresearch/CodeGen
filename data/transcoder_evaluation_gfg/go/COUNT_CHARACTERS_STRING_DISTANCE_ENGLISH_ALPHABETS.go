package main

import (
	"math"
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
		result int = 0
		n      int = int(len(str))
	)
	for i := int(0); i < n; i++ {
		for j := int(i + 1); j < n; j++ {
			if math.Abs(float64(str[i]-str[j])) == math.Abs(float64(i-j)) {
				result++
			}
		}
	}
	return result
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("smnKL"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("270083"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("0"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("kcZdsz"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("483544224"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("000011"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("WysGCirMwKBzP"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("3366"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("110"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("NlaMkpCjUgg"))
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
