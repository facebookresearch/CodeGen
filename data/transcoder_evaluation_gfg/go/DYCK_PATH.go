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


func f_gold(n uint) int {
	var res int = 1
	for i := int(0); i < int(n); i++ {
		res *= int(n*2 - uint(i))
		res /= i + 1
	}
	return res / int(n+1)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{72, 90, 61, 28, 70, 13, 7, 98, 99, 67}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(uint(param0[i])) == f_gold(uint(param0[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
