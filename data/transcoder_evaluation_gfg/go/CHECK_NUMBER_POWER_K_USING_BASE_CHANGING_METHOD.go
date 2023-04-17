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


func f_gold(n uint, k uint) bool {
	var oneSeen bool = false
	for n > 0 {
		var digit int = int(n % k)
		if digit > 1 {
			return false
		}
		if digit == 1 {
			if oneSeen {
				return false
			}
			oneSeen = true
		}
		n /= k
	}
	return true
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{64, 16, 27, 81, 1, 69, 8, 31, 43, 54}
		param1    []int = []int{4, 2, 3, 72, 9, 17, 20, 79, 81, 89}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(uint(param0[i]), uint(param1[i])) == f_gold(uint(param0[i]), uint(param1[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
