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
	var ans int = 0
	for i := int(0); i < n; i++ {
		for j := int(i + 1); j < n; j++ {
			if arr[i] == arr[j] {
				ans++
			}
		}
	}
	return ans
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{4, 6, 9, 16, 16, 21, 36, 41, 58, 60, 62, 73, 77, 81, 95}
		param0_1  []int   = []int{-86, -72, -26, -34, 18, -62, -66}
		param0_2  []int   = []int{1}
		param0_3  []int   = []int{16}
		param0_4  []int  = []int{-88, -80, -72, -68, -64, -26, 4, 14, 16, 22, 30, 32, 60, 74, 82}
		param0_5  []int  = []int{0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1}
		param0_6  []int  = []int{3, 9, 10, 12, 17, 23, 27, 29, 42, 44, 59, 61, 71, 76, 78, 82, 84, 84, 89, 90, 93, 93, 97, 97}
		param0_7  []int   = []int{68, -40, -46, -20, -64, 90}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{99, 17, 94, 43, 97, 17, 11, 58, 75, 94, 37, 22, 54, 31, 41, 4, 55, 69, 92, 80, 45, 97, 16, 33, 36, 17, 43, 82, 81, 64, 22, 65, 85, 44, 47, 14}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{12, 3, 0, 0, 11, 9, 15, 5, 15, 23}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
