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


func f_gold(low int, high int) int {
	var (
		f1     int = 0
		f2     int = 1
		f3     int = 1
		result int = 0
	)
	for f1 <= high {
		if f1 >= low {
			result++
		}
		f1 = f2
		f2 = f3
		f3 = f1 + f2
	}
	return result
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{76, 96, 19, 36, 60, 20, 76, 63, 2, 41}
		param1    []int = []int{43, 52, 79, 2, 11, 15, 4, 93, 25, 39}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
