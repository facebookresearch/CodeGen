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
	n--
	var sum int = 0
	sum += (n * (n + 1)) / 2
	sum += (n * (n + 1) * (n*2 + 1)) / 6
	return sum
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{12, 89, 76, 2, 81, 11, 26, 35, 16, 66}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
