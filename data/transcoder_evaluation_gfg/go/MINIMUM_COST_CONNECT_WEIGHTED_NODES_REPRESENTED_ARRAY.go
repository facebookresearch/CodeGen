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
	var (
		mn  int = math.MaxInt64
		sum int = 0
	)
	for i := int(0); i < n; i++ {
		mn = min(a[i], mn)
		sum += a[i]
	}
	return mn * (sum - mn)
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{3, 8, 14, 15, 17, 17, 19, 21, 22, 23, 29, 32, 36, 37, 43, 45, 46, 47, 47, 53, 57, 57, 70, 71, 72, 76, 81, 82, 90, 95, 96, 98, 99}
		param0_1  []int  = []int{94, -18, 50, 94, -74, -50, -44, -92, -58, 14, -66, -78}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{15, 18, 64, 28}
		param0_4  []int  = []int{-96, -88, -88, -84, -82, -78, -78, -60, -58, -56, -54, -52, -48, -44, -28, -26, -14, -12, 6, 10, 10, 14, 14, 50, 52, 54, 60, 62, 62, 64, 66, 70, 72, 72, 78, 80, 84}
		param0_5  []int   = []int{0, 1, 1, 0, 1, 1, 1, 1}
		param0_6  []int  = []int{3, 10, 14, 14, 15, 16, 18, 20, 21, 30, 31, 33, 35, 39, 46, 48, 59, 59, 61, 77, 78, 79, 81, 83, 85, 92, 97, 97, 99}
		param0_7  []int  = []int{4, -32, 68, -48, 54, 24, 78, 98, -70, 44, -82, -92, -16, -92, -70, 52, -58, -62, -58, 32, 14, -4, 80, -78, -26, -24, -8}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{82, 74, 53, 91, 81, 88, 42, 62, 38, 43, 29, 60, 43, 44, 19, 28, 20, 1, 5, 94, 18, 77, 52, 38, 55, 1, 10, 29, 34, 91, 64, 80, 81, 39, 4, 47, 30, 62, 58, 66, 73, 52, 62, 9, 36, 49}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{32, 10, 24, 2, 31, 6, 23, 18, 35, 38}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
