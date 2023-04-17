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


func f_gold(x1 int, y1 int, x2 int, y2 int) bool {
	return x1*(y2-y1) == y1*(x2-x1)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{1, 10, 0, 1, 82, 78, 13, 18, 42, 29}
		param1    []int = []int{28, 0, 1, 1, 86, 86, 46, 29, 35, 17}
		param2    []int = []int{2, 20, 0, 10, 19, 11, 33, 95, 25, 45}
		param3    []int = []int{56, 0, 17, 10, 4, 6, 33, 12, 36, 35}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i], param3[i]) == f_gold(param0[i], param1[i], param2[i], param3[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
