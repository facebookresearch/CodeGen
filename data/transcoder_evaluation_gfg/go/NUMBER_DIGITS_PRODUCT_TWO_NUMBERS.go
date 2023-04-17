package main

import (
	"math"
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


func f_gold(a int, b int) int {
	var (
		count int = 0
		p     int = int(math.Abs(float64(a * b)))
	)
	if p == 0 {
		return 1
	}
	for p > 0 {
		count++
		p = p / 10
	}
	return count
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{86, 81, 48, 64, 56, 5, 25, 94, 5, 46}
		param1    []int = []int{39, 87, 84, 80, 20, 70, 13, 83, 55, 46}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
