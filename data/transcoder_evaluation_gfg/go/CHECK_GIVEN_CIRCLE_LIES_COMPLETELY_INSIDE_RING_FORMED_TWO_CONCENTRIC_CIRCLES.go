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


func f_gold(r int, R int, r1 int, x1 int, y1 int) bool {
	var dis int = int(math.Sqrt(float64(x1*x1 + y1*y1)))
	return dis-r1 >= R && dis+r1 <= r
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{8, 400, 1, 61, 60, 88, 60, 26, 33, 70}
		param1    []int = []int{4, 1, 400, 40, 49, 10, 79, 88, 65, 57}
		param2    []int = []int{2, 10, 10, 2, 68, 69, 92, 75, 57, 77}
		param3    []int = []int{6, 74, 74, 50, 77, 71, 29, 84, 21, 52}
		param4    []int = []int{0, 38, 38, 0, 71, 26, 38, 10, 61, 87}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i], param2[i], param3[i], param4[i]) == f_gold(param0[i], param1[i], param2[i], param3[i], param4[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
