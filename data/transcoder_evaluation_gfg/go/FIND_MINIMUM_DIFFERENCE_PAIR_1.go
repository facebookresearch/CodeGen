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
	var diff int = math.MaxInt64
	for i := int(0); i < n-1; i++ {
		if arr[i+1]-arr[i] < diff {
			diff = arr[i+1] - arr[i]
		}
	}
	return diff
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{3, 25, 44, 46, 54, 60, 81}
		param0_1  []int  = []int{82, 68, -98, -66, -36, -42, 98, -38, 58, -6, -28, 70, -24, 18, 16, 10, 92, 44, 28, -96, -72, 24, 28, -80, -4, 38, 88, 76}
		param0_2  []int   = []int{1, 1, 1}
		param0_3  []int  = []int{87, 25, 80, 45, 44, 20, 48, 47, 51, 54, 68, 47, 89, 95, 15, 29, 5, 45, 2, 64, 53, 96, 94, 22, 23, 43, 61, 75, 74, 50}
		param0_4  []int  = []int{-74, -48, -42, -26, -16, -12, 0, 4, 8, 18, 46, 46, 62, 70, 74, 88, 92, 96, 98}
		param0_5  []int  = []int{0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0}
		param0_6  []int   = []int{27, 42, 59, 80}
		param0_7  []int   = []int{-96, -94, 10, -36, 18, -40}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int   = []int{96}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{3, 22, 2, 15, 18, 36, 2, 4, 12, 0}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
