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


func f_gold(a int, b int, c int, d int) bool {
	var sum int = a*a + b*b + c*c
	if d*d == sum {
		return true
	} else {
		return false
	}
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{1, 3, 0, -1, 82, 14, 6, 13, 96, 70}
		param1    []int = []int{2, 2, 0, -1, 79, 57, 96, 7, 65, 33}
		param2    []int = []int{2, 5, 0, -1, 6, 35, 45, 3, 72, 6}
		param3    []int = []int{3, 38, 0, 1, 59, 29, 75, 63, 93, 2}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i], param3[i]) == f_gold(param0[i], param1[i], param2[i], param3[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
