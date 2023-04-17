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


func f_gold(n int) bool {
	if n <= 1 {
		return false
	}
	if n <= 3 {
		return false
	}
	if n%2 == 0 || n%3 == 0 {
		return true
	}
	for i := int(5); i*i <= n; i = i + 6 {
		if n%i == 0 || n%(i+2) == 0 {
			return true
		}
	}
	return false
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{62, 13, 29, 72, 30, 20, 10, 47, 91, 52}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
