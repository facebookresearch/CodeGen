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


func f_gold(arr []int, n int, x int) bool {
	for i := int(0); i < n-1; i++ {
		for j := int(i + 1); i < n; i++ {
			if arr[i]*arr[j] == x {
				return true
			}
		}
	}
	return false
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{3, 4, 5, 5, 6, 11, 18, 29, 29, 30, 35, 36, 38, 38, 40, 43, 43, 43, 50, 53, 58, 61, 62, 63, 64, 64, 65, 72, 73, 77, 78, 78, 84, 90, 94, 96}
		param0_1  []int  = []int{-72, 16, 0, 68, -58, 58, 46, 38, -28, -56, -28, -14, -56, 40, 30, 80, 94, -52, 0, -88, 8, -96, -52, -96, 48, -10, -32, -74, 88, 18, 70}
		param0_2  []int   = []int{0, 0, 0, 0, 0, 1, 1, 1, 1}
		param0_3  []int  = []int{78, 49, 30, 28, 71, 70, 29, 43, 91, 56, 51, 47, 21, 57, 69, 28, 68, 78, 38, 31, 35, 33, 55, 18, 88, 15, 69, 7, 51, 75, 8, 64, 6, 84, 79, 23, 62, 10, 71, 52, 77}
		param0_4  []int  = []int{-90, -86, -76, -72, -70, -62, -56, -50, -18, -12, -10, 4, 16, 26, 42, 48, 52, 54, 54, 70, 84, 86, 88, 98}
		param0_5  []int   = []int{1}
		param0_6  []int  = []int{4, 7, 14, 14, 16, 18, 19, 20, 22, 24, 29, 38, 38, 38, 40, 40, 46, 46, 47, 51, 51, 52, 55, 56, 56, 62, 62, 62, 78, 79, 81, 84, 86, 88, 89, 89, 89}
		param0_7  []int  = []int{72, 80, -82, 24, -98, 90, -32, -56, -22, 8, -12, 8, -78, 60, -62, 50, 12, -60, 10, -54, 74, 98, 26, 56, 24}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{93, 40, 48, 99, 95, 59, 43, 58, 79, 70, 28}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{28, 25, 7, 35, 23, 0, 23, 21, 22, 9}
		param2    []int  = []int{26, 16, 8, 25, 23, 0, 32, 19, 18, 5}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
