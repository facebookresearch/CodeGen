package main

import (
		"fmt"
"sort"
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


func f_gold(arr []int, n int, m int) int {
	if m == 0 || n == 0 {
		return 0
	}
	sort.Ints(arr)
	if n < m {
		return -1
	}
	var min_diff int = math.MaxInt64
	var first int = 0
	var last int = 0
	for i := int(0); i+m-1 < n; i++ {
		var diff int = arr[i+m-1] - arr[i]
		if diff < min_diff {
			min_diff = diff
			first = i
			last = i + m - 1
		}
	}
	return arr[last] - arr[first]
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{2, 5, 11, 23, 33, 35, 39, 51, 52, 56, 74, 76, 76, 79, 85, 88, 93, 98}
		param0_1  []int  = []int{-42, 76, -34, -74, 16, 4, 88, -70, -88, -94, -24, 4, -14, -56, 56, -18, 84, 0, -48, -94, 72, 42, 36, 52, 74, -84, -50, 16, 30}
		param0_2  []int   = []int{0, 0, 1, 1, 1, 1}
		param0_3  []int  = []int{29, 49, 88, 44, 92, 43, 12, 5, 38, 75, 57, 3, 85, 16, 86, 62, 16, 40, 76, 37, 5, 69, 16, 63, 84, 78, 74, 18, 4, 89, 73, 67, 60}
		param0_4  []int  = []int{-98, -80, -50, -44, -42, -36, -36, -28, -10, -8, -4, -2, 2, 10, 18, 18, 26, 32, 36, 56, 80, 86, 88, 90}
		param0_5  []int  = []int{0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1}
		param0_6  []int   = []int{13, 15, 62, 65, 87}
		param0_7  []int  = []int{-50, 58, 78, 28, 4, 18, -8, 18, -88, -48, -26, -32, 64, 48, 60, 94, -92, 48, -36, 30, -80, -60, 82, -62, 32, -36, -76, -88, -60, 22, -14, 72, 30}
		param0_8  []int  = []int{0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int   = []int{25, 17, 58, 40, 53, 73, 23, 77, 38}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{16, 15, 5, 25, 16, 13, 3, 31, 9, 8}
		param2    []int  = []int{13, 28, 5, 18, 12, 14, 4, 17, 6, 6}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
