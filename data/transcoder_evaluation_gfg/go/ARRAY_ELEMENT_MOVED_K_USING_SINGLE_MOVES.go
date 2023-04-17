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


func f_gold(a []int, n int, k int) int {
	if k >= n-1 {
		return n
	}
	var best int = 0
	var times int = 0
	for i := int(0); i < n; i++ {
		if a[i] > best {
			best = a[i]
			if i != 0 {
				times = 1
			}
		} else {
			times += 1
		}
		if times >= k {
			return best
		}
	}
	return best
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{2, 5, 5, 9, 10, 10, 11, 14, 23, 27, 31, 32, 33, 33, 33, 37, 39, 41, 41, 42, 42, 43, 47, 60, 61, 68, 73, 73, 73, 78, 80, 80, 82, 83, 86, 87, 89, 92, 94, 98}
		param0_1  []int  = []int{80, -58, 64, 48, -16, 60, -50, -52, 62, -86, -96, 52, 26, -30, 14}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1}
		param0_3  []int   = []int{90, 23, 43, 42, 7, 71, 79}
		param0_4  []int  = []int{-96, -96, -90, -84, -68, -64, -56, -56, -50, -50, -48, -46, -28, -18, 0, 0, 6, 32, 32, 34, 42, 42, 46, 50, 50, 52, 64, 64, 70, 76, 84, 88}
		param0_5  []int   = []int{1, 1, 1}
		param0_6  []int  = []int{2, 9, 15, 19, 26, 29, 42, 45, 46, 47, 55, 60, 60, 61, 62, 64, 68, 69, 74, 79, 96}
		param0_7  []int  = []int{-32, 12, 80, 42, 80, 8, 58, -76, -42, -98, 22, -90, -16, -4, -62, -32, 28, 12, 78, -52, -84, 78, 88, -76, -52, 68, -34, -16, -4, 2, -78, -94, -22, 34, 6, -62, 72}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int   = []int{52, 19}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{33, 14, 7, 4, 28, 1, 14, 26, 26, 1}
		param2    []int  = []int{37, 13, 6, 4, 21, 2, 17, 31, 14, 1}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
