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


func f_gold(n int, k int) int {
	if n+1 >= k {
		return k - 1
	} else {
		return n*2 + 1 - k
	}
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{90, 86, 92, 72, 25, 11, 94, 91, 66, 34}
		param1    []int = []int{74, 36, 38, 71, 57, 53, 80, 75, 58, 88}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
