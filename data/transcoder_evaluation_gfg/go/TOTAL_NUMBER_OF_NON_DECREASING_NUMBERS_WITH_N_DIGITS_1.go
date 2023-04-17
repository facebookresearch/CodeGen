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


func f_gold(n int) float64 {
	var (
		N     int   = 10
		count float64 = 1
	)
	for i := int(1); i <= n; i++ {
		count *= float64(N + i - 1)
		count /= float64(i)
	}
	return count
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{40, 11, 94, 73, 6, 73, 58, 40, 64, 66}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
