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


func f_gold(arr []int, n int, x int) bool {
	var i int
	for i = 0; i < n-1; i++ {
		if arr[i] > arr[i+1] {
			break
		}
	}
	var l int = (i + 1) % n
	var r int = i
	for l != r {
		if arr[l]+arr[r] == x {
			return true
		}
		if arr[l]+arr[r] < x {
			l = (l + 1) % n
		} else {
			r = (n + r - 1) % n
		}
	}
	return false
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{3, 8, 10, 15, 18, 19, 20, 20, 21, 22, 26, 30, 32, 34, 43, 45, 50, 50, 51, 52, 53, 56, 57, 58, 62, 63, 65, 82, 86, 91, 91, 92, 92, 93, 97}
		param0_1  []int  = []int{30, -34, 86, -30, -26, 2, 90, 8, 26, -8, -8, 0, -86, 68, 22, 72, -76, 48, -24, 90, -22, -58, -54, 90, -12, -12, 88, 72, -58, 68, 84, 22, 60, 66, -52, -38, -90, 62, 30, -26, 88, -36, 92, 32, -32, -42, -90, -40, -10}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int   = []int{20, 68, 40, 19, 74, 69}
		param0_4  []int  = []int{-98, -94, -94, -94, -90, -88, -88, -78, -74, -70, -68, -66, -64, -62, -54, -50, -40, -40, -40, -40, -28, -22, -22, -18, -14, -12, 0, 6, 6, 8, 12, 20, 22, 26, 28, 36, 42, 44, 48, 52, 56, 60, 68, 84}
		param0_5  []int   = []int{1, 1, 0}
		param0_6  []int   = []int{12, 22, 38, 76, 80, 86}
		param0_7  []int  = []int{-36, -10, -26, 34, -50, 66, -2, -14, -62, 60, -48, 94, -70, 6, -60, -90, 28, -4, -20, -52, 40, -76, -92, -14, 54, 4, -58, 38, -74, -96, -88, 86, -54, 98, 48, 68, 78, -28, -80, -46}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{69, 99, 25, 52, 41, 51, 7, 33, 42, 91, 85, 57, 91, 89, 86, 11, 70, 67, 30, 92, 81, 23, 51, 98, 85, 5, 50, 44}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{17, 41, 26, 4, 28, 2, 4, 26, 17, 21}
		param2    []int  = []int{30, 10, 1, 88, -94, 60, 3, 37, 20, 27}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
