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


func f_gold(arr []int, n int) int {
	sort.Ints(arr)
	var a int = 0
	var b int = 0
	for i := int(0); i < n; i++ {
		if i&1 != 0 {
			a = a*10 + arr[i]
		} else {
			b = b*10 + arr[i]
		}
	}
	return a + b
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{3, 4, 5, 10, 14, 16, 18, 42, 43, 43, 45, 46, 51, 52, 53, 58, 61, 66, 79, 81, 82, 84}
		param0_1  []int  = []int{48, -22, 60, 32, 48, -2, -76, -50, -26, 56, -86, 98, -30, -22, 82, -20, 58, 40, 76, -2, 82, -90, 8, -46, 22, 94}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{79, 45}
		param0_4  []int  = []int{-90, -68, -38, -34, -4, 6, 10, 28, 48, 52, 54, 68, 88, 90}
		param0_5  []int  = []int{1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0}
		param0_6  []int  = []int{4, 8, 8, 23, 26, 27, 30, 42, 44, 55, 59, 64, 67, 69, 74, 77, 82, 82, 87, 96, 97}
		param0_7  []int  = []int{0, -18, -98, -36, -62, 0, -32, -98, 46, 72, -18, 30, -86, -42, -82, 2, -76, -64, -66, -48, -28, 52, -46, -76, 76, 10, 70, 4, 18, 94, 88, 80, -60, -36, 62, 96, -4, 88, 50}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 1, 1, 1, 1}
		param0_9  []int  = []int{8, 71, 75, 58, 97, 24, 56, 98, 71, 69, 32, 64, 54, 96, 69, 22, 7, 47, 45, 68, 17, 36, 90, 9, 71, 86, 16, 61, 53, 63, 9, 74, 38, 87, 14, 86, 42, 42, 14, 43, 58, 82, 72, 73, 32}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{19, 25, 23, 1, 11, 22, 17, 32, 6, 25}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
