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


func f_gold(strA []byte, strB []byte) int8 {
	var (
		res int = 0
		i   int
	)
	for i = 0; i < int(len(strA)); i++ {
		res ^= int(strA[i])
	}
	for i = 0; i < int(len(strB)); i++ {
		res ^= int(strB[i])
	}
	return int8(res)
}
//TOFILL
func main() {
	var (
		n_success int           = 0
		param0    [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("obfLA mmMYvghH"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("2941"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("0111111"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("oWvbFstI"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("4937516500"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("101110100"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("hYZscJQFBE"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("58443"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("1100"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("ZUdYuIBVNaeeb"))
			return t
		}()}
		param1 [10][]byte = [10][]byte{func() []byte {
			var t []byte
			copy(t[:], ([]byte)("obfLA  mmMYvghH"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("23941"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("01011111"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("oWvsbFstI"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("49376516500"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("1011210100"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("hYZscJQQFBE"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("584443"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("11000"))
			return t
		}(), func() []byte {
			var t []byte
			copy(t[:], ([]byte)("ZUdYVuIBVNaeeb"))
			return t
		}()}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if int(f_filled(param0[i][:], param1[i][:])) == int(f_gold(param0[i][:], param1[i][:])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
