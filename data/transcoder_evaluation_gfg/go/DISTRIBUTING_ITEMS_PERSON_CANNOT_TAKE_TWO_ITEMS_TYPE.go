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


func f_gold(arr []int, n int, k int) bool {
	var count int
	for i := int(0); i < n; i++ {
		count = 0
		for j := int(0); j < n; j++ {
			if arr[j] == arr[i] {
				count++
			}
			if count > k*2 {
				return false
			}
		}
	}
	return true
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{1, 1, 2, 3, 1}
		param0_1  []int   = []int{2, 3, 3, 5, 3, 3}
		param0_2  []int   = []int{0, 0, 1, 1, 1}
		param0_3  []int  = []int{7, 60, 78, 91, 80, 75, 85, 21, 41, 63, 1, 84, 69, 13, 94, 25, 54, 54, 52, 68, 53, 35, 17, 37, 98, 27, 2, 31}
		param0_4  []int  = []int{-96, -94, -82, -80, -78, -66, -36, -24, -18, -12, -2, -2, 6, 8, 10, 12, 36, 38, 42, 58, 64, 68, 82, 84, 86, 88, 94}
		param0_5  []int  = []int{0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0}
		param0_6  []int  = []int{16, 19, 25, 25, 32, 37, 48, 59, 60, 60, 71, 74, 77, 81, 91, 94}
		param0_7  []int  = []int{-62, -94, 72, -22, 86, -80, 64, 98, -82, -50, 12, -4, 56, 46, -80, 2, -86, -44, -26, 68, -94, -82, 74, 26, 94, 40, 50, -40, -42, -10}
		param0_8  []int   = []int{0, 0, 0, 0, 0, 1, 1, 1}
		param0_9  []int  = []int{83, 57, 2, 47, 70, 22, 49, 51, 25, 57, 32, 7, 8, 99, 6, 86, 24, 79, 42, 43, 1, 24, 68, 11, 24, 12, 43, 40, 14, 45, 11, 46, 12, 80, 66}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{5, 6, 2, 24, 24, 34, 10, 20, 5, 21}
		param2    []int  = []int{2, 2, 1, 2, 3, 2, 8, 4, 2, 33}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
