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


func f_gold(A []int, arr_size int, sum int) bool {
	var (
		l int
		r int
	)
	sort.Ints(A)
	for i := int(0); i < arr_size-2; i++ {
		l = i + 1
		r = arr_size - 1
		for l < r {
			if A[i]+A[l]+A[r] == sum {
				fmt.Print("Triplet is %d, %d, %d", A[i], A[l], A[r])
				return true
			} else if A[i]+A[l]+A[r] < sum {
				l++
			} else {
				r--
			}
		}
	}
	return false
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int   = []int{28, 47, 65, 89}
		param0_1  []int  = []int{-26, -64, -2, 96, -52, -14, -56, 52, -70, 70, -64, 74, -8, 18, 78, 14, 6, -16, 50, 84, -90, 12, -88, 52, 52, -40, 58, -48, 98, -66, 46, -88, 68, 12, 0, 70, -42}
		param0_2  []int   = []int{}
		param0_3  []int   = []int{49, 66, 22, 93, 52, 54, 80, 87}
		param0_4  []int  = []int{-96, -92, -86, -74, -62, -60, -56, -54, -46, -38, -32, -26, -16, -16, -8, -4, 0, 6, 20, 28, 42, 44, 56}
		param0_5  []int  = []int{1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1}
		param0_6  []int  = []int{1, 2, 16, 16, 20, 24, 24, 38, 41, 54, 57, 72, 79, 83, 89, 90, 96, 97, 98}
		param0_7  []int   = []int{52, 22, 78, -30}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{72, 40, 92, 11, 98, 20, 4, 58, 49, 11, 58, 28, 16, 16, 44, 10, 50, 23, 83, 41, 41, 92, 1, 28, 26, 83, 6, 52, 48, 9, 77, 51}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{3, 22, 0, 5, 13, 39, 12, 2, 21, 29}
		param2    []int  = []int{3, 24, 0, 7, 19, 39, 12, 3, 16, 27}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
