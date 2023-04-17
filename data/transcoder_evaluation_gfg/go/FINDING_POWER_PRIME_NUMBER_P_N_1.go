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


func f_gold(n int, p int) int {
	var (
		ans  int = 0
		temp int = p
	)
	for temp <= n {
		ans += n / temp
		temp = temp * p
	}
	return ans
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{76, 77, 9, 59, 8, 97, 78, 41, 72, 71}
		param1    []int = []int{43, 91, 42, 67, 52, 8, 24, 88, 61, 28}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
