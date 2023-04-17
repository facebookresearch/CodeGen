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


func f_gold(arr []int, n int) int {
	var (
		ones            int = 0
		twos            int = 0
		common_bit_mask int
	)
	for i := int(0); i < n; i++ {
		twos = twos | (ones & arr[i])
		ones = ones ^ arr[i]
		common_bit_mask = ^(ones & twos)
		ones &= common_bit_mask
		twos &= common_bit_mask
	}
	return ones
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{7, 26, 26, 48, 59, 62, 66, 70, 72, 75, 76, 81, 97, 98}
		param0_1  []int  = []int{-42, -48, -64, -74, 56, -34, 20, 16, 34, -84, 86, 38, 56, -86, 30, -74, -96, 96, 12, 10, -46, 10, -36, 38, 34, -46, -20, 14, 12, 62, -54, 20, -82, 24, 96}
		param0_2  []int   = []int{0, 0, 1, 1}
		param0_3  []int  = []int{68, 91, 61, 6, 32, 47, 76, 69, 44, 71, 29, 79, 74, 33, 44, 33, 45, 75, 43, 82, 83, 81, 95, 16, 86, 33, 69, 61, 73, 21, 54, 17, 98, 62, 14, 72, 80, 31, 56, 82, 14, 48, 76}
		param0_4  []int  = []int{-98, -96, -92, -62, -52, -42, -42, -26, 4, 10, 14, 38, 64, 66, 72, 74, 82}
		param0_5  []int  = []int{0, 1, 1, 1, 0, 0, 0, 1, 0, 1}
		param0_6  []int   = []int{53, 63, 63}
		param0_7  []int  = []int{-96, -38, -26, -46, 68, -36, 20, -18, -10, 52, 40, 94, -8, -64, 82, -22}
		param0_8  []int   = []int{0, 0, 0, 0, 0, 1, 1}
		param0_9  []int  = []int{99, 46, 48, 81, 27, 97, 26, 50, 77, 32, 45, 99, 46}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{7, 27, 3, 38, 14, 5, 2, 15, 3, 12}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
