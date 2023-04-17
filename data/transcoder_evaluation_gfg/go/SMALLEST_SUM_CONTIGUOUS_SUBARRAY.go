package main

import (
		"fmt"
	"math"
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
		min_ending_here int = math.MaxInt64
		min_so_far      int = math.MaxInt64
	)
	for i := int(0); i < n; i++ {
		if min_ending_here > 0 {
			min_ending_here = arr[i]
		} else {
			min_ending_here += arr[i]
		}
		min_so_far = min(min_so_far, min_ending_here)
	}
	return min_so_far
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{2, 9, 13, 14, 15, 18, 19, 19, 25, 26, 29, 29, 29, 30, 31, 36, 37, 37, 38, 39, 39, 40, 40, 42, 42, 46, 50, 53, 58, 60, 62, 64, 65, 67, 68, 69, 72, 77, 78, 83, 85, 89, 90, 93, 95, 95, 97}
		param0_1  []int  = []int{14, -58, 8, 78, -26, -20, -60, 42, -64, -12}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{44, 88, 20, 47, 69, 42, 26, 49, 71, 91, 18, 95, 9, 66, 60, 37, 47, 29, 98, 63, 15, 9, 80, 66, 1, 9, 57, 56, 20, 2, 1}
		param0_4  []int  = []int{-78, -64, -62, -60, -52, 4, 8, 46, 72, 74}
		param0_5  []int  = []int{0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1}
		param0_6  []int  = []int{3, 7, 16, 17, 23, 23, 23, 28, 29, 30, 34, 38, 40, 41, 43, 43, 44, 46, 51, 51, 51, 55, 57, 58, 61, 62, 66, 66, 67, 69, 70, 73, 75, 77, 79, 80, 85, 85, 87, 87, 93, 96}
		param0_7  []int  = []int{80, 22, 38, 26, 62, -48, -48, 46, -54, 4, 76, 46, 48, 40, -92, -98, -88, 12, -42, -94, 76, -16, -82, 62, 18, -24}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{85, 44, 1, 97, 50, 74, 62, 90, 3, 78, 8, 48, 96, 41, 36, 91, 57, 97, 85, 90, 78, 43, 28, 92, 85, 59, 29, 38, 34, 65, 20, 26, 27, 23, 71, 22, 47, 99, 68, 93, 67, 66, 69, 82, 98, 15, 44, 51, 65}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{24, 6, 8, 26, 8, 11, 38, 22, 13, 45}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
