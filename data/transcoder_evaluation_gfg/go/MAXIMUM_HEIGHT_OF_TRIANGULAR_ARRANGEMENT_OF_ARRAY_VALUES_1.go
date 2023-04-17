package main

import (
		"fmt"
	"math"
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
	return int(math.Floor((math.Sqrt(float64((n*8)+1)) + float64(-1)) / 2))
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{1, 2, 2, 3, 5, 6, 7, 8, 8, 12, 15, 16, 18, 18, 20, 21, 21, 22, 22, 24, 24, 25, 30, 35, 42, 49, 52, 55, 55, 63, 68, 70, 72, 73, 77, 80, 83, 87, 87, 88, 88, 94, 95, 97}
		param0_1  []int  = []int{48, -72, 84, -24, 28, 94, 36, 28, 32, 66, -62, 64, 6, -68, -12, 46, 4, 98, 18, 86, -60, 76, 14, 98}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{11, 16, 84, 8, 86, 44, 79, 11, 73, 12, 29, 62, 22, 44, 28, 8, 48, 92, 73, 63, 59, 44, 95, 66}
		param0_4  []int  = []int{-94, -94, -92, -88, -86, -82, -80, -80, -78, -76, -56, -56, -50, -44, -42, -36, -36, -32, -32, -26, -14, -12, -6, 12, 24, 28, 34, 38, 42, 42, 46, 50, 56, 62, 62, 74, 84, 92, 94}
		param0_5  []int  = []int{0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0}
		param0_6  []int  = []int{2, 2, 3, 3, 3, 4, 5, 13, 16, 18, 21, 22, 27, 28, 32, 34, 36, 37, 41, 42, 43, 51, 52, 52, 54, 54, 61, 65, 67, 67, 68, 71, 75, 77, 77, 78, 80, 81, 81, 84, 86, 90, 90, 93, 93, 94, 99, 99}
		param0_7  []int   = []int{54, -86}
		param0_8  []int   = []int{0, 1}
		param0_9  []int  = []int{5, 54, 49, 80, 56, 62, 31, 49, 60, 19, 45, 94, 33, 46, 32}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{22, 12, 25, 14, 19, 24, 31, 1, 1, 8}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
