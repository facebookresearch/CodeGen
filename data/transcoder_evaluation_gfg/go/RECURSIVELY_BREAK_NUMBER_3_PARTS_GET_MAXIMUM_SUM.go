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
	if n == 0 || n == 1 {
		return n
	}
	return max(f_gold(n/2)+f_gold(n/3)+f_gold(n/4), n)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{39, 79, 7, 76, 48, 18, 58, 17, 36, 5}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
