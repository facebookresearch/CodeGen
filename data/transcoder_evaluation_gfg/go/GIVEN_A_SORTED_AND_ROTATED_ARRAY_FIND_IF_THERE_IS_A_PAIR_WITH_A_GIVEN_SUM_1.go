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


func f_gold(arr []int, n int, x int) int {
	var i int
	for i = 0; i < n-1; i++ {
		if arr[i] > arr[i+1] {
			break
		}
	}
	var l int = (i + 1) % n
	var r int = i
	var cnt int = 0
	for l != r {
		if arr[l]+arr[r] == x {
			cnt++
			if l == (r-1+n)%n {
				return cnt
			}
			l = (l + 1) % n
			r = (r - 1 + n) % n
		} else if arr[l]+arr[r] < x {
			l = (l + 1) % n
		} else {
			r = (n + r - 1) % n
		}
	}
	return cnt
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{24, 54}
		param0_1  []int  = []int{68, -30, -18, -6, 70, -40, 86, 98, -24, -48}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{84, 44, 40, 45, 2, 41, 52, 17, 50, 41, 5, 52, 48, 90, 13, 55, 34, 55, 94, 44, 41, 2}
		param0_4  []int  = []int{-92, -76, -74, -72, -68, -64, -58, -44, -44, -38, -26, -24, -20, -12, -8, -8, -4, 10, 10, 10, 20, 20, 26, 26, 28, 50, 52, 54, 60, 66, 72, 74, 78, 78, 78, 80, 86, 88}
		param0_5  []int  = []int{1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1}
		param0_6  []int  = []int{5, 5, 15, 19, 22, 24, 26, 27, 28, 32, 37, 39, 40, 43, 49, 52, 55, 56, 58, 58, 59, 62, 67, 68, 77, 79, 79, 80, 81, 87, 95, 95, 96, 98, 98}
		param0_7  []int  = []int{-98, 28, 54, 44, -98, -70, 48, -98, 56, 4, -18, 26, -8, -58, 30, 82, 4, -38, 42, 64, -28}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{26, 72, 74, 86, 98, 86, 22, 6, 95, 36, 11, 82, 34, 3, 50, 36, 81, 94, 55, 30, 62, 53, 50, 95, 32, 83, 9, 16}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{1, 8, 33, 18, 29, 19, 28, 17, 24, 19}
		param2    []int  = []int{1, 8, 28, 16, 30, 10, 34, 14, 24, 16}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
