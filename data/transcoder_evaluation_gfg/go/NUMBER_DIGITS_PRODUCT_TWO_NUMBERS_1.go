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


func f_gold(a int, b int) int {
	if a == 0 || b == 0 {
		return 1
	}
	return int(math.Floor(math.Log10(float64(math.Abs(float64(a))))+math.Log10(float64(math.Abs(float64(b))))) + 1)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{97, 52, 95, 35, 40, 18, 92, 73, 10, 82}
		param1    []int = []int{91, 49, 34, 40, 85, 97, 15, 98, 62, 22}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
