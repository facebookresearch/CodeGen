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


func f_gold(arr []int, low int, high int) int {
	var (
		max int = arr[low]
		i   int
	)
	for i = low + 1; i <= high; i++ {
		if arr[i] > max {
			max = arr[i]
		} else {
			break
		}
	}
	return max
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{11, 15, 16, 19, 24, 25, 26, 28, 34, 34, 43, 61, 63, 66, 67, 72, 77, 79, 81, 83, 87, 94, 99}
		param0_1  []int   = []int{8, 92}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{84, 39, 92, 89, 38, 75, 18, 39, 83, 67, 41, 46, 49, 27}
		param0_4  []int  = []int{-98, -94, -88, -84, -74, -72, -58, -52, -48, -48, -46, -42, -42, -32, -30, -30, -18, -10, -8, -8, -6, -4, 4, 6, 28, 30, 34, 38, 44, 48, 56, 58, 60, 64, 86}
		param0_5  []int   = []int{0, 1, 0}
		param0_6  []int  = []int{5, 9, 10, 16, 18, 19, 23, 24, 26, 33, 37, 44, 46, 54, 55, 57, 58, 59, 63, 64, 70, 75, 77, 81, 83, 84, 85, 85, 88, 89, 96, 97, 99}
		param0_7  []int   = []int{86, 20, -50, 74, -78, 86}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{16, 57, 65, 61, 17, 63, 7, 35, 69, 91, 30, 44, 99, 80, 6, 80, 56, 8, 84, 95, 20, 73, 30, 62, 77, 26, 66, 61, 61, 45}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{15, 1, 23, 8, 31, 2, 20, 3, 19, 28}
		param2    []int  = []int{21, 1, 15, 13, 34, 2, 31, 5, 18, 22}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
