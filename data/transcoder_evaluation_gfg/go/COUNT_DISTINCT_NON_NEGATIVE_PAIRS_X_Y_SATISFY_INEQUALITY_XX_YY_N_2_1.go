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
	var (
		x      int = 0
		yCount int
		res    int = 0
	)
	for yCount = 0; yCount*yCount < n; yCount++ {
	}
	for yCount != 0 {
		res += yCount
		x++
		for yCount != 0 && x*x+(yCount-1)*(yCount-1) >= n {
			yCount--
		}
	}
	return res
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{72, 75, 92, 30, 45, 40, 81, 17, 81, 99}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
