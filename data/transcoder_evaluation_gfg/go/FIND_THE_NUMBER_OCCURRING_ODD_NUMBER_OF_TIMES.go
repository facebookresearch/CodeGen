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


func f_gold(arr []int, arr_size int) int {
	for i := int(0); i < arr_size; i++ {
		var count int = 0
		for j := int(0); j < arr_size; j++ {
			if arr[i] == arr[j] {
				count++
			}
		}
		if count%2 != 0 {
			return arr[i]
		}
	}
	return -1
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{1, 5, 5, 8, 14, 15, 17, 17, 18, 23, 23, 25, 26, 35, 36, 39, 51, 53, 56, 56, 60, 62, 64, 64, 65, 66, 67, 68, 71, 75, 80, 82, 83, 88, 89, 91, 91, 92, 93, 95, 99}
		param0_1  []int  = []int{-56, 98, 44, 30, -88, 18, 60, 86, 4, 16, 10, 64, -22, -86, -66, -16, 70, -44, 98, 78, -96, -66, 92, 10, 40, -16}
		param0_2  []int   = []int{0, 0, 0, 0, 0, 1, 1, 1}
		param0_3  []int  = []int{36, 11, 83, 41, 42, 14, 46, 89, 91, 96, 57, 42, 74, 73, 9, 26, 79, 40, 31, 69, 44, 39, 14, 92, 34, 20, 52, 47, 14}
		param0_4  []int  = []int{-84, -84, -84, -78, -66, -62, -62, -36, -24, -10, -10, -8, -4, -2, 12, 14, 20, 22, 36, 42, 46, 66, 84, 96, 96, 98}
		param0_5  []int  = []int{1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1}
		param0_6  []int  = []int{11, 12, 14, 28, 42, 48, 50, 58, 67, 74, 86, 89, 95}
		param0_7  []int  = []int{52, -56, -6, 74, 10, 68, 74, 10, 16, -80, 82, -32, 6, -6, 82, 20}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int   = []int{4, 80, 92}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{31, 19, 6, 25, 23, 19, 7, 11, 31, 1}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
