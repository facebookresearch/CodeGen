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
		num       int = n
		dec_value int = 0
		base      int = 1
		temp      int = num
	)
	for temp != 0 {
		var last_digit int = temp % 10
		temp = temp / 10
		dec_value += last_digit * base
		base = base * 2
	}
	return dec_value
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{70, 95, 41, 97, 8, 16, 41, 57, 81, 78}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
