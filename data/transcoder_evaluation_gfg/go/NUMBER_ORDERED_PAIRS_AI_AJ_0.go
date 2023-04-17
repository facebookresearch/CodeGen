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


func f_gold(a []int, n int) int {
	var count int = 0
	for i := int(0); i < n; i++ {
		for j := int(i + 1); j < n; j++ {
			if (a[i] & a[j]) == 0 {
				count += 2
			}
		}
	}
	return count
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{17, 20, 32, 35, 35, 36, 43, 47, 59, 59, 68, 69, 70, 70, 75, 82, 88, 94, 96, 99}
		param0_1  []int  = []int{-78, -40, 58, -36, 34, -12, -38, 48, -66, 16, 50, -26, -22, 46, -70, -68, -44, -52, -78, -50}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{49, 57, 17, 37, 56, 61, 10, 3, 33, 33, 70, 35, 50, 85, 48, 65, 83, 21, 96, 19, 66, 43, 69, 17, 60, 87, 82, 3, 83, 44, 63, 19, 55, 58, 77, 76, 50, 96}
		param0_4  []int  = []int{-94, -88, -86, -80, -80, -72, -64, -60, -58, -58, -58, -50, -44, -32, -8, -8, 0, 6, 8, 10, 14, 14, 18, 28, 34, 34, 46, 54, 56, 56, 56, 64, 66, 66, 70, 82, 84, 88, 96}
		param0_5  []int  = []int{1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0}
		param0_6  []int  = []int{1, 3, 10, 11, 13, 14, 15, 17, 20, 25, 26, 26, 27, 29, 32, 36, 36, 36, 42, 46, 47, 49, 51, 54, 54, 55, 60, 66, 67, 68, 68, 68, 72, 77, 78, 79, 83, 84, 92, 98}
		param0_7  []int  = []int{-76, -72, 16, 38, -60, 44, -2, -76, -76, -56, 40, 36, 50, -50, -32, 48, -96, 80, 84, 60, 84, 38, -54, -42, 48, 30, 66, -62, -52, -94, 64, -16, 54, 98}
		param0_8  []int   = []int{0, 0, 1, 1, 1, 1}
		param0_9  []int  = []int{63, 82, 22, 84, 11, 62, 18, 43, 57, 25, 4, 27, 62, 46, 55, 16, 1, 9, 10, 73, 36, 80, 95, 87, 47, 64, 27, 25, 70}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{17, 11, 23, 37, 33, 13, 32, 28, 5, 22}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
