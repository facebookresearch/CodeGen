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


func f_gold(ar1 []int, ar2 []int, n int) int {
	var (
		i     int = 0
		j     int = 0
		count int
		m1    int = -1
		m2    int = -1
	)
	for count = 0; count <= n; count++ {
		if i == n {
			m1 = m2
			m2 = ar2[0]
			break
		} else if j == n {
			m1 = m2
			m2 = ar1[0]
			break
		}
		if ar1[i] < ar2[j] {
			m1 = m2
			m2 = ar1[i]
			i++
		} else {
			m1 = m2
			m2 = ar2[j]
			j++
		}
	}
	return (m1 + m2) / 2
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{2, 6, 18, 21, 23, 27, 44, 44, 69, 72, 78, 88, 90, 98}
		param0_1  []int  = []int{90, 54, 24, -10, -84, -74, 58, 96, -28, -92, -18, 90, 70, -60, 72, 78, 10, 42, -2, -18, -38, -16, 18, -86, 40, -46, -38, 66, 20, -16, 48}
		param0_2  []int   = []int{0, 1, 1}
		param0_3  []int  = []int{53, 17, 94, 21, 16, 75, 67, 51, 44, 71, 65, 82}
		param0_4  []int  = []int{-96, -92, -80, -68, -64, -64, -60, -56, -52, -50, -50, -22, -20, -4, -2, 0, 6, 20, 22, 28, 38, 40, 48, 50, 56, 58, 64, 64, 80, 82, 90, 92, 92, 92}
		param0_5  []int  = []int{0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1}
		param0_6  []int  = []int{8, 15, 17, 19, 21, 32, 34, 38, 41, 41, 49, 49, 51, 54, 54, 56, 56, 57, 59, 63, 70, 74, 79, 79, 84, 84, 86, 88, 89, 93, 98}
		param0_7  []int  = []int{96, -42, -94, -46, -68, 76, 8, 16, -54, -94, 76, 24, 94, 10, 34, 78, -30, 0, -52, 80, 98, -58, 92, 12, 26, 64}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int   = []int{61, 69, 66, 3}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1_0  []int  = []int{6, 12, 16, 18, 26, 34, 48, 48, 49, 56, 61, 79, 81, 89}
		param1_1  []int  = []int{-72, -62, 14, -58, 70, 54, 88, -40, -94, 4, 60, -16, -38, -98, -70, -46, 66, 42, 26, 36, 56, -4, 32, 30, -46, -42, -72, 44, 16, 4, 24}
		param1_2  []int   = []int{0, 1, 1}
		param1_3  []int  = []int{98, 50, 8, 11, 80, 41, 59, 24, 94, 41, 75, 78}
		param1_4  []int  = []int{-88, -72, -72, -58, -54, -50, -48, -34, -24, -14, -14, -14, -10, -6, 4, 12, 16, 18, 26, 30, 32, 34, 40, 46, 52, 54, 58, 62, 62, 72, 82, 82, 92, 98}
		param1_5  []int  = []int{1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1}
		param1_6  []int  = []int{5, 6, 17, 18, 22, 29, 32, 33, 36, 44, 45, 47, 59, 59, 60, 65, 67, 68, 69, 71, 72, 76, 78, 81, 84, 85, 85, 86, 86, 87, 92}
		param1_7  []int  = []int{88, 78, -26, 10, 84, 34, 56, -8, -30, 46, 48, 20, 26, -78, 96, 44, 92, -44, -86, 24, -58, -96, -86, -12, -98, 18}
		param1_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1}
		param1_9  []int   = []int{39, 84, 97, 15}
		param1    [][]int = [][]int{param1_0, param1_1, param1_2, param1_3, param1_4, param1_5, param1_6, param1_7, param1_8, param1_9}
		param2    []int  = []int{12, 16, 2, 10, 25, 40, 29, 17, 17, 3}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), ([]int)(param1[i]), param2[i]) == f_gold(([]int)(param0[i]), ([]int)(param1[i]), param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
