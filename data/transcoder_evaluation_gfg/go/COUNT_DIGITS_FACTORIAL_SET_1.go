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
	if n < 0 {
		return 0
	}
	if n <= 1 {
		return 1
	}
	var digits float64 = 0
	for i := int(2); i <= n; i++ {
		digits += math.Log10(float64(i))
	}
	return int(math.Floor(digits) + 1)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{66, 7, 55, 37, 76, 16, 17, 95, 71, 90}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
