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


func f_gold(a int, b int, k int) int {
	var (
		p     int = int(math.Pow(float64(a), float64(b)))
		count int = 0
	)
	for p > 0 && count < k {
		var rem int = p % 10
		count++
		if count == k {
			return rem
		}
		p = p / 10
	}
	return 0
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{11, 41, 5, 1, 24, 5, 66, 7, 77, 60}
		param1    []int = []int{2, 3, 4, 2, 1, 2, 5, 10, 30, 50}
		param2    []int = []int{1, 0, 3, 4, 5, 3, 8, 3, 10, 1}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i]) == f_gold(param0[i], param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
