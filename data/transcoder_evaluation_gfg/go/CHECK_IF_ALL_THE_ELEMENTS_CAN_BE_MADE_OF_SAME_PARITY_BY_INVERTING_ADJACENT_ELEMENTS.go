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


func f_gold(a []int, n int) bool {
	var (
		count_odd  int = 0
		count_even int = 0
	)
	for i := int(0); i < n; i++ {
		if a[i]&1 != 0 {
			count_odd++
		} else {
			count_even++
		}
	}
	if count_odd%2 != 0 && count_even%2 != 0 {
		return false
	} else {
		return true
	}
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{1, 1, 1, 7, 7, 8, 10, 10, 10, 14, 15, 18, 20, 23, 24, 24, 26, 30, 32, 32, 33, 36, 42, 43, 46, 48, 51, 51, 52, 53, 58, 58, 59, 59, 59, 60, 67, 71, 72, 74, 76, 77, 83, 84, 86, 90, 91}
		param0_1  []int  = []int{-90, -20, -60, -64, -24, 84, -2, -32, 28, -54, 44, -96, 52, 88, 20, -56, -2}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{98, 70, 24, 18, 7, 4, 78, 19, 70, 56, 99, 54, 69, 15, 88, 20, 40, 13, 19, 56, 62}
		param0_4  []int   = []int{-72, -66, -58, -20, 36, 80, 92}
		param0_5  []int   = []int{0, 1}
		param0_6  []int  = []int{6, 13, 14, 16, 21, 26, 26, 28, 29, 35, 38, 42, 47, 47, 62, 67, 77, 81, 81, 83, 84, 88, 90, 96, 97, 98}
		param0_7  []int  = []int{-48, -8, 20, 32, -90, -42, -6, -88, -72, 42, 66, -62, 82, -4, 8, 12, -22, 82, 56, 96, -54, 92, -42, 30, -18, 14, -6, -66, 34, 16, -84, -94, 48, -48, 52, -60, -92, -16}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{45, 86, 53, 80, 27, 45, 1, 85, 91, 93, 92, 43, 75, 86, 81, 48, 21, 34, 5, 10, 88, 42, 7, 15, 96, 85, 62, 86, 52, 37}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{30, 12, 36, 19, 6, 1, 17, 35, 14, 29}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
