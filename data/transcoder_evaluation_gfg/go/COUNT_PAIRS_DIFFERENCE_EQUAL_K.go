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


func f_gold(arr []int, n int, k int) int {
	var count int = 0
	for i := int(0); i < n; i++ {
		for j := int(i + 1); j < n; j++ {
			if arr[i]-arr[j] == k || arr[j]-arr[i] == k {
				count++
			}
		}
	}
	return count
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{9, 14, 17, 19, 22, 23, 23, 27, 30, 31, 34, 37, 37, 39, 39, 42, 57, 61, 68, 73, 77, 79, 91, 96, 97}
		param0_1  []int   = []int{-78, -42, 28, -88, 18, -52}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{8, 46, 57, 28, 80, 2, 75, 57, 83, 45, 32, 49, 77, 30, 94, 33, 23, 29, 35, 81, 85}
		param0_4  []int  = []int{-90, -72, -72, -62, -62, -54, -54, -52, -48, -38, -22, -22, -22, -12, -12, -8, -8, -8, -6, -6, -2, 6, 12, 26, 26, 28, 28, 38, 40, 48, 52, 52, 58, 60, 68, 70, 72, 76, 76, 76, 92}
		param0_5  []int  = []int{0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1}
		param0_6  []int  = []int{3, 13, 19, 23, 27, 32, 49, 52, 54, 57, 58, 58, 63, 67, 68, 68, 69, 70, 75, 80, 86, 90, 91, 95}
		param0_7  []int   = []int{-56, 40, -66, 42, 8, -40, -8, -42}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{99, 12, 90, 10, 86, 86, 81, 19, 1, 1, 98, 82, 34, 39, 34, 1, 54, 47, 39, 82, 21, 50, 82, 41, 98, 47, 88, 46, 72, 28, 28, 29, 60, 87, 92, 53, 93, 29, 74, 75, 11, 32, 48, 47, 85, 16, 20}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{19, 3, 16, 15, 22, 45, 19, 7, 16, 24}
		param2    []int  = []int{19, 4, 14, 11, 25, 39, 21, 6, 28, 45}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
