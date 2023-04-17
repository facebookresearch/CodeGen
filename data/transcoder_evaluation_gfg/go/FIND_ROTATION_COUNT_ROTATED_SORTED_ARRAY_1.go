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
		return 0
	}
	if high == low {
		return low
	}
	var mid int = low + (high-low)/2
	if mid < high && arr[mid+1] < arr[mid] {
		return mid + 1
	}
	if mid > low && arr[mid] < arr[mid-1] {
		return mid
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
		param0_0  []int   = []int{4, 16, 38, 39, 48, 74, 79}
		param0_1  []int  = []int{-46, 72, 72, -66, 96, 92, 40, 8, 94, -84, 6, -90, 38, -6, 48, -20, -86, -76, 88, -50, -44, -14, 54, -6, -2, 72, 8, -64, -46, 44, -88, 50, 86, 38, 42, -56}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{48, 74, 59, 57, 95, 11, 25, 61, 46, 54, 34, 84, 7, 97, 62, 57, 99, 93, 76, 5, 76, 93, 35, 84, 37, 60, 65, 16, 30, 73, 42, 61, 74, 77, 48, 62, 84, 93, 64, 57, 68, 46, 28, 77}
		param0_4  []int  = []int{-72, -68, -66, -66, -62, -62, -52, -48, -42, -42, -42, -38, -30, -22, -20, -20, -16, -16, -14, 0, 2, 2, 2, 4, 12, 20, 22, 26, 32, 34, 46, 46, 64, 64, 64, 66, 68, 68, 68, 74, 80, 84, 84, 88, 88, 90, 96, 98}
		param0_5  []int   = []int{1}
		param0_6  []int  = []int{7, 11, 20, 21, 22, 27, 30, 30, 34, 35, 36, 37, 38, 60, 61, 63, 63, 69, 70, 75, 80, 84, 88, 97}
		param0_7  []int   = []int{-2, 70, -40}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{71, 71, 27, 10, 97, 43, 55, 71, 6, 6, 77, 48, 77, 2, 83, 51, 61, 19, 2, 51, 26, 70, 20, 23, 54, 15, 6, 92, 35, 75, 8, 57, 50, 49, 88, 21, 36}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{6, 32, 16, 24, 29, 0, 23, 2, 30, 24}
		param2    []int  = []int{6, 21, 29, 26, 43, 0, 22, 1, 17, 22}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
