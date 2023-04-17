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


func f_gold(arr []int, n int) bool {
	if n == 0 || n == 1 {
		return true
	}
	for i := int(1); i < n; i++ {
		if arr[i-1] > arr[i] {
			return false
		}
	}
	return true
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{2, 3, 4, 10, 11, 13, 17, 19, 23, 26, 28, 29, 30, 34, 35, 37, 38, 38, 43, 49, 49, 50, 52, 53, 55, 55, 57, 58, 58, 59, 64, 66, 67, 70, 72, 72, 75, 77, 77, 87, 89, 89, 90, 91, 98, 99, 99, 99}
		param0_1  []int  = []int{56, -94, -26, -52, 58, -66, -52, -66, -94, 44, 38, -66, 70, -70, -80, -78, -72, -60, -76, 68, -50, 32, -16, 84, 74, -42, 98, -8, 72, 26, 24, 6, 24, 86, 86, 78, -92, 80, 32, -74, 26, 50, 92, 4, 2, -34, -2, -18, -10}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{38, 79, 76, 92, 92}
		param0_4  []int   = []int{-42, -28, 2, 32, 50, 56, 86, 96, 98}
		param0_5  []int  = []int{1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1}
		param0_6  []int  = []int{1, 9, 12, 21, 21, 24, 34, 55, 60, 63, 67, 68, 88, 89, 91, 94, 98, 99}
		param0_7  []int  = []int{-96, 96, -98, -42, -74, 40, 42, 50, -46, -52, 8, -46, 48, 88, -78, -72, -10, -20, 98, -40, -18, 36, 4, 46, 52, 28, -88, -28, -28, -86}
		param0_8  []int   = []int{0, 0, 0, 0, 1, 1}
		param0_9  []int  = []int{66, 12, 48, 82, 33, 77, 99, 98, 14, 92}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{46, 30, 13, 2, 7, 11, 9, 29, 3, 7}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
