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


func f_gold(limit int) int {
	if limit < 2 {
		return 0
	}
	var ef1 float64 = 0
	var ef2 float64 = 2
	var sum float64 = ef1 + ef2
	for ef2 <= float64(limit) {
		var ef3 float64 = ef2*4 + ef1
		if ef3 > float64(limit) {
			break
		}
		ef1 = ef2
		ef2 = ef3
		sum += ef2
	}
	return int(sum)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{67, 89, 12, 94, 96, 25, 49, 8, 33, 59}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
