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


func f_gold(x int) int {
	var (
		i    int = 1
		fact int = 1
	)
	for i = 1; i < x; i++ {
		fact = fact * i
		if fact%x == 0 {
			break
		}
	}
	return i
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{67, 47, 57, 89, 67, 40, 16, 83, 93, 43}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
