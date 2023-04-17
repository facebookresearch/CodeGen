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
	var (
		ans int = 0
		y   int = N / K
		x   int = N % K
	)
	ans = (K*(K-1)/2)*y + (x*(x+1))/2
	return ans
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{40, 46, 97, 63, 92, 60, 67, 61, 74, 67}
		param1    []int = []int{90, 64, 20, 1, 52, 35, 40, 62, 61, 41}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
