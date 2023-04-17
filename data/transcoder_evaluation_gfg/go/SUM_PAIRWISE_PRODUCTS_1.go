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
		multiTerms float64 = float64(n * (n + 1) / 2)
		sum        float64 = multiTerms
	)
	for i := int(2); i <= n; i++ {
		multiTerms = multiTerms - float64(i-1)
		sum = sum + multiTerms*float64(i)
	}
	return sum
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{41, 50, 67, 18, 60, 6, 27, 46, 50, 20}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
