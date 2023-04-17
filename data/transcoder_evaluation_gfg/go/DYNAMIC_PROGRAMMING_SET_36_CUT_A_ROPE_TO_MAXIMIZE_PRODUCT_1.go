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


func f_gold(n int) int {
	if n == 2 || n == 3 {
		return n - 1
	}
	var res int = 1
	for n > 4 {
		n -= 3
		res *= 3
	}
	return n * res
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{62, 53, 8, 6, 35, 35, 46, 74, 69, 3}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
