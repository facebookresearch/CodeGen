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
			if curr_sum <= 0 && x > 0 {
				start = end
				curr_sum = 0
			}
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
		param0_0  []int  = []int{2, 4, 5, 10, 14, 15, 16, 20, 23, 28, 31, 35, 36, 36, 43, 48, 49, 55, 57, 57, 58, 61, 64, 64, 68, 70, 70, 73, 74, 76, 76, 77, 81, 81, 82, 87, 89, 92, 99}
		param0_1  []int  = []int{66, -20, 12, -48, 22, 28, 40, -30, -6, -96, 10, -88, 40}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{28, 19, 38, 31, 17, 27, 60, 35, 19, 47, 34, 51, 3, 95, 33, 29, 84, 46, 74, 87}
		param0_4  []int   = []int{-48, -2}
		param0_5  []int  = []int{1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1}
		param0_6  []int  = []int{1, 4, 4, 6, 8, 10, 12, 12, 13, 15, 18, 20, 21, 23, 25, 28, 28, 33, 33, 35, 35, 36, 37, 38, 42, 44, 63, 63, 65, 65, 65, 66, 70, 74, 77, 78, 80, 80, 84, 87, 87, 89, 92, 93, 94, 97, 98, 99}
		param0_7  []int  = []int{-82, -12, -40, 58, 22, -76, -94, -28, 42, 36, 64}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{76, 65, 96, 76, 1, 91, 22, 29, 95, 21, 73, 68, 30, 52, 73, 86, 52, 66, 67, 37, 76, 53, 68, 6, 95, 81, 98, 42, 63, 38, 92, 78, 59, 86, 10, 38, 18, 15, 52, 62, 16, 66}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{33, 11, 42, 15, 1, 12, 42, 10, 10, 23}
		param2    []int  = []int{28, 12, 23, 15, 1, 15, 27, 6, 14, 35}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
