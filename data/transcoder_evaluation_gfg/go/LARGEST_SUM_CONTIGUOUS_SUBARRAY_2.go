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


func f_gold(a []int, size int) int {
	var (
		max_so_far int = a[0]
		curr_max   int = a[0]
	)
	for i := int(1); i < size; i++ {
		curr_max = max(a[i], curr_max+a[i])
		max_so_far = max(max_so_far, curr_max)
	}
	return max_so_far
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{1, 3, 4, 7, 8, 8, 10, 12, 16, 19, 19, 20, 20, 21, 21, 22, 26, 27, 29, 34, 36, 38, 38, 39, 41, 43, 44, 47, 47, 49, 57, 57, 60, 62, 63, 65, 75, 77, 77, 78, 81, 82, 82, 83, 83, 84, 85, 98, 99}
		param0_1  []int  = []int{-40, 14, 2, -70, 86, -90, -50, -54, -2, 90, 30}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{60, 69, 41, 7, 77, 36, 36, 26, 35, 30, 64, 75, 3, 35, 60, 71, 29, 47, 15, 29, 43, 88, 56, 22, 9, 45, 40, 50, 52}
		param0_4  []int  = []int{-96, -88, -80, -72, -64, -64, -60, -60, -60, -58, -56, -54, -54, -50, -50, -26, -26, -24, -20, -8, -2, 0, 4, 4, 12, 14, 18, 18, 24, 32, 42, 44, 44, 44, 48, 50, 50, 56, 60, 60, 70, 80, 88, 88, 90, 98}
		param0_5  []int  = []int{0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0}
		param0_6  []int  = []int{2, 4, 4, 5, 6, 7, 11, 12, 14, 18, 23, 24, 27, 28, 33, 36, 37, 38, 39, 40, 41, 41, 48, 48, 52, 61, 64, 66, 66, 77, 79, 82, 85, 88, 91, 94, 99}
		param0_7  []int  = []int{-56, 0, 16, 12, 20, 36, 32, -52, -68, -36, -96, -46, -34, 56, 2, 78, 6, 30, -68, -48, 2, 44, -26, -36, -30, -20, -90, -66, 4, 94, 8, 4, -4, -32, -24}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{39, 87, 27, 89, 26, 25, 80, 82, 21, 25, 55, 27, 20, 81, 47, 79, 26, 72, 10, 11, 90, 89}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{38, 10, 18, 25, 35, 22, 34, 20, 22, 21}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
