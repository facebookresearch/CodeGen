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


func f_gold(a int, b int, c int) bool {
	if a+b <= c || a+c <= b || b+c <= a {
		return false
	} else {
		return true
	}
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{29, 83, 48, 59, 56, 68, 63, 95, 2, 11}
		param1    []int = []int{19, 34, 14, 12, 39, 85, 36, 34, 90, 16}
		param2    []int = []int{52, 49, 65, 94, 22, 9, 41, 37, 27, 1}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i]) == f_gold(param0[i], param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
