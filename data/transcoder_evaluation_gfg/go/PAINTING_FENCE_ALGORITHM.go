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


func f_gold(n int, k int) int {
	var (
		total int = k
		mod   int = 0x3B9ACA07
		same  int = 0
		diff  int = k
	)
	for i := int(2); i <= n; i++ {
		same = diff
		diff = total * (k - 1)
		diff = diff % mod
		total = (same + diff) % mod
	}
	return total
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{6, 23, 89, 63, 23, 44, 81, 43, 9, 41}
		param1    []int = []int{30, 87, 31, 36, 68, 66, 18, 73, 42, 98}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
