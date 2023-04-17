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


func f_gold(arr []int, n int, k int) int {
	var dist_count int = 0
	for i := int(0); i < n; i++ {
		var j int
		for j = 0; j < n; j++ {
			if i != j && arr[j] == arr[i] {
				break
			}
		}
		if j == n {
			dist_count++
		}
		if dist_count == k {
			return arr[i]
		}
	}
	return -1
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{2, 3, 8, 18, 20, 33, 53, 56, 60, 71, 76, 80, 81, 87, 88, 89, 92, 95}
		param0_1  []int  = []int{-78, 6, 32, 52, -12, -32, 22, -40, -82, 24, 30, 10, -40}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{3, 28, 55, 21, 42, 60, 96, 83, 98, 75, 29, 73, 51, 21, 27, 65, 19, 47, 12, 81, 19, 94, 50, 43, 21, 32, 52, 44, 52, 91, 49, 59, 52, 10, 75, 86, 46, 43, 3, 49, 70, 60, 77, 99, 27, 63}
		param0_4  []int  = []int{-96, -90, -76, -44, -16, -8, 0, 0, 2, 2, 8, 14, 16, 18, 18, 20, 20, 28, 34, 44, 68, 74, 84, 90}
		param0_5  []int  = []int{0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0}
		param0_6  []int  = []int{3, 4, 5, 8, 9, 15, 26, 26, 26, 35, 39, 40, 42, 43, 45, 45, 48, 52, 54, 56, 57, 67, 74, 77, 79, 80, 81, 86, 87, 92, 95, 97}
		param0_7  []int  = []int{-76, -24, -12, 66, -40, 26, 72, 46, -56, 58, -68, 2, -82}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{29, 83, 32, 75, 5, 22, 68, 64, 36, 18, 7, 63, 16, 42, 77, 61, 1, 26, 12, 41, 67, 85, 85, 35, 94, 18, 14, 65, 8, 55, 44, 34, 48, 23, 8, 27, 86, 2, 51, 91}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{16, 8, 7, 40, 23, 10, 26, 6, 27, 28}
		param2    []int  = []int{16, 6, 5, 39, 12, 8, 24, 10, 17, 24}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
