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


func f_gold(ar []int, n int) int {
	var res int = 0
	sort.Ints(ar)
	for i := int(0); i < n; i++ {
		var count int = 1
		for ; i < n-1; i++ {
			if ar[i] == ar[i+1] {
				count++
			} else {
				break
			}
		}
		res = max(res, count)
	}
	return res
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{1, 2, 5, 8, 16, 21, 21, 22, 23, 26, 26, 27, 27, 29, 31, 33, 36, 37, 37, 38, 42, 45, 47, 50, 57, 58, 60, 60, 62, 63, 66, 66, 76, 84, 84, 88, 96, 99}
		param0_1  []int  = []int{-30, -60, 34, 4, 86, 80, -96, -94, 52, 46, 8, 82, -94, -96, 78, 82, -22, -36, 78, 50, -46, -36, 80, 24, -14, 94, -46, -38, 82, 4, -24, 2, 4, -82, -82, -18, -62, 12, 8, 92, 70, -10}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{38, 47, 84, 49, 48, 62, 48, 41, 38, 48, 92, 16, 99}
		param0_4  []int  = []int{-88, -64, -40, -38, -38, -16, 16, 20, 28, 40, 56, 58, 60, 68, 74, 92}
		param0_5  []int  = []int{1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1}
		param0_6  []int   = []int{14, 24, 82, 87, 95}
		param0_7  []int  = []int{-34, 62, 40, -84, 52, -76, 2, -58, 94, 22, 2, -18, -88, 62, -14, 46, 50, -58, -80, 68, -64, 90, -58, 12, 76, -40, 40, -46, 8, -80, 4, -90, 14, -10, 64, -68}
		param0_8  []int   = []int{0, 1, 1, 1}
		param0_9  []int  = []int{43, 41, 90, 5, 6, 17, 68, 68, 86, 89}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{25, 35, 34, 6, 12, 29, 3, 34, 3, 7}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
