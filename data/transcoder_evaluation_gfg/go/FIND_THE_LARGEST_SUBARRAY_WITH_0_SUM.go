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
	var max_len int = 0
	for i := int(0); i < n; i++ {
		var curr_sum int = 0
		for j := int(i); j < n; j++ {
			curr_sum += arr[j]
			if curr_sum == 0 {
				max_len = max(max_len, j-i+1)
			}
		}
	}
	return max_len
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{1, 2, 6, 6, 15, 23, 26, 27, 30, 34, 35, 38, 42, 43, 44, 46, 50, 53, 53, 57, 62, 65, 67, 70, 76, 79, 81, 82, 85, 90}
		param0_1  []int  = []int{72, -6, -24, -82, 16, 78, -82, 38, -2, 78, -60, 40, 26, -82, -32, -56, 52, 14, 62, -18, -84, -94, 48, 54, 2, -28}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{14, 67, 44, 5, 60, 87, 23, 37, 44, 70, 47, 52, 38, 30, 78, 60, 95, 62, 3, 45, 96, 35, 81, 8, 82, 75, 76, 64, 33, 65, 65, 49, 1, 63, 99, 53, 40, 12, 46, 93, 88, 27, 89, 89, 60, 3, 92, 63}
		param0_4  []int  = []int{-98, -98, -96, -86, -74, -74, -72, -70, -70, -66, -66, -66, -64, -64, -50, -50, -48, -38, -28, -24, -24, -18, -16, -14, -8, -6, -2, -2, 10, 28, 32, 38, 42, 54, 54, 62, 68, 84, 88}
		param0_5  []int  = []int{0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0}
		param0_6  []int  = []int{6, 14, 26, 27, 37, 50, 51, 54, 55, 67, 68, 72, 83, 84, 95, 99}
		param0_7  []int  = []int{-6, -96, -46, 4, -50, -56, -34, 6, -72, -68, 92, 88, -80, 18, 58, 20, 34, -22, -18, -90, -80, -24, -82, 6, 54, 70, 22, 94}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{65, 34, 82, 43, 15, 94, 34, 50, 70, 77, 83, 26, 85, 5}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{19, 24, 18, 39, 25, 12, 10, 22, 45, 10}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
