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


func f_gold(n int, p int) int {
	if n >= p {
		return 0
	}
	var result int = 1
	for i := int(1); i <= n; i++ {
		result = (result * i) % p
	}
	return result
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{85, 14, 83, 30, 96, 55, 82, 12, 38, 46}
		param1    []int = []int{18, 13, 21, 35, 51, 58, 71, 74, 3, 73}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
