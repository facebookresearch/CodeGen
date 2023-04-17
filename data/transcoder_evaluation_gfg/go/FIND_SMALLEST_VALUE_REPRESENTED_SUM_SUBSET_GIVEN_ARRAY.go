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
	var res int = 1
	for i := int(0); i < n && arr[i] <= res; i++ {
		res = res + arr[i]
	}
	return res
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{16, 23, 24, 41, 48, 58, 72, 75}
		param0_1  []int  = []int{-14, -82, 12, -14, -38, 12, 40, 12, -74, 42, -36, 64}
		param0_2  []int   = []int{0, 0, 1, 1, 1, 1}
		param0_3  []int   = []int{17, 89, 44}
		param0_4  []int  = []int{-94, -92, -84, -82, -72, -58, -56, -40, -34, -34, -24, -22, -8, -8, 12, 14, 16, 16, 22, 22, 34, 46, 54, 58, 68, 72, 74, 78, 88, 96}
		param0_5  []int  = []int{0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0}
		param0_6  []int  = []int{2, 12, 13, 13, 13, 16, 28, 32, 34, 41, 41, 47, 49, 49, 50, 52, 58, 61, 63, 65, 67, 68, 68, 74, 80, 80, 84, 84, 89, 93, 94, 98, 99, 99}
		param0_7  []int   = []int{-54}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{42, 50, 76, 45, 6, 63, 46, 73, 65, 70, 87, 5, 41, 63, 96, 75, 38, 76, 27, 7, 71, 9, 65, 44, 76, 37, 94, 52, 55, 3, 38, 68, 45, 15, 35, 90, 36, 46, 13, 92, 32, 22, 49, 35, 83}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{4, 8, 5, 2, 25, 8, 23, 0, 33, 35}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
