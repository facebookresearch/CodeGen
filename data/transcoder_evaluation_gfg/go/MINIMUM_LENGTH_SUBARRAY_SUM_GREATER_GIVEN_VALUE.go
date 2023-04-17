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


func f_gold(arr []int, n int, x int) int {
	var (
		curr_sum int = 0
		min_len  int = n + 1
		start    int = 0
		end      int = 0
	)
	for end < n {
		for curr_sum <= x && end < n {
			curr_sum += arr[func() int {
				p := &end
				x := *p
				*p++
				return x
			}()]
		}
		for curr_sum > x && start < n {
			if end-start < min_len {
				min_len = end - start
			}
			curr_sum -= arr[func() int {
				p := &start
				x := *p
				*p++
				return x
			}()]
		}
	}
	return min_len
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{6, 11, 11, 14, 18, 19, 21, 22, 22, 23, 26, 27, 28, 28, 29, 30, 31, 34, 39, 42, 42, 44, 45, 49, 49, 53, 57, 61, 65, 66, 67, 70, 71, 73, 74, 74, 78, 85, 88, 94, 95, 97}
		param0_1  []int  = []int{-30, -22, -66, -80, 18, -64, -28, -46, 94, 60, -64, 2, 26, -94, 58, 56, 56, 88, 50, -78, -12, 68, 54, -78, 42, -30, 24, -48, 84, 12, -88, 0, 54, -92, -4, 42, -60, -72, -32}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{86, 8, 23, 40, 55, 93, 11, 35, 33, 37, 96, 91, 35, 66, 37, 57, 83, 99, 96, 15, 18, 93}
		param0_4  []int  = []int{-92, -68, -48, -48, -42, -26, -22, -18, 2, 4, 8, 14, 20, 22, 32, 46, 52, 62, 70, 96, 98}
		param0_5  []int  = []int{0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0}
		param0_6  []int  = []int{4, 4, 11, 11, 13, 15, 16, 18, 19, 19, 19, 23, 26, 27, 34, 39, 39, 40, 41, 46, 47, 51, 52, 52, 53, 57, 58, 58, 60, 64, 68, 70, 72, 84, 84, 85, 95, 98, 99}
		param0_7  []int  = []int{12, -22, 2, -90, -92, 84, -26, -76, -72, 50, -36, 30, 78, -18, -94, -30, 22, 28, 10, 32, 34, -86, 0, -4, 40, 0, 80, 50, 66, -48, -40, -94, 64, 58, -14, 0, -32, -58, -22, -94, -68, -36, -94, -48, 40, 78, -74}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{1, 33, 20, 32, 76, 27, 8, 95, 78, 72, 25, 56}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{37, 31, 8, 16, 17, 11, 31, 42, 25, 9}
		param2    []int  = []int{23, 29, 12, 13, 14, 10, 35, 26, 21, 10}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
