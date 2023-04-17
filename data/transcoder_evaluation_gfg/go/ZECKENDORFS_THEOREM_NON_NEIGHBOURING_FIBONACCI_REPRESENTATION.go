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
	if n == 0 || n == 1 {
		return n
	}
	var f1 int = 0
	var f2 int = 1
	var f3 int = 1
	for f3 <= n {
		f1 = f2
		f2 = f3
		f3 = f1 + f2
	}
	return f2
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{54, 71, 64, 71, 96, 43, 70, 94, 95, 69}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
