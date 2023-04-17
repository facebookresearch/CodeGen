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
	var (
		sum        int = 0
		maxsize    int = -1
		startindex int
	)
	_ = startindex
	for i := int(0); i < n-1; i++ {
		if arr[i] == 0 {
			sum = -1
		} else {
			sum = 1
		}
		for j := int(i + 1); j < n; j++ {
			if arr[j] == 0 {
				sum += -1
			} else {
				sum += 1
			}
			if sum == 0 && maxsize < j-i+1 {
				maxsize = j - i + 1
				startindex = i
			}
		}
	}
	if maxsize == -1 {
		fmt.Print("No such subarray")
	} else {
		fmt.Print("No such subarray")
	}
	return maxsize
}
//TOFILL
func main() {
	var n_success int = 0
	_ = n_success
	var param0_0 []int = []int{56, 8, 67, 35, 19, 82, 81, 66, 10, 24, 82, 2, 42, 48, 18, 63, 48, 74, 60, 64, 64, 95, 95, 20, 95, 55, 63, 96, 54}
	var param0_1 []int = []int{78, 67, 1, 78, 48, 83, 17, 19, 21, 44, 99, 68, 16, 54, 9}
	var param0_2 []int = []int{3, 69, 97, 21, 12, 67, 45, 53, 77, 70, 26, 43}
	var param0_3 []int = []int{21, 80, 29, 22, 77, 64, 42, 4, 71, 75, 62, 27, 30, 36, 66, 37, 49, 97}
	var param0_4 []int = []int{18, 66, 9, 90, 21, 95, 74, 48, 44, 9, 43, 17}
	var param0_5 []int = []int{42, 41, 87, 3, 64, 25, 96, 55, 99, 57, 32, 64, 10, 75, 69, 95, 11, 36, 15, 2, 78, 70, 14, 54, 11, 28, 55, 47, 27, 85, 47, 62, 97, 68, 44, 70, 12, 27, 36, 85, 76, 91, 17, 75, 83, 34, 32, 89, 55}
	var param0_6 []int = []int{44}
	var param0_7 []int = []int{1, 43, 28, 17, 30, 46, 89, 51, 15, 70, 96, 79, 65, 55, 8}
	var param0_8 []int = []int{25, 91, 68, 4, 35, 49, 33}
	var param0_9 []int = []int{14, 86, 22, 42, 94, 54, 28, 41, 48, 8, 82, 84, 99, 92, 33, 75, 38, 31, 59, 86, 21, 6, 77, 89, 79, 83, 57, 26, 89, 45, 60, 55, 60, 76, 76, 6, 40, 57, 38, 44, 7, 98, 64, 65, 88, 73, 88, 99}
	var param0 [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
	var param1 []int = []int{26, 8, 9, 10, 10, 41, 0, 9, 4, 26}
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i]) == f_gold(([]int)(param0[i]), param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("No such subarray")
	os.Exit(0)
}
