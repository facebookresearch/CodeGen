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
	if k > n {
		return -1
	}
	var sum int = arr[0]
	for i := int(1); i < k; i++ {
		sum += arr[i]
	}
	var max_sum int = sum
	var max_end int = k - 1
	for i := int(k); i < n; i++ {
		var sum int = sum + arr[i] - arr[i-k]
		if sum > max_sum {
			max_sum = sum
			max_end = i
		}
	}
	return max_end - k + 1
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{2, 5, 11, 37, 41, 49, 49, 63, 98}
		param0_1  []int  = []int{84, -72, 12, 0, 86, -32, -18, 48, 60, 42, 8, -6, -10, -6, -52, -84, -98, 76, -10, -14, -94, -48, 94, -10, -20, 40, -52, 0, 94, -68, 44, -34, -26, -6, -94, 34, -80, -62, -40, 56, 52, -20, 74, -46, -88, -26, 22}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{94, 97, 74, 88, 14, 66, 65, 50, 76, 55, 70, 93, 53, 30, 2, 60, 65, 24, 80, 73, 84, 95, 49, 32, 55, 70, 17, 26, 96, 20, 36, 2, 89, 49, 83, 67, 42, 51, 71, 11, 61, 78, 17, 78, 94, 68}
		param0_4  []int   = []int{-98, -90, -60, -38, 38, 42}
		param0_5  []int   = []int{1, 0, 0, 1, 1, 1, 1}
		param0_6  []int  = []int{4, 9, 17, 17, 19, 32, 35, 36, 37, 40, 44, 45, 47, 48, 48, 56, 56, 60, 61, 65, 66, 79, 83, 91, 93, 99}
		param0_7  []int  = []int{78, 82, -92, -46, -16, -64, 28, 60, 64, 52, 54, -84, 70, 22, 24, 0, -14, 20, -90, 30, 0, 86, 12, 72, -64, -52, 86, 16, -42}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{81, 77, 6, 3, 72, 24, 75, 47, 17, 29, 69, 15, 15, 50, 30, 83, 11, 7, 59, 7, 12, 82, 45, 76, 9, 48, 98, 49, 29, 66, 3, 53, 37, 13, 72, 58, 37, 87, 55}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{8, 34, 11, 35, 3, 3, 22, 25, 25, 34}
		param2    []int  = []int{7, 43, 18, 33, 5, 4, 24, 27, 20, 23}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
