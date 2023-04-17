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
	var result int = -1
	for i := int(0); i < n; i++ {
		for j := int(0); j < n-1; j++ {
			for k := int(j + 1); k < n; k++ {
				if arr[j]*arr[k] == arr[i] {
					result = max(result, arr[i])
				}
			}
		}
	}
	return result
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{4, 78, 84}
		param0_1  []int  = []int{-54, 64, 60, 14, 18, -68, -54, -58, 38, -72, -84, 46, 74, 76, 28, -2, 54, 24, 18, -74, -78, 14, -38, -70, 26, -54, -36, -96, -12, 8, 62, -42, -84, 10, -6, 36, -72, 10, 10, -20, 16, 92, -64, -34, 74, -98, 18}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{39, 49, 94, 80, 48, 34, 63, 82, 47, 51, 60, 68, 79, 23, 97, 22, 54, 53, 40, 2, 25}
		param0_4  []int   = []int{-90, -52, -10, 12, 72}
		param0_5  []int   = []int{1, 0, 0}
		param0_6  []int  = []int{2, 9, 11, 14, 16, 17, 17, 18, 19, 21, 24, 25, 28, 29, 30, 33, 33, 39, 41, 41, 43, 46, 50, 51, 60, 62, 67, 80, 84, 86, 91, 92, 97}
		param0_7  []int   = []int{4}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{52, 8, 31, 92, 20, 18, 34, 5, 15, 8, 73, 20, 40, 61, 80, 51, 95, 73, 38, 30, 21, 69, 52, 38, 68, 77}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{2, 26, 22, 10, 3, 2, 27, 0, 16, 22}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
