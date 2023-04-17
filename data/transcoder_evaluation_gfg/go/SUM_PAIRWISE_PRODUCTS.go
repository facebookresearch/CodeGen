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
	var sum float64 = 0
	for i := int(1); i <= n; i++ {
		for j := int(i); j <= n; j++ {
			sum = sum + float64(i*j)
		}
	}
	return sum
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{21, 32, 16, 38, 9, 3, 5, 46, 45, 87}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
