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


func f_gold(n uint) uint {
	var (
		res int = 1
		i   int
	)
	for i = 2; i <= int(n); i++ {
		res *= i
	}
	return uint(res)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{15, 7, 16, 67, 71, 16, 77, 27, 37, 73}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(uint(param0[i])) == f_gold(uint(param0[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
