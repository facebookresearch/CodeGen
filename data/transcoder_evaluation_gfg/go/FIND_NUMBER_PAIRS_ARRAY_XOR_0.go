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
	var count int = 1
	var answer int = 0
	for i := int(1); i < n; i++ {
		if a[i] == a[i-1] {
			count += 1
		} else {
			answer = answer + (count*(count-1))/2
			count = 1
		}
	}
	answer = answer + (count*(count-1))/2
	return answer
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{4, 7, 9, 12, 13, 13, 14, 16, 19, 23, 24, 25, 28, 29, 38, 38, 41, 42, 44, 51, 55, 56, 58, 59, 61, 62, 62, 63, 63, 64, 67, 68, 69, 71, 78, 78, 80, 82, 82, 82, 83, 85, 86, 92, 94, 98}
		param0_1  []int  = []int{42, -20, 52, 34, 58, 62, -60, 70, 36, -8, -26, 68, 34, -92, 42, 94, 56, 84, -70, 70}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{31, 87, 75, 69, 11, 65, 25, 27}
		param0_4  []int  = []int{-92, -88, -86, -74, -72, -70, -70, -66, -62, -60, -52, -42, -42, 8, 14, 30, 36, 84, 88}
		param0_5  []int   = []int{1, 0, 0, 0}
		param0_6  []int  = []int{2, 8, 9, 12, 21, 23, 30, 31, 33, 34, 34, 41, 43, 45, 52, 53, 53, 55, 56, 61, 73, 73, 73, 74, 76, 79, 81, 81, 81, 90, 91, 92, 92, 97, 99, 99}
		param0_7  []int  = []int{84, 6, -36, 62, -2, -32, -82, -78, 20, 8, -50, -70, 20, -58, 94, -28, -84, -22, -44, -84, 2, -68, -34, 58, -64, -86, -40, -80, 74, -26, 12, 2, -20, 20, 76, -14, -40, 56, 24, -16, -66, 14, -42, 0, 72, 82, -70}
		param0_8  []int   = []int{0, 0, 0, 0, 0, 0, 0, 1, 1}
		param0_9  []int  = []int{67, 93, 54, 91, 74, 88, 48, 68, 17, 6, 15, 25}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{24, 17, 37, 5, 13, 3, 30, 31, 8, 9}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
