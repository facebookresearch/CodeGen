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
	return (a / 2) + b/2 + (a%2+b%2)/2
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{9, 68, 51, 31, 14, 73, 51, 75, 98, 83}
		param1    []int = []int{81, 79, 2, 49, 10, 9, 13, 67, 51, 74}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
