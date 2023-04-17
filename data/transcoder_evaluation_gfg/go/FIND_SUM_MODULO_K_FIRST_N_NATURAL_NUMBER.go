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


func f_gold(N int, K int) int {
	var ans int = 0
	for i := int(1); i <= N; i++ {
		ans += i % K
	}
	return ans
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{11, 36, 71, 74, 66, 38, 2, 73, 79, 30}
		param1    []int = []int{5, 69, 28, 1, 84, 14, 11, 87, 11, 55}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
