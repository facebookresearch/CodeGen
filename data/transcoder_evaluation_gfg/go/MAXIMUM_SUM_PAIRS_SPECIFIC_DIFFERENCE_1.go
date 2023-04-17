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


func f_gold(arr []int, N int, k int) int {
	var maxSum int = 0
	sort.Ints(arr)
	for i := int(N - 1); i > 0; i-- {
		if arr[i]-arr[i-1] < k {
			maxSum += arr[i]
			maxSum += arr[i-1]
			i--
		}
	}
	return maxSum
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{2, 10, 11, 11, 12, 14, 15, 17, 27, 27, 28, 36, 36, 44, 47, 47, 54, 55, 62, 64, 68, 69, 70, 70, 75, 76, 78, 85, 85, 91, 95, 97}
		param0_1  []int  = []int{-36, 78, 10, 30, -12, -70, -98, -14, -44, -66, -40, -8, 78, 2, -70, 40, 92, 58, 30, 10, -84, -62, -86, -50, 82, 36, -92, -30, -2, -34, 88, 2, -4, -72}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{77, 78, 58}
		param0_4  []int  = []int{-88, -88, -88, -82, -58, -54, -48, -46, -46, -44, -20, -2, 10, 28, 28, 28, 42, 42, 44, 50, 50, 54, 56, 58, 62, 68, 70, 72, 74, 76, 78, 88, 90, 92}
		param0_5  []int  = []int{0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1}
		param0_6  []int  = []int{5, 7, 10, 11, 15, 17, 20, 20, 29, 29, 32, 37, 38, 39, 40, 41, 45, 51, 60, 64, 64, 68, 68, 70, 71, 71, 71, 75, 76, 82, 84, 87, 88, 88, 95, 98}
		param0_7  []int  = []int{-46, -32, 76, -28, 44, -14, 94, -4, 60, -88, -52, 32, -66, 28, 94, 76, 86, -4, 74, 52, 64, -36, -98, -40, 70, 18, -22, -20, -16, -74, 12, 60, 94, 98, -28, -24, 4, -34, -60, 56}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{79, 13, 25, 22, 61, 1, 2, 73, 66, 94, 47, 9, 1, 99, 25, 39, 95, 46, 95, 20, 63, 15, 14, 36, 9, 91, 14}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{26, 26, 47, 1, 21, 41, 30, 33, 28, 19}
		param2    []int  = []int{18, 25, 26, 1, 24, 40, 21, 23, 41, 23}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
