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


func f_gold(x int, y int) int {
	var res int = 1
	for i := int(0); i < y; i++ {
		res = (res * x) % 10
	}
	return res
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{33, 95, 21, 3, 40, 64, 17, 58, 44, 27}
		param1    []int = []int{55, 7, 63, 62, 53, 24, 23, 74, 13, 54}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
