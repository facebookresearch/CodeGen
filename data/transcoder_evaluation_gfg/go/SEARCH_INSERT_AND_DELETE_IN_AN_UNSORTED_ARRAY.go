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


func f_gold(arr []int, n int, key int) int {
	var i int
	for i = 0; i < n; i++ {
		if arr[i] == key {
			return i
		}
	}
	return -1
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{4, 8, 11, 23, 55, 57, 73, 74, 77, 79, 93}
		param0_1  []int  = []int{-88, 12, -62, -66, -24, 18, 12, 22, 94, 30, -50, -42, -94, 18, 76, -6, -48, -68, 48, 36, -78, 52, -82, 76, 2, -44, -10, 88}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{33, 9, 93, 70, 81, 70, 56, 66, 72, 81, 74, 32, 71, 72, 3, 81, 70, 22, 82, 2, 75, 18, 90, 29, 48}
		param0_4  []int  = []int{-98, -70, -62, -60, -60, -54, -48, -48, -46, -44, -34, -26, -18, -6, 4, 18, 28, 32, 34, 40, 50, 54, 56, 62, 64, 64, 98}
		param0_5  []int  = []int{1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1}
		param0_6  []int  = []int{4, 6, 7, 10, 10, 12, 13, 18, 23, 29, 29, 34, 46, 54, 60, 61, 63, 67, 69, 70, 72, 76, 79, 79, 81, 82, 88, 90, 99}
		param0_7  []int  = []int{94, 34, -60, -74, 86, 80, 68, -48, 78, -62, -98, -44, -44, 92, -94, -86, -36, 12, 84, -90, 52, 42, -42, -66, 88, 76, 66}
		param0_8  []int   = []int{0, 0, 0, 1}
		param0_9  []int  = []int{76, 59, 38, 83, 38, 93, 27, 11, 17, 80, 26, 28, 35, 53, 88, 10, 9, 75}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{8, 27, 11, 24, 18, 17, 15, 21, 2, 12}
		param2    []int  = []int{11, 12, 0, 72, 23, 16, 28, 16, 3, 13}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
