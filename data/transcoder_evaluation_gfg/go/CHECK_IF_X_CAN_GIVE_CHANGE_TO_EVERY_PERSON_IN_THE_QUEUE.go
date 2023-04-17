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


func f_gold(notes []int, n int) int {
	var (
		fiveCount int = 0
		tenCount  int = 0
	)
	for i := int(0); i < n; i++ {
		if notes[i] == 5 {
			fiveCount++
		} else if notes[i] == 10 {
			if fiveCount > 0 {
				fiveCount--
				tenCount++
			} else {
				return 0
			}
		} else {
			if fiveCount > 0 && tenCount > 0 {
				fiveCount--
				tenCount--
			} else if fiveCount >= 3 {
				fiveCount -= 3
			} else {
				return 0
			}
		}
	}
	return 1
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{20}
		param0_1  []int   = []int{5, 5, 5, 20, 10}
		param0_2  []int  = []int{5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10}
		param0_3  []int  = []int{10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 18}
		param0_4  []int   = []int{5, 5, 20}
		param0_5  []int  = []int{10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5}
		param0_6  []int  = []int{5, 10, 20, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5}
		param0_7  []int  = []int{-82, -10, -78, -84, 68, 62, 10, 20, -86, -98, 92, 70, 40, -12, -20, -36, 8, -70, 6, 8, 44, -24, 8, -18, 76, -54, -14, -94, -68, -62, -24, -36, -74, 92, 92, -80, 48, 56, 94}
		param0_8  []int  = []int{10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5}
		param0_9  []int  = []int{46, 46, 93, 57, 82, 34, 83, 80, 77, 36, 80, 85, 69, 28, 9, 56, 49, 27, 83, 25, 1, 80, 99, 14, 69, 82, 79, 71, 74, 34}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{4, 5, 27, 12, 2, 17, 7, 31, 25, 20}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
