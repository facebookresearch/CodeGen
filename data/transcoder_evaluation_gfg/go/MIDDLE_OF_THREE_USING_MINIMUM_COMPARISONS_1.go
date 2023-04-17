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


func f_gold(a int, b int, c int) int {
	if a > b {
		if b > c {
			return b
		} else if a > c {
			return c
		} else {
			return a
		}
	} else {
		if a > c {
			return a
		} else if b > c {
			return c
		} else {
			return b
		}
	}
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{43, 76, 57, 10, 59, 92, 49, 16, 33, 66}
		param1    []int = []int{24, 54, 5, 13, 47, 14, 62, 95, 41, 63}
		param2    []int = []int{7, 66, 40, 4, 56, 50, 65, 12, 90, 46}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i]) == f_gold(param0[i], param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
