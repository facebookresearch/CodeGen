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


func f_gold(n int) bool {
	if n == 0 || n == 9 {
		return true
	}
	if n < 9 {
		return false
	}
	return f_gold((n >> 3) - (n & 7))
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{96, 85, 54, 14, 47, 11, 49, 99, 28, 82}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
