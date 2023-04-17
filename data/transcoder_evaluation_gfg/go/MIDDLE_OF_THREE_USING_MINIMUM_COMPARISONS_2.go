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


func f_gold(a int, b int, c int) int {
	var (
		x int = a - b
		y int = b - c
		z int = a - c
	)
	if x*y > 0 {
		return b
	} else if x*z > 0 {
		return c
	} else {
		return a
	}
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{48, 21, 71, 93, 3, 58, 88, 8, 17, 13}
		param1    []int = []int{46, 7, 4, 34, 61, 78, 41, 84, 66, 3}
		param2    []int = []int{38, 16, 31, 11, 32, 6, 66, 38, 27, 23}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i]) == f_gold(param0[i], param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
