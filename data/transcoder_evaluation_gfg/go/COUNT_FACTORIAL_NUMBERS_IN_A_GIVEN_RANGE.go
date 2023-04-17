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


func f_gold(low int, high int) int {
	var (
		fact int = 1
		x    int = 1
	)
	for fact < low {
		fact = fact * x
		x++
	}
	var res int = 0
	for fact <= high {
		res++
		fact = fact * x
		x++
	}
	return res
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{57, 57, 31, 62, 49, 82, 31, 5, 76, 55}
		param1    []int = []int{79, 21, 37, 87, 98, 76, 45, 52, 43, 6}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
