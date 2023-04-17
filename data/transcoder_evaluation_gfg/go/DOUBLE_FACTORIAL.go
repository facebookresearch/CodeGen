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


func f_gold(n uint) uint {
	if n == 0 || n == 1 {
		return 1
	}
	return n * f_gold(n-2)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{52, 93, 15, 72, 61, 21, 83, 87, 75, 75}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(uint(param0[i])) == f_gold(uint(param0[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
