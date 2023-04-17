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
	var count int = 0
	for curr := int(1); ; curr++ {
		var sum int = 0
		for x := int(curr); x > 0; x = x / 10 {
			sum = sum + x%10
		}
		if sum == 10 {
			count++
		}
		if count == n {
			return curr
		}
	}
	return -1
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{37, 13, 51, 69, 76, 10, 97, 40, 69, 4}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
