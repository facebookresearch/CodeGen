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
	for i := int(0); i <= (n-2)/2; i++ {
		if arr[i*2+1] > arr[i] {
			return false
		}
		if i*2+2 < n && arr[i*2+2] > arr[i] {
			return false
		}
	}
	return true
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{2, 2, 2, 7, 10, 14, 24, 38, 42, 50, 59, 60, 72, 73, 79, 83, 89}
		param0_1  []int  = []int{-48, 98, 96, -56, -2, 58, 52, -50, 58, 50, 62, 86, -26, -98, 34, 20, -28, 56, -36}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{91, 50, 37}
		param0_4  []int  = []int{-80, -26, 0, 0, 6, 14, 22, 76, 82, 88, 98}
		param0_5  []int   = []int{1, 0}
		param0_6  []int  = []int{9, 24, 24, 33, 48, 50, 55, 61, 69, 79, 83}
		param0_7  []int  = []int{30, 32, -82, -48, 88, -24, 74, 2, 90, 98, 68, 82, 32, -60, 2, -94, 18, 14, 46, 50, -60, -74, -76, 66, -76, -34, -20, 82, -44, -62, 34, 48, -56, 2, 64, -78, -64, 98, -10, -28, 78, -42}
		param0_8  []int  = []int{0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{38, 74, 99, 75, 44, 75, 24, 70, 78, 74, 60, 59, 34, 27, 7, 23, 19, 95, 4, 35, 38, 22, 46, 1, 44, 20, 52, 1, 96, 57, 5, 76, 49, 1, 37, 35}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{9, 9, 20, 2, 10, 1, 8, 27, 6, 31}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
