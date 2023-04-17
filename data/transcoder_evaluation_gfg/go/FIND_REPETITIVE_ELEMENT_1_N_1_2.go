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
	var res int = 0
	for i := int(0); i < n-1; i++ {
		res = res ^ (i + 1) ^ arr[i]
	}
	res = res ^ arr[n-1]
	return res
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{2, 2, 4, 5, 5, 7, 7, 7, 8, 11, 14, 15, 18, 19, 20, 25, 25, 29, 29, 31, 32, 32, 33, 38, 42, 48, 52, 55, 60, 61, 63, 71, 74, 78, 82, 82, 84, 84, 87, 87, 88, 90, 93, 94, 94}
		param0_1  []int  = []int{46, 2, 62, 60, 92, 4, 26, 66, 66, 90, 26, -14, 76, -20, -68}
		param0_2  []int   = []int{0, 0, 0, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{87, 67, 11, 47, 64, 81, 94, 75, 58, 77, 18, 2, 85, 26, 6, 44, 55, 19, 46, 49, 5, 69, 44, 12, 42, 66, 46, 9, 26, 49, 68, 95, 6, 9, 11, 72, 5, 67}
		param0_4  []int  = []int{-98, -94, -92, -82, -78, -64, -62, -58, -52, -44, -40, -38, -8, 6, 10, 20, 22, 28, 30, 30, 36, 54, 54, 58, 64, 68, 76, 78, 84, 88, 90, 94, 96}
		param0_5  []int  = []int{1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1}
		param0_6  []int  = []int{1, 14, 15, 15, 21, 34, 38, 39, 41, 50, 60, 74, 96, 97}
		param0_7  []int   = []int{96, -12, -16, -52}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{66, 21, 21, 59, 78, 8, 46, 41, 16, 32, 97, 93, 32, 86, 91, 61, 67, 61, 97, 49, 66, 35, 24, 35, 65, 45, 83}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{31, 8, 4, 34, 29, 17, 7, 3, 21, 25}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
