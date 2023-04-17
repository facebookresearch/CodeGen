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
	var (
		n          int = int(len(str))
		oddDigSum  int = 0
		evenDigSum int = 0
	)
	for i := int(0); i < n; i++ {
		if i%2 == 0 {
			oddDigSum += int(str[i] - byte('0'))
		} else {
			evenDigSum += int(str[i] - byte('0'))
		}
	}
	return (oddDigSum-evenDigSum)%11
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("r"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("7386620"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("1010"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("rWFOLX VB"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("3845847974820"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("01001"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("yq"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("770356"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("0000110111001"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("tDMrBdHJJITDx"))
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
