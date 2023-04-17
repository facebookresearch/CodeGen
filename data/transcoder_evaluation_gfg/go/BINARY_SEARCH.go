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


func f_gold(arr []int, l int, r int, x int) int {
	if r >= l {
		var mid int = l + (r-l)/2
		if arr[mid] == x {
			return mid
		}
		if arr[mid] > x {
			return f_gold(arr, l, mid-1, x)
		}
		return f_gold(arr, mid+1, r, x)
	}
	return -1
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{3, 4, 4, 8, 9, 13, 13, 15, 18, 27, 30, 32, 42, 48, 50, 52, 56, 66, 69, 69, 77, 84, 84, 93}
		param0_1  []int  = []int{52, -58, -22, -80, 44, -52, -34, 94, -34, -74, 42, 60, -62, 70, 98, 32, 10, 94, 26, 56, -48, -50, 42, 2, 46, 28, -68, -16, -96, -12, 66, -46, 74, -60, -52, 28, -92, -78, 32, 28, 16, 34, 30, -60, -14}
		param0_2  []int   = []int{0, 1}
		param0_3  []int   = []int{28, 84, 40, 81}
		param0_4  []int  = []int{-66, -62, -60, -56, -56, -2, 40, 44, 50, 74, 82, 94}
		param0_5  []int  = []int{1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1}
		param0_6  []int  = []int{15, 26, 31, 36, 36, 61, 68, 72, 75, 79, 82, 98}
		param0_7  []int  = []int{0, -82, -94, 48, 48, -96, 14, 66, 76, -30, 86, 28, -28, -66, -64, 92, -94, -66, 86, 26, 8, 94, -82, -80, 4, -26, 76, -46, 72, 88, -6, 8, -30, 40, -88, 2, -40, -98, -22, -20, 4, -12, 54, -20, -36, 12}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1}
		param0_9  []int   = []int{81, 47}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{19, 40, 1, 2, 8, 7, 6, 38, 12, 1}
		param2    []int  = []int{12, 35, 1, 2, 6, 7, 7, 33, 10, 1}
		param3    []int  = []int{22, 44, 1, 2, 8, 10, 8, 39, 6, 1}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i], param3[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i], param3[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
