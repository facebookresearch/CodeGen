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


func f_gold(a int, b int) int {
	if a == 0 {
		return b
	}
	return f_gold(b%a, a)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{46, 26, 40, 58, 25, 2, 8, 21, 82, 17}
		param1    []int = []int{89, 82, 12, 4, 44, 87, 65, 87, 10, 61}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
