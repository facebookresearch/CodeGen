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


func f_gold(arr []int, n int) int {
	sort.Ints(arr)
	var minXor int = math.MaxInt64
	var val int = 0
	for i := int(0); i < n-1; i++ {
		val = arr[i] ^ arr[i+1]
		minXor = min(minXor, val)
	}
	return minXor
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{8, 11, 12, 27, 32, 32, 36, 56, 57, 66, 68, 70, 74, 78, 82, 83, 96}
		param0_1  []int   = []int{40, 48, 66, 4, -60, 42, -8, 38}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{98, 6, 82, 95, 87, 20, 11, 63, 78, 70, 37, 12, 57, 67, 10, 49, 38, 28, 86, 7, 61, 50, 32, 68, 91, 66, 57, 29, 2, 64, 65, 15, 16, 4, 7, 76, 44, 52, 81, 89, 3, 36, 57, 95, 48, 24}
		param0_4  []int  = []int{-88, -84, -76, -58, -40, -38, -28, -24, -20, -14, -12, 16, 20, 28, 28, 30, 40, 44, 56, 58, 60, 92, 92}
		param0_5  []int  = []int{0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0}
		param0_6  []int  = []int{6, 6, 19, 31, 41, 45, 49, 56, 78, 96, 98}
		param0_7  []int   = []int{62, -90, 22, -84, -4}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{83, 13, 43, 99, 34, 74, 56, 20, 93, 65, 92, 58, 91, 72, 37, 10, 39, 7, 29, 69, 42, 28}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{10, 7, 19, 36, 13, 20, 6, 3, 21, 14}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
