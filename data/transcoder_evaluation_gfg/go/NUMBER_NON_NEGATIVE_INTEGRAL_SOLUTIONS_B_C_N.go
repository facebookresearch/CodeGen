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


func f_gold(n int) int {
	var result int = 0
	for i := int(0); i <= n; i++ {
		for j := int(0); j <= n-i; j++ {
			for k := int(0); k <= (n - i - j); k++ {
				if i+j+k == n {
					result++
				}
			}
		}
	}
	return result
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{62, 44, 37, 81, 14, 20, 76, 72, 96, 52}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
