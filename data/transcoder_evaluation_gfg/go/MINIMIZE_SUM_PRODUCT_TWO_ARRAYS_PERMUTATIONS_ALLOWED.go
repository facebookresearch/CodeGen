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


func f_gold(A []int, B []int, n int) int {
	sort.Ints(A)
	sort.Ints(B)
	var result int = 0
	for i := int(0); i < n; i++ {
		result += A[i] * B[n-i-1]
	}
	return result
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{31, 85}
		param0_1  []int  = []int{22, -6, 84, 70, 84, 6, 28, -74, -14, 68, 22, 90, -10}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{12, 33, 93, 2, 83, 9, 61, 84, 9, 69, 2}
		param0_4  []int  = []int{-92, -88, -84, -78, -78, -76, -66, -54, -52, -48, -46, -44, -40, -34, -32, -24, -20, -14, -6, -4, 2, 6, 10, 10, 22, 26, 32, 36, 36, 40, 46, 48, 56, 58, 64, 76, 80, 80, 80, 84, 84, 84, 92}
		param0_5  []int  = []int{1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0}
		param0_6  []int  = []int{4, 6, 6, 20, 22, 23, 26, 39, 40, 47, 50, 68, 68, 70, 73, 77, 80, 82, 85}
		param0_7  []int   = []int{78, 60, -8, 46, -12}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{60, 66, 84, 99, 85, 89, 28, 97, 85, 71, 53, 93, 23, 9, 45, 26, 49, 95, 64, 33, 70, 34, 10, 1, 68, 39, 53, 12}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1_0  []int   = []int{18, 33}
		param1_1  []int  = []int{2, -48, -36, -4, -22, -98, -74, -92, -72, -4, 48, -32, 94}
		param1_2  []int  = []int{0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param1_3  []int  = []int{85, 92, 92, 1, 54, 31, 69, 4, 39, 81, 52}
		param1_4  []int  = []int{-98, -90, -82, -80, -76, -66, -62, -62, -62, -50, -50, -50, -32, -30, -14, -12, 4, 6, 12, 14, 16, 30, 30, 30, 32, 34, 40, 42, 50, 52, 56, 58, 60, 62, 62, 64, 66, 68, 78, 82, 86, 90, 94}
		param1_5  []int  = []int{0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1}
		param1_6  []int  = []int{2, 3, 15, 21, 22, 26, 35, 37, 37, 38, 57, 59, 62, 63, 64, 76, 81, 85, 91}
		param1_7  []int   = []int{-72, -80, -30, 16, -38}
		param1_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param1_9  []int  = []int{37, 33, 33, 77, 78, 34, 28, 1, 63, 15, 51, 50, 90, 22, 71, 23, 68, 55, 2, 22, 31, 54, 76, 36, 2, 27, 96, 89}
		param1    [][]int = [][]int{param1_0, param1_1, param1_2, param1_3, param1_4, param1_5, param1_6, param1_7, param1_8, param1_9}
		param2    []int  = []int{1, 6, 14, 7, 26, 32, 17, 2, 17, 15}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), ([]int)(param1[i]), param2[i]) == f_gold(([]int)(param0[i]), ([]int)(param1[i]), param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
