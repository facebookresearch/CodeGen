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
		prevPrev int = 1
		prev     int = 2
		curr     int = 3
	)
	for n > 0 {
		prevPrev = prev
		prev = curr
		curr = prevPrev + prev
		n = n - (curr - prev - 1)
	}
	n = n + (curr - prev - 1)
	return prev + n
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{76, 91, 62, 65, 83, 57, 76, 6, 2, 86}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
