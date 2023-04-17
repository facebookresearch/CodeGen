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


func f_gold(a uint, b uint) uint {
	var res int = 0
	for b > 0 {
		if b&1 != 0 {
			res = res + int(a)
		}
		a = a << 1
		b = b >> 1
	}
	return uint(res)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{4, 36, 65, 55, 35, 69, 84, 5, 15, 67}
		param1    []int = []int{33, 67, 52, 37, 76, 98, 62, 80, 36, 84}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(uint(param0[i]), uint(param1[i])) == f_gold(uint(param0[i]), uint(param1[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
