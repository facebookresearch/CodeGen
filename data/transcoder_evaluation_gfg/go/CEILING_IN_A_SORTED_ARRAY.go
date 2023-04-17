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


func f_gold(arr []int, low int, high int, x int) int {
	var i int
	if x <= arr[low] {
		return low
	}
	for i = low; i < high; i++ {
		if arr[i] == x {
			return i
		}
		if arr[i] < x && arr[i+1] >= x {
			return i + 1
		}
	}
	return -1
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{2, 3, 4, 6, 8, 9, 9, 10, 11, 16, 19, 20, 21, 21, 21, 24, 24, 25, 28, 30, 30, 30, 32, 34, 35, 39, 41, 42, 49, 52, 57, 59, 61, 62, 66, 68, 71, 73, 76, 79, 83, 84, 85, 86, 87, 87}
		param0_1  []int  = []int{92, 50, -84, 60, 32, -54, 84, -82, -42, -72, -64, -28, -48, 66, 92, -42, 42, -66, 52, -30, 48, 42, 36, -4, 64, 62, -16, 0, 20, 26, 78, 78, 12, -6, -30, -14, 76, 72, 70, -34, 98, 32}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{26, 68, 73, 76, 14, 19, 56, 80, 17, 7, 15, 64, 99, 98, 21, 21, 72, 12, 14, 10, 44, 82, 25, 42, 46, 86, 79, 43, 91}
		param0_4  []int  = []int{-90, -86, -84, -50, -30, -24, -12, -2, 8, 22, 30, 44, 58, 58, 60, 60, 62, 90}
		param0_5  []int  = []int{0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1}
		param0_6  []int  = []int{2, 2, 29, 31, 34, 39, 48, 50, 56, 61, 66, 66, 69, 73, 88}
		param0_7  []int  = []int{-98, 48, -58, 8, 70, 62, 92, 84, -58, -46, -26, -92, 18, -88, 40, -12, 60, 14, 54, -64, 88, 52, -44, 88, -46, -8, 36, -22, 28, -20, -50, 58, -82, -44, -44, 54, -86, 40, 10, 0, -24, -84, -10, 62, 58, 0, -88}
		param0_8  []int   = []int{0, 0, 0, 0, 1, 1}
		param0_9  []int  = []int{56, 30, 33, 5, 67, 35, 22, 54, 36, 55, 94, 89, 40, 65, 29, 76, 17, 14, 14, 49, 40, 44, 35, 69, 63, 2, 81, 78, 19, 67, 12, 14, 68, 30, 82, 85, 12, 2, 94, 33, 85, 75, 97, 31, 69, 31, 85, 26}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{23, 36, 11, 23, 9, 12, 9, 40, 5, 46}
		param2    []int  = []int{37, 35, 9, 27, 16, 15, 12, 29, 5, 47}
		param3    []int  = []int{44, 34, 13, 26, 10, 18, 10, 24, 5, 47}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i], param3[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i], param3[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
