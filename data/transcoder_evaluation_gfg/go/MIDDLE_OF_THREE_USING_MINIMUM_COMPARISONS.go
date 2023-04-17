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
	if a < b && b < c || c < b && b < a {
		return b
	} else if b < a && a < c || c < a && a < b {
		return a
	} else {
		return c
	}
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{56, 56, 36, 71, 3, 84, 30, 82, 90, 38}
		param1    []int = []int{5, 60, 56, 54, 70, 57, 80, 54, 70, 4}
		param2    []int = []int{82, 17, 51, 6, 81, 47, 85, 32, 55, 5}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i]) == f_gold(param0[i], param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
