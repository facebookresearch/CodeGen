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
		l   int = 0
		sum int = 0
		ans int = 360
	)
	for i := int(0); i < n; i++ {
		sum += arr[i]
		for sum >= 180 {
			ans = min(ans, int(math.Abs(float64(180-sum))*2))
			sum -= arr[l]
			l++
		}
		ans = min(ans, int(math.Abs(float64(180-sum))*2))
	}
	return ans
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{4, 4, 5, 5, 13, 14, 14, 16, 19, 20, 30, 31, 32, 33, 35, 38, 38, 42, 44, 44, 48, 48, 52, 58, 60, 64, 65, 66, 68, 69, 70, 70, 71, 72, 73, 79, 81, 83, 83, 84, 86, 87, 88, 88, 91, 92, 95, 95, 98}
		param0_1  []int  = []int{-56, 88, -50, 70, 20, 58, 42, -56, -52, -78, 98, 20, -26, 4, 20, -66, -46, -58, 74, 74, -72, 2, 16, -78, -4, 10, 58, 60, -46, -2, 32, -96, 24, -6, 90, -64, -24, -38, 26, 66, -42, -86, 48, 92, 28, 6, -54, -6}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{52, 67, 62}
		param0_4  []int   = []int{-56, -22, 32, 42, 66}
		param0_5  []int  = []int{1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0}
		param0_6  []int   = []int{38, 46, 58, 72}
		param0_7  []int  = []int{16, 62, 90, 40, 30, -56, -92, -56, 60, 42, -64, 92, -30, -70, 42, -48, -54, 54, 48, 94, -44, -46, 10, 48, 22, -24, -62, 34, 60, 24, -60, 50, 40, 34}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{86, 43, 74, 84, 86, 14, 45, 7, 92, 36, 79, 13, 67, 18, 96, 77, 13, 22, 28, 36, 57, 56, 99, 57, 8, 48, 5, 79, 65, 64, 96, 6, 36, 91, 53, 55, 11, 12, 80, 99, 50, 40, 4, 9, 52, 41}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{27, 29, 25, 1, 4, 10, 2, 20, 37, 40}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
