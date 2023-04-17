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


func f_gold(num int, divisor int) int {
	return num - divisor*(num/divisor)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{80, 63, 1, 22, 66, 61, 45, 29, 95, 9}
		param1    []int = []int{54, 21, 56, 39, 7, 67, 63, 44, 65, 68}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
