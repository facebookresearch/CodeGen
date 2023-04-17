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


func f_gold(N int) int {
	if N == 1 {
		return 4
	}
	var countB int = 1
	var countS int = 1
	var prev_countB int
	var prev_countS int
	for i := int(2); i <= N; i++ {
		prev_countB = countB
		prev_countS = countS
		countS = prev_countB + prev_countS
		countB = prev_countS
	}
	var result int = countS + countB
	return result * result
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{17, 66, 53, 97, 34, 54, 9, 99, 59, 87}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
