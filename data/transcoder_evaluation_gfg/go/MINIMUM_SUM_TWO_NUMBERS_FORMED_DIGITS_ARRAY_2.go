package main

import (
		"fmt"
"sort"
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
	sort.Ints(a)
	var num1 int = 0
	var num2 int = 0
	for i := int(0); i < n; i++ {
		if i%2 == 0 {
			num1 = num1*10 + a[i]
		} else {
			num2 = num2*10 + a[i]
		}
	}
	return num2 + num1
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{4, 16, 29, 30, 38, 83}
		param0_1  []int  = []int{58, 74, -28, -60, -6, 66, -76, 46, 0, -24, 28, -16, -14, 24, -94, -56, -80, 40, -18, -68, -8, -94, -88, -12, -20, -8}
		param0_2  []int   = []int{0, 1}
		param0_3  []int   = []int{7, 12, 78, 8}
		param0_4  []int   = []int{-78, -48, -48, -26, 8, 34}
		param0_5  []int  = []int{1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0}
		param0_6  []int  = []int{2, 3, 5, 7, 25, 30, 31, 38, 42, 45, 52, 53, 56, 59, 60, 71, 74, 76, 80, 90, 91, 98}
		param0_7  []int  = []int{40, -62, -2, -58, 60, 38, 48, -4, 0, 62, -52, -80, 56, 38, 58, -72, 32, -26, -14, 70, 58, -86, -32, 56, -40, 84, 24, 60, -46, -32, 78, 78, -66, 20, -32, 98, 84, 44, 48, 4, 54, -66, 6, -62, 58}
		param0_8  []int   = []int{0, 0, 0, 0, 0, 0, 1, 1, 1}
		param0_9  []int  = []int{59, 9, 3, 20, 83, 87, 48, 4, 86, 67, 89, 96, 17, 36, 39, 45, 99, 8, 56, 92, 63, 81, 7, 75, 32, 10, 71, 82, 97, 92, 65, 23, 22, 47, 70, 79, 57, 81, 65, 50}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{5, 16, 1, 3, 4, 27, 13, 34, 8, 35}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
