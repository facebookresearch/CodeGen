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


func f_gold(arr []int, dep []int, n int) int {
	sort.Ints(arr)
	sort.Ints(dep)
	var plat_needed int = 1
	var result int = 1
	var i int = 1
	var j int = 0
	for i < n && j < n {
		if arr[i] <= dep[j] {
			plat_needed++
			i++
			if plat_needed > result {
				result = plat_needed
			}
		} else {
			plat_needed--
			j++
		}
	}
	return result
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{8, 24, 28, 64, 75, 86, 93, 95}
		param0_1  []int  = []int{2, -30, -8, -78, 58, -42, -94, 84, -58, 14, 78, 34, 30, 6, -18, -92, 0, 94, -54, 58, 0, -86, 66, 86, 8, -26, 50, 16, -30, -68, 98, -28, -4, -6}
		param0_2  []int   = []int{0, 0, 0, 0, 0, 0, 1}
		param0_3  []int  = []int{51, 5, 48, 61, 71, 2, 4, 35, 50, 76, 59, 64, 81, 5, 21, 95}
		param0_4  []int   = []int{-64, -52, 44, 52, 90}
		param0_5  []int  = []int{0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1}
		param0_6  []int   = []int{2, 15, 25, 55, 72, 96, 98}
		param0_7  []int  = []int{-60, 30, -58, 52, 40, 74, 74, 76, -72, -48, 8, -56, -24, -40, -98, -76, -56, -20, 30, -30, -34, 4, -34}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int   = []int{37, 84, 20, 34, 56, 1, 87, 72}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1_0  []int   = []int{19, 30, 41, 51, 62, 68, 85, 96}
		param1_1  []int  = []int{40, 22, -24, 80, -76, -4, -8, -34, 96, -98, 16, 28, 14, 52, 10, -10, -62, 64, -48, 10, -64, -90, -52, 46, 34, 50, 50, -84, 68, -12, -44, 28, -22, 78}
		param1_2  []int   = []int{0, 0, 0, 0, 0, 1, 1}
		param1_3  []int  = []int{67, 84, 86, 43, 50, 90, 49, 8, 40, 67, 5, 51, 40, 28, 31, 47}
		param1_4  []int   = []int{-62, -16, 22, 26, 58}
		param1_5  []int  = []int{0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0}
		param1_6  []int   = []int{3, 6, 11, 19, 26, 37, 39}
		param1_7  []int  = []int{-96, -40, -76, 52, -20, -28, -64, -72, 36, 56, 52, 34, 14, 8, -50, 6, -82, -98, -8, 18, -76, -66, -22}
		param1_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param1_9  []int   = []int{68, 62, 84, 54, 15, 29, 70, 96}
		param1    [][]int = [][]int{param1_0, param1_1, param1_2, param1_3, param1_4, param1_5, param1_6, param1_7, param1_8, param1_9}
		param2    []int  = []int{6, 18, 6, 8, 3, 17, 6, 20, 22, 6}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), ([]int)(param1[i]), param2[i]) == f_gold(([]int)(param0[i]), ([]int)(param1[i]), param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
