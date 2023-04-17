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


func f_gold(arr []int, n int, x int, y int) int {
	var (
		i        int = 0
		min_dist int = math.MaxInt64
		prev     int
	)
	for i = 0; i < n; i++ {
		if arr[i] == x || arr[i] == y {
			prev = i
			break
		}
	}
	for ; i < n; i++ {
		if arr[i] == x || arr[i] == y {
			if arr[prev] != arr[i] && (i-prev) < min_dist {
				min_dist = i - prev
				prev = i
			} else {
				prev = i
			}
		}
	}
	return min_dist
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{4, 7, 7, 8, 11, 14, 16, 25, 34, 35, 36, 36, 38, 40, 41, 43, 45, 47, 57, 60, 64, 72, 73, 74, 75, 82, 83, 83, 84, 84, 84, 92}
		param0_1  []int  = []int{96, 70, 88, -64, -42, 58, 92, 66, -14, 90, -66, 12, 88, -12, 48, -4, 90, 24, 98, 14, 32, 38, 98, 78, 2, 26, 12, -36, 90, 80, 40, 58, 88, 64, 16}
		param0_2  []int   = []int{0, 0, 1}
		param0_3  []int  = []int{46, 96, 82, 73, 30, 36, 56, 20, 5, 36, 4, 7, 89, 63, 54, 97, 80, 56, 93, 34, 90, 56, 25, 27, 75, 68, 14, 90}
		param0_4  []int  = []int{-96, -88, -82, -66, -62, -52, -52, -46, -46, -40, -40, -28, -24, -12, 0, 4, 10, 24, 42, 46, 48, 48, 50, 60, 62, 64, 64, 70, 92, 98}
		param0_5  []int  = []int{0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1}
		param0_6  []int  = []int{1, 2, 2, 6, 10, 14, 15, 18, 19, 22, 23, 29, 30, 37, 40, 40, 41, 41, 42, 42, 44, 46, 46, 54, 56, 72, 73, 81, 83, 83, 86, 88, 93}
		param0_7  []int  = []int{46, 86, -52, 18, -32, 86, 2, 38, 72, 72, -60, 70, -58, 66, -66, -72, -74, 58, 52, 58, 16, 64, 62, -62, 80, -70, -96, -44, -20, -74, -10, 14, -32, 48, 30, 76, -16, 80, 66, -46, -92, 26, -86, 28, -76, -24, -98, 54, 50}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{32, 65, 10, 72, 17, 58, 79, 28, 67, 36, 18, 35}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{22, 25, 1, 26, 24, 10, 27, 30, 38, 7}
		param2    []int  = []int{7, 58, 1, 54, 0, 0, 1, 25, 0, 10}
		param3    []int  = []int{40, 70, 1, 82, 4, 1, 42, 45, 0, 7}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i], param3[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i], param3[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
