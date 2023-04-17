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


func f_gold(a int, b int) int {
	var cnt int = 0
	for i := int(a); i <= b; i++ {
		for j := int(1); j*j <= i; j++ {
			if j*j == i {
				cnt++
			}
		}
	}
	return cnt
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{48, 3, 20, 98, 96, 40, 9, 57, 28, 98}
		param1    []int = []int{42, 82, 72, 98, 90, 82, 15, 77, 80, 75}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
