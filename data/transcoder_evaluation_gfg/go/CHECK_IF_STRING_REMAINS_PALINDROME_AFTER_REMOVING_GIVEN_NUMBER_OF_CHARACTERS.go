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


func f_gold(str []byte, n int) bool {
	var len_ int = int(len(str))
	if len_ >= n {
		return true
	}
	return false
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("ZCoQhuM"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("7437725"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("11"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("buGlvR"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("9"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("101101010110"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("YguiM"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("8198"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("11101"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("hUInqJXNdbfP"))
			return t
		}()}
		param1 []int = []int{2, 53, 30, 1, 92, 3, 18, 90, 71, 4}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i][:], param1[i]) == f_gold(param0[i][:], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
