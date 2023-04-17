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


func f_gold(x int, y int) bool {
	return (x ^ y) < 0
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{59, -20, -100, 54, -16, -23, 93, 24, -8, 29}
		param1    []int = []int{-99, -21, 100, -49, 16, -68, 37, -61, 69, 10}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
