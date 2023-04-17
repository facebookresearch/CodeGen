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


func f_gold(n int) int {
	var res int = 0
	for x := int(0); x*x < n; x++ {
		for y := int(0); x*x+y*y < n; y++ {
			res++
		}
	}
	return res
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{61, 45, 53, 4, 82, 86, 37, 48, 81, 50}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
