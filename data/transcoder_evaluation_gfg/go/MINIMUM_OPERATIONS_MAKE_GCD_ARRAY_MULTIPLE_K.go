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


func f_gold(a []int, n int, k int) int {
	var result int = 0
	for i := int(0); i < n; i++ {
		if a[i] != 1 && a[i] > k {
			result = result + min(a[i]%k, k-a[i]%k)
		} else {
			result = result + k - a[i]
		}
	}
	return result
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{3, 7, 27, 32, 36, 37, 44, 48, 50, 64, 86}
		param0_1  []int   = []int{-22, 6, -20, 60, -74, 98, 52, -22}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{77, 11, 51, 11, 84, 79, 43, 12, 14, 50, 15, 6, 85, 32, 74, 49, 7, 2, 58}
		param0_4  []int  = []int{-90, -66, -64, -58, -46, -44, -32, -30, -30, -22, -18, -14, 12, 12, 18, 34, 44, 60, 70, 70, 74, 76, 86, 98, 98}
		param0_5  []int  = []int{1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1}
		param0_6  []int  = []int{9, 22, 27, 27, 37, 53, 53, 56, 63, 73, 76, 81, 82}
		param0_7  []int  = []int{-46, 60, 80, 80, 42, -98, 30, -48, 4, -32, -78, 40, 52, 26, 88, 4, 22, 62, 88, -94, 2, 0, 58, 38, 52, -50, -52, 58, -62, 30, -38, -8, -82, -66}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{42, 69, 93, 82, 8, 23, 73, 1, 77, 39, 49, 4, 95, 85}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{5, 5, 23, 9, 12, 36, 10, 18, 19, 12}
		param2    []int  = []int{10, 4, 29, 17, 22, 31, 11, 19, 22, 13}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
