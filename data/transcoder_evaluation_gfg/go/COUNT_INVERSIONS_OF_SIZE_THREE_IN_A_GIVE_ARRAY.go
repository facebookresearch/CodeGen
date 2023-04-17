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
	var invcount int = 0
	for i := int(0); i < n-2; i++ {
		for j := int(i + 1); j < n-1; j++ {
			if arr[i] > arr[j] {
				for k := int(j + 1); k < n; k++ {
					if arr[j] > arr[k] {
						invcount++
					}
				}
			}
		}
	}
	return invcount
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{11, 17, 27, 29, 31, 31, 32, 44, 45, 93}
		param0_1  []int  = []int{-48, -10, -44, -94, 50, -24, 30, 72, -6, 56, 94, -44, -96, -52, -2, 68, -52, 30, 98, 0, 12, -98, -94, 48, -96, -86}
		param0_2  []int   = []int{0, 0, 0, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{78, 82, 51, 92, 88, 95}
		param0_4  []int  = []int{-98, -96, -84, -72, -70, -62, -62, -58, -56, -54, -52, -52, -52, -50, -40, -40, -38, -36, -34, -26, -26, -22, -22, -20, -12, -8, -2, 4, 14, 14, 18, 22, 28, 32, 34, 34, 42, 44, 54, 58, 60, 64, 74, 80, 88, 90, 92, 94, 96}
		param0_5  []int   = []int{1, 0, 0, 0}
		param0_6  []int  = []int{2, 3, 5, 5, 5, 7, 7, 15, 16, 21, 29, 29, 35, 39, 39, 40, 42, 44, 46, 48, 48, 52, 52, 52, 54, 55, 57, 62, 67, 67, 67, 70, 71, 71, 76, 78, 79, 87, 94, 96}
		param0_7  []int   = []int{-60, -42, 20, 52, -54, 40, 56}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{98, 81, 23, 71, 82, 31, 15, 21, 4, 68, 68, 22, 77, 83, 22, 9, 10, 56}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{5, 15, 6, 3, 47, 3, 39, 6, 37, 13}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
