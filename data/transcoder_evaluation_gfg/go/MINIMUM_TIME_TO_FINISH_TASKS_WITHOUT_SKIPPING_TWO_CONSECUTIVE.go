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


func f_gold(arr []int, n int) int {
	if n <= 0 {
		return 0
	}
	var incl int = arr[0]
	var excl int = 0
	for i := int(1); i < n; i++ {
		var (
			incl_new int = arr[i] + min(excl, incl)
			excl_new int = incl
		)
		incl = incl_new
		excl = excl_new
	}
	return min(incl, excl)
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{5, 17, 25, 27, 29, 30, 34, 49, 72, 75, 90, 93, 93, 94}
		param0_1  []int  = []int{-70, -32, 62, 0, -10, 92, -94, -86, 52, 6, -26, -92, -10, 70, -82, 28, 86, 58, 86, -58, 84, -80, -18, -92, -34, 6, 34, 36, 70, -50, -6, -54, 84, 22, 30, -96, -84, 72, 2, 26, -20, 4, 48, -98, 62, -28, -68}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{34, 40, 92, 35, 29, 26, 12, 66, 7, 28, 86, 4, 35, 79, 1, 48, 41, 47, 15, 75, 45, 6, 3, 94, 39, 50, 20, 8, 58, 51, 83, 44, 53, 76, 19, 84, 68, 54, 36, 53}
		param0_4  []int  = []int{-98, -98, -92, -92, -88, -82, -74, -70, -68, -68, -64, -60, -52, -52, -42, -42, -38, -36, -36, -34, -26, -24, -22, -12, -2, -2, 4, 6, 44, 44, 48, 54, 62, 62, 64, 74, 78, 82, 86, 86, 90, 90, 94}
		param0_5  []int  = []int{1, 1, 0, 0, 1, 0, 0, 1, 1, 1}
		param0_6  []int   = []int{9, 15, 19, 29, 30, 39, 40, 61}
		param0_7  []int  = []int{92, 0, 46, 70, -60, -50, 58, -56, 8, -90, 84, 16, 40, -62, 50, 78, 26, -42, -40, 98, -52, 62, 16, -62, -76, -70, -60, 32, 4, -68, 52, -64, 70, 12, -10}
		param0_8  []int   = []int{0, 0, 0, 1, 1, 1, 1}
		param0_9  []int  = []int{32, 96, 63, 93, 53, 1, 22, 19, 50, 74, 6, 94, 81, 85, 4, 86, 88, 75, 94}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{8, 36, 21, 29, 36, 5, 4, 21, 5, 18}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
