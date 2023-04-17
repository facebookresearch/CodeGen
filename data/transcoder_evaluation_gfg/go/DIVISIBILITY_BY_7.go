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


func f_gold(num int) int {
	if num < 0 {
		return f_gold(-num)
	}
	if num == 0 || num == 7 {
		return 1
	}
	if num < 10 {
		return 0
	}
	return f_gold(num/10 - (num-num/10*10)*2)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{0, -21, 7, 63, 84, 73, 81, -10, 47, 23}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
