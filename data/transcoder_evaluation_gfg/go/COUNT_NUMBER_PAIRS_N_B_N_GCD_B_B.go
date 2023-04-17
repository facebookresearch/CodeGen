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
	var (
		k    int = n
		imin int = 1
		ans  int = 0
	)
	for imin <= n {
		var imax int = n / k
		ans += k * (imax - imin + 1)
		imin = imax + 1
		k = n / imin
	}
	return ans
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{17, 72, 43, 55, 62, 22, 17, 68, 20, 29}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
