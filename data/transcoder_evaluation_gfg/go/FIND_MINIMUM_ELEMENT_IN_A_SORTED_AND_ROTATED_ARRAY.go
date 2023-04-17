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


func f_gold(arr []int, low int, high int) int {
	if high < low {
		return arr[0]
	}
	if high == low {
		return arr[low]
	}
	var mid int = low + (high-low)/2
	if mid < high && arr[mid+1] < arr[mid] {
		return arr[mid+1]
	}
	if mid > low && arr[mid] < arr[mid-1] {
		return arr[mid]
	}
	if arr[high] > arr[mid] {
		return f_gold(arr, low, mid-1)
	}
	return f_gold(arr, mid+1, high)
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{16, 22, 50, 64, 68, 79, 84, 88, 89}
		param0_1  []int  = []int{88, -38, 46, 24, -52, -12, -90, 28, 18, 14, -72, 58, -98, 28, -84, 44, -42, -32, -22, -22, -82, -30, 90, 18, 62, 62, 92, 6, 60, 28, -90, 92, 82, 62, 98, -68, 48, -74, -8, 50, 62, 24, 30, -86, 98, -96, -98}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{26, 66, 94, 28, 38, 31, 92, 66, 81, 8, 36, 64, 80, 32, 48, 71, 72, 54, 61, 60, 89}
		param0_4  []int   = []int{-46, -26, -22, -14, 46, 62}
		param0_5  []int   = []int{0, 1, 1, 1}
		param0_6  []int   = []int{14, 81, 87}
		param0_7  []int   = []int{4}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{3, 41, 40, 53, 82, 9, 90, 43, 90, 59, 37, 21, 92, 98, 36, 99, 35, 67, 24, 29, 40, 31, 46, 12, 29, 8, 93, 67, 44, 83, 71, 29, 22, 32, 33, 11, 44, 97, 84, 44, 8, 10, 31, 50, 22, 8}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{4, 42, 28, 19, 4, 2, 1, 0, 15, 42}
		param2    []int  = []int{6, 31, 21, 17, 4, 2, 1, 0, 17, 31}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
