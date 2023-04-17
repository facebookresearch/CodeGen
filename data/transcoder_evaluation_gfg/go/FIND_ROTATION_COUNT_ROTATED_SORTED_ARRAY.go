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
	var (
		min       int = arr[0]
		min_index int
	)
	for i := int(0); i < n; i++ {
		if min > arr[i] {
			min = arr[i]
			min_index = i
		}
	}
	return min_index
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{2, 4, 4, 9, 10, 13, 14, 15, 28, 28, 41, 46, 47, 48, 52, 55, 62, 67, 69, 73, 74, 79, 79, 80, 87, 90, 96, 99}
		param0_1  []int  = []int{44, 62, -40, 62, 98, 30, 16, 76, -4, -2, 78, -96, 78, -72, 94, -66, -38, -80, 40, 78, -26, 28, -40, -32, -64, 76, 26, -2, 12, 82, 16, -46, 10, 70, -62, -54, -6, 58, 32, 98}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{90, 26, 71, 74, 69, 47, 76, 96, 42, 31, 22, 17, 84, 20, 8, 98, 49, 87, 38, 53, 28, 77, 29}
		param0_4  []int  = []int{-64, -56, -10, -10, -6, -2, 0, 22, 78, 86, 98}
		param0_5  []int   = []int{0, 1, 1, 1, 1, 0, 1}
		param0_6  []int  = []int{2, 3, 3, 5, 8, 10, 11, 16, 17, 26, 35, 36, 38, 42, 59, 73, 73, 75, 75, 81, 82, 82, 86, 87, 88, 88, 90, 95, 96, 98, 98, 99}
		param0_7  []int  = []int{-96, 70, -32, -46, -26, 42, -56, 36, -72, 96, -54, -12, 78, 30, 58, 92, 56, 22, 70, 10, 42, 70, 0, -76, 58, -70, -66, -32, -30, -22, 56, 10, 18, -90, -40, -92, -70, -30, 48, 10, 32, 20, -52}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{35, 52, 21, 28, 96, 44, 80, 56, 10, 23, 48, 52, 15, 55, 43, 50, 6, 33, 62, 55, 39, 12, 31, 74, 53, 34, 41, 10, 52, 75, 57, 78, 3}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{27, 38, 11, 18, 9, 5, 29, 42, 28, 16}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
