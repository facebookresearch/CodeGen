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
	var (
		i     int
		total int = 1
	)
	for i = 2; i <= (n + 1); i++ {
		total += i
		total -= a[i-2]
	}
	return total
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{13, 27, 46, 59, 62, 82, 92}
		param0_1  []int  = []int{22, 86, -64, -20, -56, -16, 86, 42, 72, -90, 10, 42, 56, 8, 50, 24, -34, 0, -78, 64, 18, 20, -84, -22, 90, -20, 86, 26, -54, 0, 90, -48, 4, 88, 18, -64, -22, -74, 48, -36, -86, -24, 88, -64, 68, 62, 92}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{55, 89, 56, 85, 26, 4, 91, 91, 3, 77, 63, 59, 76, 90, 1, 94, 44, 70, 8, 54, 3, 91, 29, 95, 28, 75, 20}
		param0_4  []int  = []int{-94, -84, -80, -78, -66, -62, -54, -52, -26, -8, -8, -6, 4, 4, 8, 14, 26, 58, 60, 62, 62, 76, 78, 86, 92}
		param0_5  []int  = []int{1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0}
		param0_6  []int  = []int{1, 2, 7, 7, 9, 14, 23, 29, 31, 31, 35, 35, 38, 41, 44, 49, 49, 50, 51, 54, 55, 56, 57, 63, 67, 69, 73, 79, 79, 80, 86, 88, 93}
		param0_7  []int  = []int{78, -48, 16, 22, -16, 34, 56, -20, -62, -82, -74, -40, 20, -24, -46, 64, 66, -76, 58, -84, 96, 76, 86, -32, 46}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{73, 76, 25, 59, 40, 85, 90, 38, 13, 97, 93, 99, 45, 7}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{6, 38, 15, 22, 18, 25, 24, 12, 29, 12}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
