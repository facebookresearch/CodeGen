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


func f_gold(arr []int, n int, key int, capacity int) int {
	if n >= capacity {
		return n
	}
	var i int
	for i = n - 1; i >= 0 && arr[i] > key; i-- {
		arr[i+1] = arr[i]
	}
	arr[i+1] = key
	return n + 1
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{69}
		param0_1  []int  = []int{-34, -38, -72, 90, -84, -40, -40, -52, -12, 80, -4, -58}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{96, 34, 11, 1, 36, 79, 64, 75, 75, 96, 32, 18, 25, 79, 63, 80, 90, 75, 44, 71, 48, 1, 62, 53, 17, 98}
		param0_4  []int  = []int{-98, -92, -92, -84, -82, -80, -80, -74, -70, -60, -48, -42, -36, -34, -34, -34, -30, -28, -16, -6, -2, -2, 2, 12, 14, 20, 24, 40, 46, 50, 60, 66, 70, 72, 78, 82, 88, 92, 94, 94, 96}
		param0_5  []int  = []int{1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0}
		param0_6  []int  = []int{10, 12, 12, 19, 20, 21, 24, 27, 37, 47, 50, 54, 55, 58, 61, 63, 63, 68, 73, 75, 87, 90, 90, 92, 92}
		param0_7  []int  = []int{-74, 62, 74, 92, -38, -28, -26, 4, 88, -68, -76, -20, -4, 12, 72, 6, 42, 36, 88, -96, -80, 90, 80, -26, -36, -72, -62, 38, -20, 40, -10, -22, -20, 38, 82, -84, 8, -60, 86, -26, 44, -72, -70, -16, -22, 18, -16, 76, -50}
		param0_8  []int   = []int{1, 1, 1, 1, 1}
		param0_9  []int  = []int{64, 80, 47, 58, 41, 3, 85, 96, 51, 4, 22, 89, 67, 54, 88, 15, 83, 31, 19, 28, 40, 67, 37, 13, 63, 38, 27, 14, 7, 68}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{0, 6, 13, 21, 30, 12, 12, 37, 3, 23}
		param2    []int  = []int{0, 6, 19, 20, 32, 9, 13, 26, 4, 24}
		param3    []int  = []int{0, 9, 11, 13, 28, 10, 21, 42, 2, 25}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i], param3[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i], param3[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
