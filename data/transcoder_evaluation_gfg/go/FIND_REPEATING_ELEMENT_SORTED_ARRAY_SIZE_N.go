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
	if low > high {
		return -1
	}
	var mid int = (low + high) / 2
	if arr[mid] != mid+1 {
		if mid > 0 && arr[mid] == arr[mid-1] {
			return mid
		}
		return f_gold(arr, low, mid-1)
	}
	return f_gold(arr, mid+1, high)
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{15, 21, 32, 42, 42, 44, 57, 68, 75, 80, 83, 84}
		param0_1  []int  = []int{-60, -90, -88, -80, -86, 18, 54, 56, 84, 42, -60, -90, 52, -44, -62, -56, -16, 28, 22, -24, -36, -56, 80, 68, -16}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{87, 43, 74}
		param0_4  []int  = []int{-82, -66, -66, -62, -56, -52, -44, -42, -28, -22, -12, -6, -4, -2, 18, 26, 26, 28, 42, 42, 56, 58, 78, 90, 92, 94, 96, 96}
		param0_5  []int  = []int{0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1}
		param0_6  []int  = []int{6, 9, 14, 17, 22, 31, 32, 33, 36, 39, 42, 43, 46, 46, 46, 47, 49, 53, 60, 61, 67, 68, 72, 75, 77, 77, 84, 84, 85, 89, 94, 94, 95}
		param0_7  []int  = []int{-88, 82, -10, -10, 68, -86, 70, 92, -54, -10, -56}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{35, 66, 47, 42, 95, 10, 84, 80, 23, 35, 21, 71, 39, 9, 38, 40, 22, 65}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{6, 23, 33, 2, 20, 19, 23, 7, 8, 14}
		param2    []int  = []int{11, 12, 32, 2, 21, 19, 19, 10, 8, 16}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
