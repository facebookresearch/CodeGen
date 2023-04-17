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
	return arr[n-1] + arr[n-2] + arr[n-3]
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{6, 8, 18, 18, 27, 33, 33, 38, 42, 43, 44, 47, 52, 58, 64, 65, 67, 68, 71, 75, 85, 89, 91, 94, 94, 95, 95}
		param0_1  []int  = []int{24, 24, 44, 28, -88, 18, 34, 92, -84, 94, -12, 30, -82, -58}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{95, 75, 5, 51, 67, 63, 26, 47, 70, 11, 21, 9, 18, 31, 76, 66, 81, 73, 63, 55, 16, 72, 15, 28, 25, 25, 35, 79, 4, 73, 23, 87, 2, 1, 92, 94, 18, 70, 87, 27, 34, 84, 12}
		param0_4  []int  = []int{-86, -86, -78, -56, -24, -14, -10, -6, 12, 12, 18, 22, 22, 26, 50, 50, 72, 78, 94}
		param0_5  []int  = []int{0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0}
		param0_6  []int  = []int{2, 13, 17, 19, 20, 23, 28, 28, 29, 40, 45, 51, 52, 58, 58, 68, 70, 75, 79, 81, 92, 96, 97}
		param0_7  []int  = []int{94, 6, 52, 6, -78, 40, -46, -20, 64, 76, -36, -62, 50, -4, 4}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{34, 11, 15, 42, 32, 4, 6, 25, 52, 44, 14, 57, 3, 44, 7, 89, 35, 3, 70, 66, 58, 22, 5, 17, 33, 11}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{26, 8, 15, 37, 9, 9, 15, 13, 27, 13}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
