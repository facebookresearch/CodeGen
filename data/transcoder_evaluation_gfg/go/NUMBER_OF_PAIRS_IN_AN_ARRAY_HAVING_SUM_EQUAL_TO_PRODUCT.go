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


func f_gold(a []int, n int) int {
	var (
		zero int = 0
		two  int = 0
	)
	for i := int(0); i < n; i++ {
		if a[i] == 0 {
			zero++
		}
		if a[i] == 2 {
			two++
		}
	}
	var cnt int = (zero*(zero-1))/2 + (two*(two-1))/2
	return cnt
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{9, 10, 20, 26, 26, 28, 31, 34, 35, 36, 36, 37, 39, 43, 44, 44, 46, 49, 54, 57, 58, 63, 64, 64, 65, 67, 70, 70, 74, 75, 77, 78, 79, 81, 82, 83, 84, 86, 95}
		param0_1  []int  = []int{0, -10, 10, 0, 68, 4, -6, -14, 74, -80, 56, -4, 36, 56, 10, -16, 90, 84, -38, -40, 40, -86, -36, -16, -48, -76, -72, -18, -14, -40, -82, 56, -60}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{88, 20, 53, 21, 29, 73, 62, 91, 72, 34, 47, 42, 98, 9, 79, 80, 94, 36, 7, 67, 96, 34, 99, 56, 37, 70, 55, 36, 10, 77, 41, 51, 5, 37, 57, 29, 56, 74, 97, 31, 96, 52, 13, 29, 87, 58, 28, 31}
		param0_4  []int   = []int{20}
		param0_5  []int  = []int{1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1}
		param0_6  []int  = []int{2, 4, 9, 16, 22, 23, 25, 33, 33, 36, 39, 48, 49, 52, 53, 60, 67, 68, 76, 77, 79, 84, 84, 86, 89}
		param0_7  []int  = []int{-62, 42, -88, -44, 90, 30, 52, 54, 56, -72, -76, 90, 18, 42, 62, -84, 56, -80, 72}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int   = []int{22, 15, 28, 29, 32, 16, 33, 83}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{31, 19, 22, 38, 0, 21, 24, 13, 15, 7}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
