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


func f_gold(l int, w int) int {
	return (l + w) * 2
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{58, 37, 56, 22, 77, 34, 74, 37, 21, 75}
		param1    []int = []int{39, 49, 52, 43, 12, 31, 54, 52, 37, 30}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
