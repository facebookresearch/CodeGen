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


func f_gold(s int) int {
	var sum int = 0
	for n := int(1); sum < s; n++ {
		sum += n * n * n
		if sum == s {
			return n
		}
	}
	return -1
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{15, 36, 39, 43, 75, 49, 56, 14, 62, 97}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
