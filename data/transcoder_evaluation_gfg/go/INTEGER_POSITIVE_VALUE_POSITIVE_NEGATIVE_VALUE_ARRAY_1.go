package main

import (
	"math"
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
	var (
		neg int = 0
		pos int = 0
		sum int = 0
	)
	for i := int(0); i < n; i++ {
		sum += arr[i]
		if arr[i] < 0 {
			neg++
		} else {
			pos++
		}
	}
	return sum / int(math.Abs(float64(neg-pos)))
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{49, 98}
		param0_1  []int   = []int{82, 66, -68, 24, -10}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{56, 3, 18, 5, 20, 56, 47, 29, 60, 98, 60, 40, 42, 2, 54, 56, 91, 8, 93, 14, 31, 27, 61, 49, 23, 12, 71}
		param0_4  []int  = []int{-94, -94, -92, -86, -50, -48, -6, 8, 28, 40, 44, 58, 62, 72, 94}
		param0_5  []int  = []int{0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1}
		param0_6  []int   = []int{16, 56, 56}
		param0_7  []int   = []int{74, -90, -92, 30, -18, 66, -66, 22}
		param0_8  []int  = []int{0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int   = []int{21, 64, 82, 78, 30, 34, 35}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{1, 2, 8, 25, 12, 36, 1, 5, 7, 5}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
