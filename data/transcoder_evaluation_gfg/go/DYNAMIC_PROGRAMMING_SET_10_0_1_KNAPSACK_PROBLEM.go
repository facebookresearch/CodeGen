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


func f_gold(W int, wt []int, val []int, n int) int {
	if n == 0 || W == 0 {
		return 0
	}
	if wt[n-1] > W {
		return f_gold(W, wt, val, n-1)
	} else {
		return max(val[n-1]+f_gold(W-wt[n-1], wt, val, n-1), f_gold(W, wt, val, n-1))
	}
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0    []int  = []int{5, 9, 26, 7, 46, 28, 25, 9, 13, 4}
		param1_0  []int   = []int{6, 14, 18, 36, 40, 47, 54, 58}
		param1_1  []int  = []int{42, 60, -4, 24, 54, 42, -72, -92, 48, -94, -36, 18}
		param1_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param1_3  []int  = []int{56, 53, 85, 73, 93, 75, 21, 22, 39, 13, 92}
		param1_4  []int  = []int{-96, -96, -94, -84, -78, -76, -74, -74, -72, -70, -70, -50, -48, -38, -30, -28, -28, -24, -14, -10, -4, -2, 6, 6, 18, 28, 30, 30, 34, 36, 42, 48, 50, 52, 54, 58, 58, 60, 62, 74, 74, 86, 86, 88, 88, 94, 96, 96, 98}
		param1_5  []int  = []int{1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0}
		param1_6  []int  = []int{7, 16, 18, 21, 22, 26, 30, 32, 34, 37, 37, 38, 39, 40, 44, 54, 55, 56, 56, 58, 59, 60, 62, 62, 64, 66, 75, 80, 82, 83, 84, 85, 88, 89, 89, 90, 93, 96, 97}
		param1_7  []int  = []int{64, -38, 76, -24, -10, 78, -76, 78, -32, 20}
		param1_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param1_9  []int   = []int{10, 87, 55, 78, 11}
		param1    [][]int = [][]int{param1_0, param1_1, param1_2, param1_3, param1_4, param1_5, param1_6, param1_7, param1_8, param1_9}
		param2_0  []int   = []int{9, 15, 23, 24, 41, 45, 50, 92}
		param2_1  []int  = []int{-20, 56, 20, -82, 84, -90, 54, 50, 82, 92, -32, 6}
		param2_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param2_3  []int  = []int{17, 27, 34, 86, 49, 89, 79, 70, 32, 23, 64}
		param2_4  []int  = []int{-92, -72, -72, -68, -60, -58, -52, -48, -46, -46, -44, -44, -42, -36, -32, -30, -30, -24, -22, -18, -16, -8, -6, -6, -4, -2, 6, 8, 16, 20, 20, 30, 32, 32, 36, 40, 42, 44, 44, 46, 54, 56, 56, 58, 82, 82, 86, 90, 90}
		param2_5  []int  = []int{1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0}
		param2_6  []int  = []int{1, 7, 9, 10, 11, 21, 23, 25, 29, 32, 35, 35, 35, 36, 37, 38, 42, 47, 47, 48, 51, 52, 55, 58, 64, 70, 72, 73, 74, 76, 77, 80, 86, 91, 92, 92, 92, 92, 96}
		param2_7  []int  = []int{64, 50, -78, 78, 78, 44, -14, -70, -76, 90}
		param2_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param2_9  []int   = []int{29, 43, 93, 2, 42}
		param2    [][]int = [][]int{param2_0, param2_1, param2_2, param2_3, param2_4, param2_5, param2_6, param2_7, param2_8, param2_9}
		param3    []int  = []int{7, 7, 15, 9, 28, 21, 31, 6, 14, 2}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], ([]int)(param1[i]), ([]int)(param2[i]), param3[i]) == f_gold(param0[i], ([]int)(param1[i]), ([]int)(param2[i]), param3[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
