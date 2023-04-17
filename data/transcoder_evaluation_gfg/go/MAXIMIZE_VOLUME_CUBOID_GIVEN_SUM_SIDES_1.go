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


func f_gold(s int) int {
	var length int = s / 3
	s -= length
	var breadth int = s / 2
	var height int = s - breadth
	return length * breadth * height
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{8, 96, 96, 96, 12, 95, 72, 81, 42, 13}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
