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
	var sum int = 0
	for n > 0 {
		sum += n % 10
		n /= 10
	}
	if sum == 1 {
		return 10
	}
	return sum
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{2, 39, 31, 45, 35, 94, 67, 50, 4, 63}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
