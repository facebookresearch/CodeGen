package main

import (
		"fmt"
	"math"
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


func f_gold(x int, y int) int {
	x = x % 10
	if y != 0 {
		y = y%4 + 4
	}
	return (int(math.Pow(float64(x), float64(y)))) % 10
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{37, 70, 26, 9, 82, 95, 43, 7, 19, 49}
		param1    []int = []int{17, 52, 23, 96, 71, 36, 40, 27, 56, 28}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
