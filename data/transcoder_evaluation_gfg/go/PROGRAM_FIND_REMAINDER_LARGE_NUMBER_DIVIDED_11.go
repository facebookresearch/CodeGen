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
		len_ int = int(len(str))
		num  int
		rem  int = 0
	)
	for i := int(0); i < len_; i++ {
		num = rem*10 + int(str[i]-byte('0'))
		rem = num % 11
	}
	return rem
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("DvsNZVNZ"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("1170"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("10"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("evsPwREbSY"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("09219178704"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("1001010"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("SkZbWSajDKmiG"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("0287976763"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("011011000111"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("lUn"))
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
