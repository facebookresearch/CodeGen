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


func f_gold(A []int, N int, M int) int {
	var (
		sum int = 0
		ans int = 0
	)
	for i := int(0); i < N; i++ {
		for j := int(i + 1); j < N; j++ {
			for k := int(j + 1); k < N; k++ {
				sum = A[i] + A[j] + A[k]
				if sum%M == 0 {
					ans++
				}
			}
		}
	}
	return ans
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{14, 35, 56, 70, 88}
		param0_1  []int   = []int{-50, -92, 16, -68, -36}
		param0_2  []int   = []int{0, 0, 0, 1, 1, 1}
		param0_3  []int  = []int{76, 43, 22, 41, 49, 99, 25, 40, 3, 45, 60, 16, 83, 62, 26, 93, 64, 73, 72, 53, 6, 32, 35, 67, 17}
		param0_4  []int  = []int{-90, -86, -86, -66, -50, -48, -44, -42, -42, -38, -24, -22, -20, -18, -8, 8, 24, 28, 34, 48, 60, 62, 66, 68, 74, 76, 80, 82, 88}
		param0_5  []int  = []int{1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0}
		param0_6  []int  = []int{4, 5, 8, 9, 10, 12, 13, 16, 17, 18, 21, 21, 25, 27, 28, 30, 36, 36, 54, 55, 56, 57, 60, 62, 67, 67, 68, 71, 72, 72, 73, 73, 77, 77, 83, 86, 86, 86, 87, 89, 92, 92, 96, 97, 97, 98}
		param0_7  []int  = []int{-64, 52, -32, 38, 8, -62, -56, 20, 72, -12, 32, 44}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{77, 68, 45, 6, 27, 19, 29, 95, 21, 2, 39, 48, 72, 67, 49, 45, 1, 16, 56, 78, 25, 22, 27, 40, 31, 34, 26, 35, 12}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{3, 3, 4, 14, 24, 24, 24, 6, 12, 25}
		param2    []int  = []int{4, 4, 5, 21, 20, 30, 23, 6, 15, 25}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
