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


func f_gold(b int, m int) int {
	return (b/m - 1) * (b / m) / 2
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{40, 38, 47, 52, 21, 50, 8, 56, 93, 21}
		param1    []int = []int{74, 35, 71, 29, 9, 33, 82, 80, 5, 90}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
