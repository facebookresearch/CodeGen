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
	sort.Ints(arr)
	var count int = 0
	var max_count int = 0
	var min_count int = n
	for i := int(0); i < (n - 1); i++ {
		if arr[i] == arr[i+1] {
			count += 1
			continue
		} else {
			max_count = max(max_count, count)
			min_count = min(min_count, count)
			count = 0
		}
	}
	return max_count - min_count
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{5, 15, 19, 22, 28, 29, 39, 46, 46, 49, 51, 55, 62, 69, 72, 72, 72, 74, 79, 92, 92, 93, 95, 96}
		param0_1  []int  = []int{-26, -54, 92, 76, -92, -14, -24, -70, -78, -50, -48, -22, 12, 2, -34, -60, 4, -32, -10, 52, -92, -74, 18, 34, 6, -66, 42, -10, -6, 56, 92}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{59, 35, 13, 79, 61, 97, 92, 48, 98, 38, 65, 54, 31, 49, 81, 22, 96, 29, 65, 48, 92, 66, 25, 21, 26, 1, 32, 73, 46, 5, 40, 17, 53, 93, 83, 29}
		param0_4  []int   = []int{-70, -34, -32, -30, -14, 80, 86, 90}
		param0_5  []int  = []int{0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0}
		param0_6  []int   = []int{9}
		param0_7  []int   = []int{94, 10, 70, 42}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{64, 76, 49, 55, 92, 15, 4, 8, 95, 60, 90, 3, 7, 79, 84, 17, 96, 10, 80, 26, 22, 15}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{15, 30, 24, 29, 4, 23, 0, 2, 24, 20}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
