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
	var (
		sum     int = 0
		leftsum int = 0
	)
	for i := int(0); i < n; i++ {
		sum += arr[i]
	}
	for i := int(0); i < n; i++ {
		sum -= arr[i]
		if leftsum == sum {
			return i
		}
		leftsum += arr[i]
	}
	return -1
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{24, 31, 44, 52, 78, 95}
		param0_1  []int  = []int{-78, -38, 22, 58, 68, -60, -30, 6, 58, 20, -64, -40, -14, 80, -2, -88, -68, -16, -4, 78, -38, -74, 78, -72, 46, -12, 82, -76, -98, -28, -32, 88, 72, 72, 64, -10, 98, -24, -96}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1}
		param0_3  []int  = []int{98, 69, 41, 48, 40, 90, 76, 61, 17, 81, 74, 92, 54, 16, 11, 15, 8, 16, 84, 86, 34, 34, 75, 92, 67, 54, 93, 19, 31, 62, 89, 26, 96, 91, 32, 78, 42, 84, 66, 79, 29, 48, 49, 5}
		param0_4  []int   = []int{-28, 42}
		param0_5  []int  = []int{1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1}
		param0_6  []int  = []int{18, 21, 23, 24, 36, 37, 39, 49, 55, 68, 80, 81, 88, 90}
		param0_7  []int  = []int{94, 22, 42, -42, 78, 50, 96, 98, 46, 74, 98, 84, -2, -76, 48, 18, 28, -62, 78, 6, -76, -12, 46, 62, 14, 76, 44, -26, -92, 12, 62, -72, -42}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{1, 23, 18, 91, 65, 2, 73, 12, 91, 47, 14, 48, 1, 69, 95, 81, 59, 36, 79, 35, 9, 52, 55, 73, 54, 25, 8, 41, 64, 96}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{4, 19, 11, 27, 1, 25, 11, 32, 14, 19}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
