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


func f_gold(a float64, b float64) bool {
	if a == 0 || b == 0 {
		return false
	}
	var result float64 = a * b
	if a == result/b {
		return false
	} else {
		return true
	}
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{37, 10000000000, 10000000000, 0x3B9AC9FF, 39, 92, 14, 19, 14, 88}
		param1    []int = []int{80, -10000000000, 10000000000, 0x3B9AC9FF, 36, 56, 21, 38, 82, 41}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(float64(param0[i]), float64(param1[i])) == f_gold(float64(param0[i]), float64(param1[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
