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


func f_gold(x1 int, y1 int, x2 int, y2 int, r1 int, r2 int) int {
	var (
		distSq   int = (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)
		radSumSq int = (r1 + r2) * (r1 + r2)
	)
	if distSq == radSumSq {
		return 1
	} else if distSq > radSumSq {
		return -1
	} else {
		return 0
	}
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{11, 87, 51, 89, 64, 57, 65, 32, 73, 3}
		param1    []int = []int{36, 1, 1, 67, 10, 86, 90, 23, 61, 99}
		param2    []int = []int{62, 62, 47, 9, 79, 99, 42, 28, 63, 6}
		param3    []int = []int{64, 64, 90, 52, 45, 43, 82, 26, 77, 19}
		param4    []int = []int{50, 54, 14, 94, 67, 83, 77, 60, 92, 21}
		param5    []int = []int{4, 41, 71, 21, 78, 63, 32, 45, 76, 28}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i], param3[i], param4[i], param5[i]) == f_gold(param0[i], param1[i], param2[i], param3[i], param4[i], param5[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
