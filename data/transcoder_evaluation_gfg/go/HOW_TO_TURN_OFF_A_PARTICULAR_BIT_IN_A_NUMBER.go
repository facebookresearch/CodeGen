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


func f_gold(n int, k int) int {
	if k <= 0 {
		return n
	}
	return n & ^(1 << (k - 1))
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{49, 59, 76, 27, 61, 67, 63, 85, 90, 24}
		param1    []int = []int{15, 69, 20, 76, 60, 27, 71, 25, 64, 55}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
