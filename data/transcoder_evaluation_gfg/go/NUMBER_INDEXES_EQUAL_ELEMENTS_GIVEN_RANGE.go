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


func f_gold(a []int, n int, l int, r int) int {
	var count int = 0
	for i := int(l); i < r; i++ {
		if a[i] == a[i+1] {
			count += 1
		}
	}
	return count
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{4, 13, 13, 16, 16, 19, 39, 41, 48, 52, 57, 62, 65, 67, 76, 84, 88, 91, 95, 96, 97, 98}
		param0_1  []int  = []int{62, 76, 86, -8, 84, -6, 72, 84, 6, -50, -18, -94, 54, 90, -74, -64, -26, -14, -32, 62, 10, 4, 70, -28, 8, 18, 4, -62, -76, 84, -78, -4, 84, 98, 58, -68, 42, -6, 34, -38, 52, -84, 78}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{11, 75, 98, 29, 62, 53, 48, 91, 86, 66, 48, 94}
		param0_4  []int  = []int{-94, -84, -70, -70, -40, -40, -36, -24, 10, 48, 62, 74}
		param0_5  []int  = []int{1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0}
		param0_6  []int  = []int{1, 2, 6, 7, 10, 11, 13, 19, 19, 25, 29, 30, 32, 34, 35, 45, 45, 46, 47, 48, 48, 53, 58, 61, 64, 65, 67, 75, 76, 81, 81, 84, 84, 85, 86, 94, 94, 96, 99}
		param0_7  []int  = []int{-56, 42, -34, -12, -86, 82, -96, -66, 30, 16, -40, 72, 84, 94, -48, -30, 26, 50, 42, -44, -50, 22, -38, 8, 34, 94, 2, 16, -32, 18, -58, 12, -26, 28, -62}
		param0_8  []int   = []int{0, 0, 0, 0, 1, 1, 1}
		param0_9  []int   = []int{6, 29}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{18, 32, 10, 8, 11, 36, 25, 21, 4, 1}
		param2    []int  = []int{12, 38, 6, 6, 7, 40, 19, 30, 5, 1}
		param3    []int  = []int{17, 23, 6, 6, 8, 37, 37, 26, 5, 1}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i], param3[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i], param3[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
