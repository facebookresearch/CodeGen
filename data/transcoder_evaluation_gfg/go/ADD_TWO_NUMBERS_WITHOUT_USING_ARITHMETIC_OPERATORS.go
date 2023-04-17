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


func f_gold(x int, y int) int {
	for y != 0 {
		var carry int = x & y
		x = x ^ y
		y = carry << 1
	}
	return x
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{56, 17, 73, 75, 27, 61, 65, 22, 61, 97}
		param1    []int = []int{60, 44, 96, 3, 54, 1, 63, 19, 9, 23}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
