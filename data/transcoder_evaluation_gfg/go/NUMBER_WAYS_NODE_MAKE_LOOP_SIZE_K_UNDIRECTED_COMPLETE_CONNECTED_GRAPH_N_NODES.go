package main

import (
		"fmt"
	"math"
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
	var p int = 1
	if k%2 != 0 {
		p = -1
	}
	return int((math.Pow(float64(n-1), float64(k)) + float64(p*(n-1))) / float64(n))
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{27, 70, 77, 83, 16, 90, 39, 48, 56, 10}
		param1    []int = []int{59, 87, 40, 26, 2, 66, 72, 26, 77, 47}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
