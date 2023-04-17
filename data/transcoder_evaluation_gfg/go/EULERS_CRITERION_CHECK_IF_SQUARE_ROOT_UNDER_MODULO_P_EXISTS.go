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


func f_gold(n int, p int) bool {
	n = n % p
	for x := int(2); x < p; x++ {
		if (x*x)%p == n {
			return true
		}
	}
	return false
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{71, 85, 4, 20, 71, 72, 36, 95, 83, 72}
		param1    []int = []int{78, 75, 35, 99, 29, 88, 54, 52, 33, 13}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
