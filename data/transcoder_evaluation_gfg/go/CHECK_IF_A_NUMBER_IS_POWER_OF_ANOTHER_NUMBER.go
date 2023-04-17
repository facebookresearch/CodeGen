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


func f_gold(x int, y int) bool {
	if x == 1 {
		return y == 1
	}
	var pow int = 1
	for pow < y {
		pow *= x
	}
	return pow == y
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{57, 3, 10, 10, 6, 2, 1, 20, 96, 25}
		param1    []int = []int{1, 9, 101, 10000, 0xB640, 2048, 40, 79, 98, 5}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
