package main

import (
		"fmt"
"sort"
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
	var sum int = 0
	sort.Ints(arr)
	for i := int(0); i < n/2; i++ {
		sum -= arr[i] * 2
		sum += arr[n-i-1] * 2
	}
	return sum
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{8, 9, 12, 13, 17, 21, 24, 29, 37, 37, 39, 40, 41, 45, 49, 50, 53, 54, 56, 59, 60, 60, 70, 71, 72, 74, 77, 77, 78, 85, 89, 89, 90, 90, 95, 98, 98}
		param0_1  []int  = []int{0, 48, -32, 28, -84, 14, 30, -80, 92, 76, -52, -20, 52, 78, 20, 32, 96, 66, 48, 26, 88, 6, 94, 32, -40, 44, -84, 54, -84, -80, -80, -64, -92, -84, -16, -18}
		param0_2  []int   = []int{0, 0, 0, 1, 1, 1}
		param0_3  []int   = []int{47, 7, 84, 96, 59, 53, 80}
		param0_4  []int  = []int{-88, -80, -68, -62, -60, -60, -48, -46, -44, -38, -16, -16, 0, 0, 2, 8, 20, 36, 40, 40, 44, 54, 60, 68, 70, 82, 82, 84, 92, 94, 96}
		param0_5  []int  = []int{1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1}
		param0_6  []int  = []int{2, 5, 10, 11, 13, 14, 15, 17, 17, 23, 23, 24, 27, 27, 28, 29, 30, 40, 42, 43, 46, 47, 51, 52, 57, 64, 65, 73, 74, 75, 76, 77, 81, 81, 82, 87, 89, 93, 95, 95, 99}
		param0_7  []int  = []int{-72, -84, 84, 2, -76, 48, 12, -72, -92, -72, 38, 26, -38, 26, 50, 2, 20, 26, -48, 30, 24, -12, -84, -54, 20, -16, -94, 26, -22, 86}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{57, 74, 53, 52, 80, 31, 27, 53, 8, 57, 46, 73, 46, 56, 73, 84, 37, 7, 97}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{34, 24, 3, 5, 29, 32, 35, 21, 37, 13}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
