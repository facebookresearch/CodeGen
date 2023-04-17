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


func f_gold(arr []int, n int) bool {
	if n == 0 || n == 1 {
		return true
	}
	for i := int(1); i < n; i++ {
		if arr[i-1] > arr[i] {
			return false
		}
	}
	return true
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{6, 8, 8, 16, 19, 19, 21, 23, 26, 33, 34, 36, 38, 39, 41, 41, 45, 47, 52, 52, 55, 57, 60, 60, 60, 61, 69, 69, 70, 70, 72, 73, 73, 75, 78, 81, 84, 84, 85, 88, 88, 89, 90, 91, 97}
		param0_1  []int  = []int{2, -90, 66, 24, -18, 70, 34, 18, 84, -62}
		param0_2  []int   = []int{1, 1}
		param0_3  []int  = []int{12, 88, 65, 82, 23, 39, 60, 27, 57, 44, 70, 28, 23, 34, 25, 11, 48, 65, 10, 73, 26, 10, 18, 60, 73, 45, 26, 9, 36, 15, 24, 40, 2, 4, 95, 20, 39, 45}
		param0_4  []int   = []int{-38, 38, 40, 72}
		param0_5  []int   = []int{1, 0, 0, 0, 1}
		param0_6  []int  = []int{11, 15, 16, 17, 17, 17, 22, 23, 23, 25, 27, 28, 28, 31, 33, 36, 38, 40, 42, 44, 46, 49, 51, 51, 52, 60, 62, 65, 67, 71, 74, 77, 77, 78, 78, 79, 83, 83, 86, 86, 87, 87, 87, 88, 91, 92, 97, 97, 97}
		param0_7  []int  = []int{-26, -90, -78, -76, -58, -64, -72, -34, -58, -48, 78, -50, -30, 26, -60, 26}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{56, 51, 63, 30, 10, 88, 23, 1, 48, 4, 28, 44}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{22, 9, 1, 23, 2, 3, 44, 9, 23, 10}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
