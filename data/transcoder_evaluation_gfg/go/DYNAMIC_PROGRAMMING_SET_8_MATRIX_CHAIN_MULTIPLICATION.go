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


func f_gold(p []int, i int, j int) int {
	if i == j {
		return 0
	}
	var k int
	var min int = math.MaxInt64
	var count int
	for k = i; k < j; k++ {
		count = f_gold(p, i, k) + f_gold(p, k+1, j) + p[i-1]*p[k]*p[j]
		if count < min {
			min = count
		}
	}
	return min
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{6, 12, 16, 30, 31, 31, 33, 34, 45, 48, 57, 63, 81, 83}
		param0_1  []int  = []int{30, -78, 42, -6, 42, 56, -38, 28, -96, -96, 84, -18, 0, 20, -56, -40, -58, -74, 64, 62, -22, 78, 10, -22, 16, -48, 2, 14, 82, -92, -64, -18, 42, 24, 22, -50, 12, -76, 38, -30, -86, -58, -6, -4, 10, 28}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{54, 46}
		param0_4  []int  = []int{-80, -76, -68, -66, -54, -12, -10, -6, 6, 8, 20, 20, 22, 60, 66, 78, 78, 82, 98}
		param0_5  []int  = []int{0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0}
		param0_6  []int  = []int{14, 21, 29, 31, 37, 50, 51, 54, 57, 62, 64, 72, 85, 98}
		param0_7  []int  = []int{-86, 98, 90, -20, 90, 68, 70, -24, -10, -80, 70, -42, 14, 56, -26, -42, 2, -62, 24, 10, -46, -66, -82, -98, -84, -2, -52, -50, 0, -18, 90, -32, 98, 86}
		param0_8  []int   = []int{0, 0, 1, 1, 1, 1}
		param0_9  []int  = []int{52, 15, 61, 73, 45, 5, 15, 54, 69, 90, 5, 56, 13, 54, 27, 72, 58, 21, 35, 2, 59, 55, 64, 92, 54, 63, 50, 95, 38, 53, 38, 53, 73, 27, 86, 86, 99, 42, 85, 80, 43, 32, 80, 57, 78}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{10, 30, 7, 1, 13, 20, 7, 23, 5, 26}
		param2    []int  = []int{9, 27, 7, 1, 10, 17, 11, 26, 4, 42}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
