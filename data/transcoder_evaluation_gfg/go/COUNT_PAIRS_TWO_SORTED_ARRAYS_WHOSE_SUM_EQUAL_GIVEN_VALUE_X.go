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


func f_gold(arr1 []int, arr2 []int, m int, n int, x int) int {
	var count int = 0
	for i := int(0); i < m; i++ {
		for j := int(0); j < n; j++ {
			if (arr1[i] + arr2[j]) == x {
				count++
			}
		}
	}
	return count
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{11, 13, 16, 23, 26, 28, 31, 34, 37, 39, 44, 48, 56, 59, 79, 91, 96, 98}
		param0_1  []int  = []int{50, 14, -98, 14, 90, 36, 66, 44, 10, -98, -24, -36, -32, -50}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{88, 14, 29, 87, 86, 58}
		param0_4  []int  = []int{-98, -92, -88, -86, -82, -76, -72, -66, -56, -48, -34, -28, -28, -26, -20, -18, -18, -16, -16, -12, -4, 0, 6, 12, 16, 20, 22, 30, 34, 34, 36, 56, 58, 62, 64, 80, 82, 94}
		param0_5  []int  = []int{1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0}
		param0_6  []int   = []int{70, 70, 74}
		param0_7  []int   = []int{-20, -12, -50, 76, 24, 64, -22, -4, -68}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{68, 75, 51, 45, 73, 95, 48, 53, 70, 41, 65, 47, 46, 43, 79, 29, 50}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1_0  []int  = []int{1, 1, 9, 14, 17, 23, 26, 31, 33, 36, 53, 60, 71, 75, 76, 84, 87, 88}
		param1_1  []int  = []int{34, -6, -66, 0, -6, 82, 60, -98, -8, 60, -2, 4, 22, 76}
		param1_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param1_3  []int   = []int{91, 95, 64, 4, 63, 35}
		param1_4  []int  = []int{-94, -90, -88, -84, -82, -78, -76, -72, -70, -58, -58, -46, -42, -40, -40, -32, -22, -20, -18, -12, -8, -6, 6, 6, 18, 20, 34, 46, 60, 62, 66, 72, 72, 76, 76, 78, 92, 98}
		param1_5  []int  = []int{1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0}
		param1_6  []int   = []int{15, 55, 84}
		param1_7  []int   = []int{18, 98, -88, 86, 72, -44, 82, 94, 58}
		param1_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param1_9  []int  = []int{4, 6, 76, 65, 16, 13, 85, 43, 31, 14, 81, 90, 24, 87, 40, 25, 88}
		param1    [][]int = [][]int{param1_0, param1_1, param1_2, param1_3, param1_4, param1_5, param1_6, param1_7, param1_8, param1_9}
		param2    []int  = []int{9, 11, 14, 3, 34, 39, 1, 5, 27, 10}
		param3    []int  = []int{15, 12, 9, 5, 32, 26, 1, 4, 26, 10}
		param4    []int  = []int{11, 8, 12, 5, 23, 34, 1, 7, 37, 9}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), ([]int)(param1[i]), param2[i], param3[i], param4[i]) == f_gold(([]int)(param0[i]), ([]int)(param1[i]), param2[i], param3[i], param4[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
