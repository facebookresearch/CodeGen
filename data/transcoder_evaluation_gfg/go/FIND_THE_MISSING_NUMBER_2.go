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
		x1 int = a[0]
		x2 int = 1
	)
	for i := int(1); i < n; i++ {
		x1 = x1 ^ a[i]
	}
	for i := int(2); i <= n+1; i++ {
		x2 = x2 ^ i
	}
	return x1 ^ x2
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{2, 5, 7, 8, 10, 14, 27, 32, 51, 52, 57, 58, 65, 68, 68, 72, 73, 73, 83, 92, 98}
		param0_1  []int  = []int{-60, -48, 38, -78, 88, 86, -4, -94, 16, -64, 32, 88, 58, -78, -16, 48, 38, 30, 66, -60, 20, 40, -28, -64, -48, -86, -80, -8, -58, 52, 80, -32, 46, -4, -70, 76, -4, 78, -64, 38, -40}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{69, 59, 22, 33, 69, 28, 11, 34, 72, 88, 16, 30, 69, 89, 43, 4, 65, 85, 27}
		param0_4  []int  = []int{-98, -98, -92, -88, -88, -82, -74, -70, -68, -60, -60, -48, -38, -34, -34, -24, 14, 38, 50, 58, 62, 64, 64, 68, 76, 78, 78, 86, 88, 90, 92, 98, 98}
		param0_5  []int  = []int{0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0}
		param0_6  []int  = []int{1, 9, 12, 12, 24, 25, 33, 33, 36, 39, 46, 48, 48, 52, 52, 53, 57, 69, 71, 72, 75, 76, 78, 80, 82, 86, 89, 91, 94, 95, 96, 97, 98, 99}
		param0_7  []int  = []int{62, -66, 60, -92, 46, 6, -52, 48, 72, -64, 34, 20, 50, 70, -34, 20, -70, 14, -44, 66, -70}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{33, 10, 6, 71, 18, 22, 15, 57, 56, 63, 35, 93, 31, 43, 98, 99, 62, 39, 44, 86, 78, 95, 6, 76, 71}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{12, 28, 38, 13, 23, 41, 30, 17, 30, 12}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
