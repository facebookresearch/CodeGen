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


func f_gold(m int, n int) int {
	var path int = 1
	for i := int(n); i < (m + n - 1); i++ {
		path *= i
		path /= i - n + 1
	}
	return path
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{10, 52, 5, 84, 27, 77, 52, 3, 5, 14}
		param1    []int = []int{3, 8, 23, 56, 30, 90, 50, 25, 75, 18}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
