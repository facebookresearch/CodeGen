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


func f_gold(a1 []int, a2 []int, a3 []int, n1 int, n2 int, n3 int, sum int) bool {
	for i := int(0); i < n1; i++ {
		for j := int(0); j < n2; j++ {
			for k := int(0); k < n3; k++ {
				if a1[i]+a2[j]+a3[k] == sum {
					return true
				}
			}
		}
	}
	return false
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{4, 9, 10, 19, 24, 25, 26, 30, 36, 43, 44, 49, 52, 62, 66, 69, 72, 77, 80, 80, 82, 84, 90, 93, 94, 98}
		param0_1  []int  = []int{-24, -80, -72, 80, -96, -94, 64, 18, 12, 16, 74, 16, 54, 66, -96, -90, 54, 72, -32, -2, 90, -18, -98, 12, -42, -30, -82, -56, -86, 40}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{28, 15, 21, 28, 85, 68, 24}
		param0_4  []int  = []int{-86, -82, -66, -44, -44, -38, -22, -6, -2, 14, 26, 40, 54, 58, 60, 66, 72, 80, 94, 96, 98}
		param0_5  []int  = []int{1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1}
		param0_6  []int   = []int{44, 53, 85, 85, 86, 88, 93}
		param0_7  []int   = []int{70, -38, 62, -34, 74, -32, -58, -34, -54}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{41, 64, 39, 96, 54, 54, 57, 4, 82, 43, 44, 56, 1}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1_0  []int  = []int{4, 8, 17, 20, 22, 25, 27, 30, 31, 33, 35, 35, 38, 41, 49, 51, 60, 61, 66, 67, 69, 82, 84, 85, 86, 88}
		param1_1  []int  = []int{30, -60, -24, 18, 40, 44, -40, 62, 66, -38, 50, -74, -42, -86, -82, -8, 50, -72, -2, -48, -38, -20, -8, 56, -32, 68, 94, 80, -48, 0}
		param1_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1}
		param1_3  []int   = []int{57, 46, 47, 49, 16, 81, 60}
		param1_4  []int  = []int{-96, -86, -74, -56, -52, -42, -32, -22, -16, -10, -4, -4, 10, 42, 48, 52, 58, 62, 84, 90, 96}
		param1_5  []int  = []int{0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1}
		param1_6  []int   = []int{4, 5, 8, 15, 29, 40, 91}
		param1_7  []int   = []int{48, -86, -18, 14, 88, 92, -56, -8, -74}
		param1_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param1_9  []int  = []int{44, 58, 40, 87, 22, 82, 8, 81, 88, 42, 15, 14, 81}
		param1    [][]int = [][]int{param1_0, param1_1, param1_2, param1_3, param1_4, param1_5, param1_6, param1_7, param1_8, param1_9}
		param2_0  []int  = []int{12, 14, 17, 20, 22, 27, 29, 31, 32, 38, 41, 43, 56, 59, 59, 64, 66, 67, 68, 69, 71, 76, 83, 83, 85, 99}
		param2_1  []int  = []int{-24, 80, 50, -56, -92, 20, 86, -42, -30, 96, 40, -32, -64, 54, -38, -72, -70, 54, -28, 98, 60, 98, -12, -30, -30, 68, -66, 68, -58, 52}
		param2_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1}
		param2_3  []int   = []int{76, 49, 6, 44, 71, 24, 57}
		param2_4  []int  = []int{-92, -92, -90, -82, -62, -44, -42, -40, -38, -36, -22, -20, -8, 12, 22, 26, 30, 44, 54, 64, 86}
		param2_5  []int  = []int{1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0}
		param2_6  []int   = []int{30, 53, 71, 75, 76, 82, 84}
		param2_7  []int   = []int{8, 8, 32, 76, 76, 94, 22, -60, -42}
		param2_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1}
		param2_9  []int  = []int{64, 20, 24, 42, 37, 46, 6, 47, 12, 93, 8, 5, 11}
		param2    [][]int = [][]int{param2_0, param2_1, param2_2, param2_3, param2_4, param2_5, param2_6, param2_7, param2_8, param2_9}
		param3    []int  = []int{25, 26, 14, 6, 13, 25, 5, 6, 15, 7}
		param4    []int  = []int{18, 22, 14, 5, 20, 25, 3, 6, 14, 8}
		param5    []int  = []int{16, 20, 14, 5, 17, 23, 4, 6, 10, 6}
		param6    []int  = []int{222, 21, 2, 73, 6, 0, 3, 7, 13, 10}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), ([]int)(param1[i]), ([]int)(param2[i]), param3[i], param4[i], param5[i], param6[i]) == f_gold(([]int)(param0[i]), ([]int)(param1[i]), ([]int)(param2[i]), param3[i], param4[i], param5[i], param6[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
