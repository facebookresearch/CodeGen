package main

import (
		"fmt"
"sort"
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


func f_gold(arr []int, n int, k int) int {
	var count int = 0
	sort.Ints(arr)
	var l int = 0
	var r int = 0
	for r < n {
		if arr[r]-arr[l] == k {
			count++
			l++
			r++
		} else if arr[r]-arr[l] > k {
			l++
		} else {
			r++
		}
	}
	return count
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{5, 5, 10, 19, 29, 32, 40, 60, 65, 70, 72, 89, 92}
		param0_1  []int  = []int{-38, 40, 8, 64, -38, 56, 4, 8, 84, 60, -48, -78, -82, -88, -30, 58, -58, 62, -52, -98, 24, 22, 14, 68, -74, 48, -56, -72, -90, 26, -10, 58, 40, 36, -80, 68, 58, -74, -46, -62, -12, 74, -58}
		param0_2  []int   = []int{0, 0, 1}
		param0_3  []int  = []int{16, 80, 59, 29, 14, 44, 13, 76, 7, 65, 62, 1, 34, 49, 70, 96, 73, 71, 42, 73, 66, 96}
		param0_4  []int  = []int{-98, -88, -58, -56, -48, -34, -22, -18, -14, -14, -8, -4, -2, 2, 18, 38, 42, 46, 54, 68, 70, 90, 94, 96, 98}
		param0_5  []int   = []int{0, 1, 1}
		param0_6  []int   = []int{11, 43, 50, 58, 60, 68, 75}
		param0_7  []int  = []int{86, 94, -80, 0, 52, -56, 42, 88, -10, 24, 6, 8}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{54, 99, 4, 14, 9, 34, 81, 36, 80, 50, 34, 9, 7}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{7, 24, 1, 12, 23, 2, 4, 11, 29, 9}
		param2    []int  = []int{12, 36, 1, 16, 22, 1, 4, 9, 30, 8}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
