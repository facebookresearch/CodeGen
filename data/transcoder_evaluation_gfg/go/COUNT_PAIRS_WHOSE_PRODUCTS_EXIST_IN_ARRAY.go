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
	var result int = 0
	for i := int(0); i < n; i++ {
		for j := int(i + 1); j < n; j++ {
			var product int = arr[i] * arr[j]
			for k := int(0); k < n; k++ {
				if arr[k] == product {
					result++
					break
				}
			}
		}
	}
	return result
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{3, 7, 26, 40, 46, 89, 99}
		param0_1  []int  = []int{98, 42, -24, -60, 74, 86, 6, 8, 72, -58, 38, -20, 6, -6, 8, 48, -34, 30, 60, 66, 38, -54, 8, -94, -8, 0, -64, -94, -94, -72, -84, -36, 88, -62, -88, 46, -4, 88}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{37, 97, 57, 82, 29, 68, 94, 38, 81, 48, 13, 84, 57, 5, 27, 87, 11, 35, 82, 53, 67, 31, 15, 99, 6, 93, 91, 92, 3, 23, 90, 27, 6, 33, 78, 3, 19, 19, 27}
		param0_4  []int  = []int{-80, -74, -72, -72, -66, -66, -62, -50, -44, -44, -28, -24, -24, -22, -16, -10, -6, -4, -2, 2, 2, 4, 12, 16, 16, 28, 30, 32, 32, 38, 38, 72, 84, 86, 88, 90, 96}
		param0_5  []int  = []int{0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1}
		param0_6  []int   = []int{25, 67}
		param0_7  []int  = []int{82, 74, -82, 22, -28, -78, -22, -86, -74, 42, -6, 54, -88, -92, -14, -50, 68, 46, -50, 46, -18, 66, -76, -30, 36, 12, 66}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int   = []int{50, 23, 56, 9}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{5, 24, 44, 36, 34, 18, 1, 14, 32, 3}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
