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


func f_gold(n int) int {
	var ans int = 0
	for length := int(1); float64(length) <= math.Sqrt(float64(n)); length++ {
		for height := int(length); height*length <= n; height++ {
			ans++
		}
	}
	return ans
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{34, 49, 41, 17, 67, 38, 59, 64, 61, 58}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
