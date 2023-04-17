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
	var (
		i        int
		j        int
		leftsum  int
		rightsum int
	)
	for i = 0; i < n; i++ {
		leftsum = 0
		for j = 0; j < i; j++ {
			leftsum += arr[j]
		}
		rightsum = 0
		for j = i + 1; j < n; j++ {
			rightsum += arr[j]
		}
		if leftsum == rightsum {
			return i
		}
	}
	return -1
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{4, 6, 7, 8, 15, 15, 19, 23, 27, 28, 29, 31, 37, 40, 41, 42, 50, 51, 57, 58, 63, 63, 64, 70, 71, 72, 78, 83, 85, 90, 90}
		param0_1  []int   = []int{-68, -92}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{80, 74, 45, 81, 62, 88, 90, 54}
		param0_4  []int  = []int{-92, -84, -84, -66, -64, -50, -50, -48, -46, -44, -36, -36, -30, -24, -22, -16, -6, -2, 24, 48, 54, 62, 66, 74, 74, 80, 82, 88, 98, 98}
		param0_5  []int  = []int{0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1}
		param0_6  []int  = []int{2, 6, 11, 12, 14, 36, 45, 49, 52, 52, 58, 63, 70, 73, 74, 80, 82, 89, 89}
		param0_7  []int  = []int{16, -58, -14, -58, -36, -70, 36, -8, -14, -78, -26, 42, 16, 18, 0, -44, 32, 50, -78, 58, 78, 16, -34, -54, 50, 0, 46, -12, 52, -74, 78, -82, -26, -72, -86, -14, 86, 40, -8}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{58, 82, 79, 77, 84, 79, 39, 98, 53, 84, 19, 9, 93, 30, 6, 82, 8, 43, 17, 44, 62, 21, 34, 86, 98, 44, 81, 14, 82, 54, 44, 53, 36, 33, 2, 68, 19, 37}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{25, 1, 26, 4, 27, 43, 17, 26, 33, 22}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
