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
	var (
		nthElement    int = (n-1)*9 + 19
		outliersCount int = int(math.Log10(float64(nthElement))) - 1
	)
	nthElement += outliersCount * 9
	return nthElement
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{68, 70, 69, 93, 99, 44, 91, 8, 83, 51}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
