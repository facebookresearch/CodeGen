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


func f_gold(arr []int, N int, K int) int {
	sort.Ints(arr)
	var res int = math.MaxInt64
	for i := int(0); i <= (N - K); i++ {
		var curSeqDiff int = arr[i+K-1] - arr[i]
		res = min(res, curSeqDiff)
	}
	return res
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{1, 1, 4, 18, 21, 35, 37, 39, 76, 81, 86, 92, 96}
		param0_1  []int  = []int{-8, -6, 62, 52, -86, 2, -94, 0, -48, -38, 24, -48, 34}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{23, 36, 43, 50, 74, 81, 94, 13, 30, 57, 30, 71, 10, 99, 66, 94, 83, 39, 37, 3, 89, 34}
		param0_4  []int  = []int{-96, -94, -92, -84, -80, -72, -24, -22, -18, -14, 6, 8, 26, 28, 30, 36, 50, 58, 80, 84, 92, 92}
		param0_5  []int  = []int{0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1}
		param0_6  []int  = []int{6, 7, 9, 27, 30, 42, 54, 55, 57, 57, 59, 76, 84, 84, 84}
		param0_7  []int  = []int{88, 44, -96, -72, -80, 0, -64, -64, -68, 4, 38, 4, -38, 68, -54, 92, -16, 62, 24, 54, 0, 54, 62, -70, 80, -12, 84, -16, -10, 88, -30, -56, 48, 50, -24, 94, 40, 28, -86, -12}
		param0_8  []int   = []int{0, 1}
		param0_9  []int  = []int{89, 18, 7, 54, 67, 93, 10, 61, 59, 59, 69, 63, 98, 8, 78, 55, 6, 1, 56, 97, 75, 88, 10}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{7, 9, 16, 17, 21, 21, 13, 31, 1, 22}
		param2    []int  = []int{6, 12, 26, 20, 12, 22, 14, 26, 1, 14}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
