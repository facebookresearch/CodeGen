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


func f_gold(a int, b int, d int) int {
	var temp int = a
	a = min(a, b)
	b = max(temp, b)
	if d >= b {
		return (d + b - 1) / b
	}
	if d == 0 {
		return 0
	}
	if d == a {
		return 1
	}
	return 2
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{35, 85, 22, 8, 12, 58, 65, 10, 23, 5}
		param1    []int = []int{8, 55, 23, 43, 64, 25, 4, 95, 13, 50}
		param2    []int = []int{77, 33, 64, 29, 11, 26, 28, 55, 54, 71}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i]) == f_gold(param0[i], param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
