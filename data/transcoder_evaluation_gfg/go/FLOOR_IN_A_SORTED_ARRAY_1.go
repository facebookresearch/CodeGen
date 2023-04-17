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
	if low > high {
		return -1
	}
	if x >= arr[high] {
		return high
	}
	var mid int = (low + high) / 2
	if arr[mid] == x {
		return mid
	}
	if mid > 0 && arr[mid-1] <= x && x < arr[mid] {
		return mid - 1
	}
	if x < arr[mid] {
		return f_gold(arr, low, mid-1, x)
	}
	return f_gold(arr, mid+1, high, x)
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{5, 11, 20, 42, 42, 55, 58, 98, 99}
		param0_1  []int  = []int{50, -90, -38, -46, -10, -22, -66, 72, -52, 38, 90, 34, -12, -44, -6, 0, -20, -38, 86, 26, 64, -24, 40, 90, -26, -2, -28, 12, 22, -14}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{69, 28, 68, 98, 24, 67, 86, 2, 18, 22, 44, 77, 52, 62, 24, 46}
		param0_4  []int  = []int{-96, -94, -88, -84, -68, -60, -52, -52, -42, -34, -32, -16, -12, -6, -6, -4, -2, 0, 16, 18, 38, 58, 70, 72, 76, 78, 90, 92, 98}
		param0_5  []int  = []int{0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0}
		param0_6  []int  = []int{1, 6, 7, 9, 10, 11, 19, 19, 22, 22, 26, 34, 36, 37, 37, 38, 39, 40, 49, 54, 60, 62, 65, 67, 71, 76, 78, 79, 82, 82, 89, 95, 97}
		param0_7  []int  = []int{76, -32, -98, -18, -80, 74, -22, -82, 40, -64, 58, -18, -64, 34, -44, -82, -46, 62, -80, -76, 32, 44, -32, 98, -26, 62, 16, 86, -52, -72, -90, -30, 6}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{81, 69, 15, 52, 49, 54, 18, 92, 33, 21, 91, 21, 5, 25, 77, 92, 26, 58, 72, 55, 76, 18, 13, 59, 9, 12, 31, 24, 36, 33, 71, 87, 55, 19, 42, 25}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{5, 26, 11, 15, 22, 24, 22, 28, 28, 35}
		param2    []int  = []int{7, 28, 9, 11, 27, 15, 26, 31, 29, 19}
		param3    []int  = []int{6, 23, 18, 13, 20, 26, 25, 24, 30, 33}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i], param3[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i], param3[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
