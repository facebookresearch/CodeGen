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
	if x == 0 || x == 1 {
		return x
	}
	var i int = 1
	var result int = 1
	for result <= x {
		i++
		result = i * i
	}
	return i - 1
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{89, 11, 14, 92, 76, 63, 51, 16, 83, 66}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
