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


func f_gold(weight []int, n int, c int) int {
	var (
		res     int = 0
		bin_rem int = c
	)
	for i := int(0); i < n; i++ {
		if weight[i] > bin_rem {
			res++
			bin_rem = c - weight[i]
		} else {
			bin_rem -= weight[i]
		}
	}
	return res
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{6, 12, 14, 16, 19, 24, 29, 31, 33, 34, 41, 43, 47, 53, 53, 59, 64, 70, 70, 71, 72, 73, 74, 80, 81, 89, 90}
		param0_1  []int  = []int{-88, -26, 70, -92, 96, 84, -24, -18, 84, 62, -72, 42, 72, 2, 30, 86}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{51, 7, 6, 24, 19, 83, 9, 36, 40, 93, 24, 48, 63, 69, 53, 54, 42, 45, 90, 14, 29, 6, 7, 37, 53, 18, 87, 38, 59, 1, 68, 44, 47, 35, 87, 91, 60, 90, 52, 8, 80, 41, 3, 96}
		param0_4  []int  = []int{-98, -90, -78, -48, -36, -20, 2, 8, 16, 40, 54, 54, 60, 92}
		param0_5  []int  = []int{1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0}
		param0_6  []int  = []int{8, 14, 16, 35, 40, 45, 54, 57, 58, 59, 87, 88, 93, 95, 97}
		param0_7  []int  = []int{-46, -6, 60, -88, 10, 94, -12, -64, -68, -76, -60, -10, 28, 18, 86, 88, 80, -56, 94, -6, -42, 72, -10, 54, -82, -52, -70, -28, -74, 82, -12, 42, 44, 56, 52, -28, 22, 62, -20}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int   = []int{48, 57, 21, 82, 99}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{21, 11, 27, 26, 11, 32, 11, 19, 26, 4}
		param2    []int  = []int{16, 14, 23, 41, 7, 28, 12, 38, 23, 2}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
