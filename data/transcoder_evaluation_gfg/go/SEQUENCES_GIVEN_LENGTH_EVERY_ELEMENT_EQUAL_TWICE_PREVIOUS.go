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
	if m < n {
		return 0
	}
	if n == 0 {
		return 1
	}
	return f_gold(m-1, n) + f_gold(m/2, n-1)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{38, 39, 24, 90, 44, 49, 58, 97, 99, 19}
		param1    []int = []int{34, 29, 99, 23, 2, 70, 84, 34, 72, 67}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
