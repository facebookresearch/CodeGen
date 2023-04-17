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


func f_gold(x int, y int, z int) int {
	var c int = 0
	for x != 0 && y != 0 && z != 0 {
		x--
		y--
		z--
		c++
	}
	return c
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{23, 87, 35, 25, 93, 52, 95, 91, 75, 96}
		param1    []int = []int{98, 55, 90, 9, 22, 42, 88, 64, 1, 44}
		param2    []int = []int{25, 94, 29, 41, 39, 96, 26, 51, 6, 76}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i]) == f_gold(param0[i], param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
