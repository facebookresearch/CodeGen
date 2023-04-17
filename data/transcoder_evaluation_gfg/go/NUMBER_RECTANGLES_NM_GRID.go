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


func f_gold(n int, m int) int {
	return (m * n * (n + 1) * (m + 1)) / 4
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{86, 33, 3, 91, 33, 13, 75, 58, 50, 4}
		param1    []int = []int{70, 65, 5, 12, 27, 75, 36, 64, 51, 44}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
