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


func f_gold(num int, divisor int) int {
	for num >= divisor {
		num -= divisor
	}
	return num
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{70, 77, 77, 88, 96, 6, 79, 44, 26, 82}
		param1    []int = []int{13, 3, 73, 54, 39, 10, 95, 32, 86, 91}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
