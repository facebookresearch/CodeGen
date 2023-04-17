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


func f_gold(n int, templeHeight []int) int {
	var sum int = 0
	for i := int(0); i < n; i++ {
		var (
			left  int = 0
			right int = 0
		)
		for j := int(i - 1); j >= 0; j-- {
			if templeHeight[j] < templeHeight[j+1] {
				left++
			} else {
				break
			}
		}
		for j := int(i + 1); j < n; j++ {
			if templeHeight[j] < templeHeight[j-1] {
				right++
			} else {
				break
			}
		}
		sum += max(right, left) + 1
	}
	return sum
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0    []int  = []int{12, 46, 16, 9, 0, 38, 28, 9, 18, 29}
		param1_0  []int  = []int{3, 11, 12, 15, 16, 21, 24, 29, 32, 39, 42, 44, 51, 68, 79, 81, 81, 85, 92, 94}
		param1_1  []int  = []int{76, 48, 88, 70, -64, 66, -6, -58, 26, -28, -42, -94, 80, -4, -56, -46, 4, 90, -12, -78, 64, 18, -38, 26, 56, -24, 66, -18, -12, 0, -94, 12, -10, 4, -68, -20, 88, 2, -58, 16, 46, -80, -42, 44, -86, 96, -44}
		param1_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param1_3  []int  = []int{2, 95, 20, 50, 2, 58, 20, 14, 65, 69, 78, 7}
		param1_4  []int   = []int{-88}
		param1_5  []int  = []int{0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0}
		param1_6  []int  = []int{2, 3, 6, 8, 9, 10, 14, 17, 17, 22, 25, 27, 29, 29, 30, 32, 33, 35, 38, 42, 50, 51, 51, 57, 59, 59, 59, 60, 62, 62, 63, 67, 70, 75, 76, 77, 81, 81, 83, 84}
		param1_7  []int  = []int{-52, 62, 74, -62, -58, 62, 38, 42, -50, 20}
		param1_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param1_9  []int  = []int{96, 15, 9, 9, 40, 34, 17, 4, 51, 49, 34, 66, 97, 28, 64, 65, 92, 56, 74, 48, 43, 17, 82, 8, 21, 39, 83, 35, 42, 37, 64, 34, 42, 59, 45, 61, 55, 93, 94, 29, 20, 96, 77, 66}
		param1    [][]int = [][]int{param1_0, param1_1, param1_2, param1_3, param1_4, param1_5, param1_6, param1_7, param1_8, param1_9}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], ([]int)(param1[i])) == f_gold(param0[i], ([]int)(param1[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
