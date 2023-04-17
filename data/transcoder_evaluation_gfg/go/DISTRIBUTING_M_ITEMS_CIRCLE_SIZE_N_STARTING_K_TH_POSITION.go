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


func f_gold(n int, m int, k int) int {
	if m <= n-k+1 {
		return m + k - 1
	}
	m = m - (n - k + 1)
	if m%n == 0 {
		return n
	}
	return m % n
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{19, 23, 92, 9, 20, 68, 66, 77, 90, 26}
		param1    []int = []int{14, 51, 10, 50, 67, 25, 30, 22, 1, 34}
		param2    []int = []int{34, 5, 24, 34, 20, 40, 24, 32, 71, 54}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i]) == f_gold(param0[i], param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
