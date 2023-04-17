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


func f_gold(arr []int, n int, x int, k int) int {
	var i int = 0
	for i < n {
		if arr[i] == x {
			return i
		}
		i = i + max(1, int(math.Abs(float64(arr[i]-x))/float64(k)))
	}
	fmt.Print("number is not present!")
	return -1
}
//TOFILL
func main() {
	var n_success int = 0
	_ = n_success
	var param0_0 []int = []int{1, 5, 9, 11, 14, 18, 19, 21, 26, 32, 38, 38, 43, 47, 49, 52, 55, 61, 65, 67, 69, 73, 74, 79, 84, 90, 91, 91, 92, 93, 94, 99}
	var param0_1 []int = []int{12, -86, -66, -50, -48, 78, -92, -56, -2, 66, 64}
	var param0_2 []int = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
	var param0_3 []int = []int{10, 87, 39, 87, 45, 33, 5, 37, 70, 69, 88, 78, 90, 3}
	var param0_4 []int = []int{-78, -70, -68, -60, -52, -34, -24, -4, 12, 18, 58, 58, 64, 76, 84, 94}
	var param0_5 []int = []int{0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0}
	var param0_6 []int = []int{5, 5, 7, 11, 11, 15, 22, 23, 28, 38, 41, 53, 54, 57, 59, 68, 71, 89}
	var param0_7 []int = []int{-4, 0, 60, -14, -48, 54, -96, -68, -40, 64, -50, -74, -20, -22, 48, -48, 42, 62, 66, 84, 54, -52, -52, 6, 46, -90, -18, 90}
	var param0_8 []int = []int{0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1}
	var param0_9 []int = []int{30, 91, 34, 44, 3, 76, 43, 75, 49, 33, 74, 72, 68, 79, 26, 62, 23, 5, 32, 75, 82, 25, 7, 19, 32, 87, 87, 94, 34, 62, 3, 32, 59}
	var param0 [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
	var param1 []int = []int{22, 5, 35, 9, 14, 26, 16, 18, 9, 32}
	var param2 []int = []int{19, 10, 37, 8, 9, 36, 17, 14, 8, 30}
	var param3 []int = []int{26, 5, 43, 10, 13, 32, 16, 23, 9, 24}
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i], param3[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i], param3[i]) {
			n_success += 1
		}
	}
	fmt.Print("number is not present!")
	os.Exit(0)
}
