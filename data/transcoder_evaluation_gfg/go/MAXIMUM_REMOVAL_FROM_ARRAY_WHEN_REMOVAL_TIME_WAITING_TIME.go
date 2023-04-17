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


func f_gold(arr []int, n int) int {
	var (
		count           int = 0
		cummulative_sum int = 0
	)
	sort.Ints(arr)
	for i := int(0); i < n; i++ {
		if arr[i] >= cummulative_sum {
			count++
			cummulative_sum += arr[i]
		}
	}
	return count
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{7, 33, 34, 42, 42, 45, 73}
		param0_1  []int  = []int{32, -10, -64, -20, 92, -66, 6, 44, -62, -98, 4, -48, 44, 42, 12, -90, 52, 86, -30, -80, 64, 94, 14}
		param0_2  []int   = []int{0, 0, 0, 0, 1}
		param0_3  []int   = []int{11, 85, 89, 71, 82, 44}
		param0_4  []int  = []int{-96, -92, -78, -72, -68, -58, -52, -50, -50, -48, -42, -32, -20, -18, -4, 0, 0, 2, 18, 18, 20, 24, 32, 34, 36, 38, 38, 60, 66, 68, 70, 72, 72, 74, 76, 96, 98}
		param0_5  []int  = []int{0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1}
		param0_6  []int  = []int{8, 9, 10, 11, 12, 15, 17, 19, 20, 21, 24, 30, 33, 35, 36, 39, 41, 41, 42, 54, 62, 63, 68, 70, 71, 72, 77, 85, 86, 86, 94, 95, 97, 97}
		param0_7  []int  = []int{96, 22, -60, 4, -94, -16, 46, 10, 76, -90, 4, 70, -72, 60, 28, -24, -66, 92, -70, 72, 36}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{90, 63, 16, 40, 28, 97, 20, 63, 42, 31, 57, 84, 10, 12, 59, 69, 47, 7, 53, 67}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{5, 16, 2, 3, 21, 16, 31, 20, 13, 10}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
