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


func f_gold(a int, b int, k int) int {
	var (
		c1 int = (b - a) - 1
		c2 int = (k - b) + (a - 1)
	)
	if c1 == c2 {
		return 0
	}
	return min(c1, c2)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{83, 3, 11, 50, 40, 62, 40, 66, 6, 25}
		param1    []int = []int{98, 39, 96, 67, 16, 86, 78, 11, 9, 5}
		param2    []int = []int{86, 87, 30, 48, 32, 76, 71, 74, 19, 5}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i]) == f_gold(param0[i], param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
