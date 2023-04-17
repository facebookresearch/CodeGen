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


func f_gold(x int, y int, z int) int {
	if (y / x) == 0 {
		if (y / z) == 0 {
			return y
		}
		return z
	}
	if (x / z) == 0 {
		return x
	}
	return z
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{48, 11, 50, 21, 94, 22, 3, 67, 59, 50}
		param1    []int = []int{63, 55, 89, 71, 39, 44, 41, 62, 2, 11}
		param2    []int = []int{56, 84, 96, 74, 42, 86, 68, 94, 83, 1}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i]) == f_gold(param0[i], param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
