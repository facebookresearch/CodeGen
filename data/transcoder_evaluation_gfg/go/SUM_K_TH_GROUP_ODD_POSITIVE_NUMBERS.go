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


func f_gold(k int) int {
	var (
		cur int = (k * (k - 1)) + 1
		sum int = 0
	)
	for func() int {
		p := &k
		x := *p
		*p--
		return x
	}() != 0 {
		sum += cur
		cur += 2
	}
	return sum
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{91, 52, 78, 51, 65, 39, 42, 12, 56, 98}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
