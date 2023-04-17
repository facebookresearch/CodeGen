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


func f_gold(arr []int, i int, n int) bool {
	if i > (n-2)/2 {
		return true
	}
	if arr[i] >= arr[i*2+1] && arr[i] >= arr[i*2+2] && f_gold(arr, i*2+1, n) && f_gold(arr, i*2+2, n) {
		return true
	}
	return false
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{1, 2, 3, 5, 24, 24, 25, 25, 36, 37, 37, 39, 42, 44, 46, 50, 51, 54, 56, 60, 62, 70, 71, 73, 75, 80, 80, 85, 86, 89, 91, 95, 99}
		param0_1  []int  = []int{-44, -58, 88, -42, 42, -14, -44, 42, 64, 94, -46, -70, 34, -10, -46, -52, -6, -78, 64, 56, 74, 98, -34, -4, -92, 6, -52, -20, 78, -72, -40}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{10, 2, 1, 34, 21, 37, 49, 31, 70, 97, 87, 50, 76, 55}
		param0_4  []int  = []int{-94, -84, -82, -66, -64, -62, -56, -38, -24, -24, -4, 2, 4, 4, 8, 14, 16, 20, 30, 34, 34, 48, 58, 58, 70, 76, 78, 86, 88, 96, 98}
		param0_5  []int  = []int{1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0}
		param0_6  []int   = []int{5, 20, 30, 5, 10, 21, 5}
		param0_7  []int   = []int{50, 20, 30, 5, 10, 21, 5}
		param0_8  []int   = []int{50, 20, 30, 5, 10, 21, 5}
		param0_9  []int   = []int{50, 20, 30, 5, 10, 21, 5}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{0, 0, 0, 0, 29, 12, 0, 0, 2, 7}
		param2    []int  = []int{18, 27, 20, 8, 26, 11, 7, 7, 7, 7}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
