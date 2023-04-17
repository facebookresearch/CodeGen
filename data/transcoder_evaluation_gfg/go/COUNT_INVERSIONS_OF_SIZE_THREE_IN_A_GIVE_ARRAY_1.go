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
	for i := int(1); i < n-1; i++ {
		var small int = 0
		for j := int(i + 1); j < n; j++ {
			if arr[i] > arr[j] {
				small++
			}
		}
		var great int = 0
		for j := int(i - 1); j >= 0; j-- {
			if arr[i] < arr[j] {
				great++
			}
		}
		invcount += great * small
	}
	return invcount
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{4, 75, 89}
		param0_1  []int  = []int{84, -66, -52, 34, -28, -6, 20, 22, -78, -26, 14, 24, -92, -18, 32, -94, -64, -38, 56, 4, -10, 58, -66, -58, -10, -8, -62, -60, -26}
		param0_2  []int   = []int{0, 0, 0, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{18, 7, 43, 57, 94, 37, 38, 41, 59, 64, 97, 29, 51, 37, 64, 91, 42, 83, 13, 22, 68}
		param0_4  []int  = []int{-94, -86, -84, -84, -82, -66, -62, -58, -52, -48, -44, -40, -38, -32, -22, -22, -22, -14, -8, -6, -6, 0, 2, 20, 20, 26, 32, 32, 52, 56, 66, 74, 76, 80, 80, 86, 88, 94}
		param0_5  []int  = []int{0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0}
		param0_6  []int  = []int{4, 8, 15, 19, 24, 31, 33, 36, 38, 45, 45, 52, 54, 65, 73, 75, 83, 84, 90, 92, 93}
		param0_7  []int  = []int{80, -30, -44, 76, -96, 2, 22, -30, 36, -6, 88, -60, -90, -52, 78, 90, -52}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{74, 71, 28, 45, 14, 31, 17, 10, 82, 27, 45, 73, 93, 87, 57, 58}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{1, 26, 7, 17, 34, 9, 19, 10, 7, 10}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
