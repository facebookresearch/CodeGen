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


func f_gold(n uint, d uint) uint {
	return n & (d - 1)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{54, 39, 35, 9, 62, 16, 93, 32, 39, 63}
		param1    []int = []int{59, 84, 81, 60, 68, 16, 96, 38, 62, 16}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(uint(param0[i]), uint(param1[i])) == f_gold(uint(param0[i]), uint(param1[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
