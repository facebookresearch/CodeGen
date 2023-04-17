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


func f_gold(arr []int, n int, x int, y int) int {
	var count int = 0
	for i := int(0); i < n; i++ {
		if arr[i] >= x && arr[i] <= y {
			count++
		}
	}
	return count
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{9, 16, 19, 24, 36, 38, 42, 49, 51, 53, 53, 57, 57, 58, 71, 78, 78, 92, 92, 93}
		param0_1  []int  = []int{28, -74, -18, 10, 26, 28, -96, -80, 82, 94, 22, 50, 72, -90, 76, 50, 20, -44, -80}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{25, 8, 66, 90, 50, 65, 76, 90, 27}
		param0_4  []int  = []int{-98, -96, -90, -82, -80, -78, -70, -66, -60, -60, -50, -48, -34, -26, -24, -16, -14, -8, -6, 4, 22, 24, 26, 30, 30, 48, 52, 56, 60, 62, 74, 76, 78, 86}
		param0_5  []int  = []int{1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0}
		param0_6  []int  = []int{4, 6, 17, 19, 24, 29, 30, 31, 32, 37, 37, 40, 43, 44, 44, 45, 57, 64, 69, 70, 73, 78, 86, 89, 91, 92, 94}
		param0_7  []int   = []int{32, -88, 70, -6, 28, -48}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{37, 84, 97, 74, 12, 26, 47, 10, 14, 33}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{13, 18, 30, 4, 32, 15, 17, 4, 13, 5}
		param2    []int  = []int{12, 13, 21, 8, 24, 16, 21, 3, 12, 9}
		param3    []int  = []int{13, 13, 31, 5, 24, 12, 15, 4, 11, 8}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i], param3[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i], param3[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
