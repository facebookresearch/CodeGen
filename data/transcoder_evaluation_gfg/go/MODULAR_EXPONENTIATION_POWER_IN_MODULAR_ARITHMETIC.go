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


func f_gold(x int, y uint, p int) int {
	var res int = 1
	x = x % p
	for y > 0 {
		if y&1 != 0 {
			res = (res * x) % p
		}
		y = y >> 1
		x = (x * x) % p
	}
	return res
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{45, 67, 26, 33, 35, 68, 14, 5, 23, 37}
		param1    []int = []int{5, 25, 91, 61, 8, 41, 76, 89, 42, 63}
		param2    []int = []int{68, 49, 44, 9, 13, 5, 20, 13, 45, 56}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], uint(param1[i]), param2[i]) == f_gold(param0[i], uint(param1[i]), param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
