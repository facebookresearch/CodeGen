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
	for n%2 == 0 {
		k--
		n = n / 2
		if k == 0 {
			return 2
		}
	}
	for i := int(3); float64(i) <= math.Sqrt(float64(n)); i = i + 2 {
		for n%i == 0 {
			if k == 1 {
				return i
			}
			k--
			n = n / i
		}
	}
	if n > 2 && k == 1 {
		return n
	}
	return -1
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{94, 99, 64, 27, 24, 84, 69, 69, 22, 39}
		param1    []int = []int{0, 1, 3, 3, 4, 6, 98, 39, 60, 57}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
