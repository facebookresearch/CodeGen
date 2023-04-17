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


func f_gold(process int, need int) int {
	var minResources int = 0
	minResources = process*(need-1) + 1
	return minResources
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{38, 82, 2, 38, 31, 80, 11, 2, 26, 37}
		param1    []int = []int{37, 3, 26, 72, 85, 73, 9, 31, 59, 67}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
