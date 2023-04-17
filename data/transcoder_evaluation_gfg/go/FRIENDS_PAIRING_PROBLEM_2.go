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
	var (
		a int = 1
		b int = 2
		c int = 0
	)
	if n <= 2 {
		return n
	}
	for i := int(3); i <= n; i++ {
		c = b + (i-1)*a
		a = b
		b = c
	}
	return c
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{24, 1, 91, 90, 89, 29, 3, 60, 75, 14}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
