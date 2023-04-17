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
	if n == 1 || n == 0 {
		return 1
	}
	if arr[n-1] < arr[n-2] {
		return 0
	}
	return f_gold(arr, n-1)
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{1, 4, 19, 21, 28, 32, 35, 44, 51, 55, 62, 80, 80, 83, 90, 93, 93}
		param0_1  []int  = []int{84, -28, -42, 38, -94, -70, 34, 54, 38, -58, -54, -6, 72, -32, -18, 80, -6, -38, -30, -86, -10, 14, 92, -56, 40, -58, -2, -6, -46, -80, 72, -12, 2, -64, 36, 98, -24}
		param0_2  []int   = []int{0, 1, 1, 1}
		param0_3  []int  = []int{74, 75, 9, 13, 57, 82, 57, 37, 47, 11, 28, 6, 33, 14, 47, 29, 15, 56, 69, 86, 31, 19, 18, 58, 70, 73, 30, 95, 35, 17, 16, 97, 68, 95, 33, 36, 11, 60, 4, 63, 5, 64, 85, 77, 4}
		param0_4  []int  = []int{-96, -92, -84, -78, -74, -68, -66, -64, -62, -50, -48, -48, -46, -38, -28, -28, -26, -24, -24, -20, -14, -12, -4, 16, 18, 28, 32, 48, 50, 62, 70, 72, 78, 90, 92}
		param0_5  []int  = []int{0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0}
		param0_6  []int  = []int{6, 8, 11, 21, 29, 31, 41, 50, 56, 56, 69, 69, 74, 79, 86, 88, 93, 95, 99}
		param0_7  []int  = []int{10, -12, -36, 72, -42, -94, 38, -78, -4, 6, 12, 6, -48}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{97, 58, 88, 20, 63, 1, 23, 33, 57, 81, 54, 66, 95, 31, 54, 16, 37, 7, 1, 94, 18, 42, 39, 26, 75, 65, 57, 69, 86, 77, 17, 7, 71, 12, 38, 87, 48, 55, 54, 72, 15, 30, 55}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{8, 21, 2, 31, 31, 38, 10, 6, 35, 29}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
