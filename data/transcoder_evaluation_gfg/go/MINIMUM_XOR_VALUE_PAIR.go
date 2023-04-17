package main

import (
		"fmt"
	"math"
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
	var min_xor int = math.MaxInt64
	for i := int(0); i < n; i++ {
		for j := int(i + 1); j < n; j++ {
			min_xor = min(min_xor, arr[i]^arr[j])
		}
	}
	return min_xor
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{4, 5, 7, 10, 10, 11, 14, 19, 21, 24, 27, 27, 27, 28, 28, 28, 33, 34, 41, 42, 43, 48, 52, 53, 53, 59, 62, 64, 66, 71, 77, 78, 78, 79, 80, 82, 90, 97, 99, 99}
		param0_1  []int  = []int{-68, -58, 52, 88, 90, 66, -66, -84, -70, -64, 56, 42, 94, -10, 0, 80, 8, 28, -94, 36, 90, 56, 56, 80, -94, 50, 90, -28, -22, -2, -96, 74, -16, -14}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{57, 63, 11, 73, 60, 73, 25, 65, 39, 48, 31, 17, 23, 94, 10, 97, 42, 45, 83, 75, 97, 96}
		param0_4  []int  = []int{-92, -92, -90, -88, -84, -82, -66, -64, -64, -62, -44, -42, -40, -28, -22, -12, -4, -2, 0, 4, 16, 22, 28, 34, 54, 60, 72, 74, 78, 86, 94}
		param0_5  []int  = []int{1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0}
		param0_6  []int  = []int{2, 2, 6, 13, 16, 16, 17, 19, 19, 20, 22, 25, 27, 29, 34, 34, 34, 36, 38, 39, 42, 49, 49, 53, 59, 59, 71, 77, 79, 82, 83, 83, 84, 84, 86, 86, 87, 88, 93, 96}
		param0_7  []int  = []int{-14, 20, 36, 12, -54, -50, 92, -28, 44, -46, 6, 96, 82, 70, -20, 24, -96, -14, 46, -28, -46, -28, 22, -82, 36, -94, -48, -92, 96, 74, 14}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{50, 48, 94, 64, 60, 48, 79, 75, 77, 62, 33, 42, 22, 78, 32, 99, 27, 23, 76, 51, 34, 54, 70, 12, 19, 17, 13, 82, 96, 70, 4, 12, 5, 11, 23, 23, 18, 93, 38, 69}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{34, 17, 9, 21, 18, 36, 36, 20, 39, 30}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
