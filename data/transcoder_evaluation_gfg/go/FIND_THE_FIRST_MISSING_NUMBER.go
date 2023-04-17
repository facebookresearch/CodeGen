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


func f_gold(array []int, start int, end int) int {
	if start > end {
		return end + 1
	}
	if start != array[start] {
		return start
	}
	var mid int = (start + end) / 2
	if array[mid] == mid {
		return f_gold(array, mid+1, end)
	}
	return f_gold(array, start, mid)
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{3, 6, 7, 9, 11, 14, 18, 30, 30, 32, 32, 34, 37, 44, 45, 45, 48, 48, 48, 52, 58, 60, 63, 67, 69, 69, 81, 83, 87, 89, 97, 99}
		param0_1  []int  = []int{88, -62, 16, 80, 66, 78, 88, 38, 52, -96, 48, 98, 96, -62, 18, 34, -58, 30, -10, 26, -98, 48, -96, 4, 92, 36, 36, -36, -32, -70, 62, -58, -58, -84, 86, -98}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{79, 99, 79, 85, 61, 58, 62, 61, 39, 87, 39, 74, 36, 70, 30, 43, 20, 52, 54, 50, 81, 98, 42}
		param0_4  []int  = []int{-98, -72, -46, -44, -42, -40, -16, -4, 62, 70, 74}
		param0_5  []int  = []int{1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0}
		param0_6  []int   = []int{58}
		param0_7  []int  = []int{4, -84, -42, 12, -50, 42, -36, -38, -36, 98, -2, 20, 6, -96, -78, 24, 34, 88, 0, 74, 0, -8, -86, -68, -42, 98, -26, 86, -70, -32, -82, 78, 46, 58, 84, 4, -60, -90, -52, -78}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int   = []int{8}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{24, 19, 26, 20, 8, 26, 0, 37, 28, 0}
		param2    []int  = []int{18, 26, 28, 20, 10, 23, 0, 31, 28, 0}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
