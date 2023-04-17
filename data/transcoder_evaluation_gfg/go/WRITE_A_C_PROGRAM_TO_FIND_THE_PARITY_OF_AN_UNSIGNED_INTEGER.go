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


func f_gold(n uint) bool {
	var parity bool = false
	for n != 0 {
		parity = !parity
		n = n & (n - 1)
	}
	return parity
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{63, 64, 85, 36, 20, 63, 42, 19, 62, 97}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(uint(param0[i])) == f_gold(uint(param0[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
