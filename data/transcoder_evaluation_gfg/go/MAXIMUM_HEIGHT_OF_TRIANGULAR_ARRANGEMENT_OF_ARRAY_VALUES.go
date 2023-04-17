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


func f_gold(a []int, n int) int {
	var result int = 1
	for i := int(1); i <= n; i++ {
		var y float64 = float64((i * (i + 1)) / 2)
		if y < float64(n) {
			result = i
		} else {
			break
		}
	}
	return result
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{8, 10, 11, 14, 14, 17, 20, 20, 22, 22, 22, 23, 25, 30, 33, 39, 39, 41, 43, 45, 46, 46, 46, 50, 51, 53, 57, 59, 60, 64, 64, 66, 72, 72, 75, 77, 85, 85, 87, 88, 90, 91, 93, 94, 94, 95}
		param0_1  []int  = []int{-44, -90, 20, 4, -56, -50, -80, 74, -82, 20, 62, -26, -10, -14, -76, 82, -88, 92, 30, 44, -62, -86, -20, -96, -60, -88, -78, -40, -48, -92, 62, 58, 94, 68, 68, 44, 80, 4, 48, -92, 30, -76, -46, -20, 4}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{8, 34, 48, 10, 5, 12, 80, 7, 67, 1, 79, 59, 63, 13, 16, 23, 62, 56, 99, 89, 7, 80}
		param0_4  []int   = []int{-88, -46, -40, -40, 38}
		param0_5  []int  = []int{1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1}
		param0_6  []int   = []int{8, 15, 35, 39, 49, 81, 86, 91}
		param0_7  []int  = []int{-24, 56, -74, -76, -80, 86, 90, 0, -26, 18, 72, 78, -66, -28, 22, 22, 72, 78, -50, -12, 20, 12, -68, -2, -58, -44, 28, -58, 90, -28, 32, -70, -48, -66, -94, -50, 18, -12, 80, 12, 82, 56, -64, 10, -22}
		param0_8  []int   = []int{}
		param0_9  []int  = []int{62, 93, 69, 40, 26, 2, 29, 83, 66, 68, 67, 73, 12, 65, 89, 57, 38, 99, 42, 27, 38, 24, 43, 4, 4, 54, 72, 47, 52, 46, 53, 24, 3, 41, 64, 33, 88, 3, 1, 7, 17, 31, 20, 33, 69, 21, 9, 24, 59}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{38, 36, 28, 12, 3, 44, 7, 36, 1, 26}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
