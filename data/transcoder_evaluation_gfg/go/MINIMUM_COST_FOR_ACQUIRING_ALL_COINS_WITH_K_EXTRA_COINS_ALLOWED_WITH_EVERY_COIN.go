package main

import (
		"fmt"
"sort"
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


func f_gold(coin []int, n int, k int) int {
	sort.Ints(coin)
	var coins_needed int = int(math.Ceil(float64(n) * 1.0 / float64(k+1)))
	var ans int = 0
	for i := int(0); i <= coins_needed-1; i++ {
		ans += coin[i]
	}
	return ans
}
//TOFILL
func main() {
	var (
		n_success int      = 0
		param0_0  []int  = []int{2, 4, 5, 9, 10, 10, 11, 14, 15, 19, 21, 22, 29, 36, 36, 38, 39, 39, 39, 41, 41, 42, 45, 45, 48, 55, 56, 57, 64, 66, 66, 66, 66, 69, 74, 76, 80, 81, 82, 82, 85, 87, 95, 95}
		param0_1  []int  = []int{-6, -52, 20, -98, -10, 48, 36, 66, -88, 94, 68, 16}
		param0_2  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_3  []int  = []int{91, 62, 29, 49, 6, 11, 10, 43, 78, 35, 32, 5, 1, 48, 15, 24, 4, 71}
		param0_4  []int  = []int{-98, -92, -88, -84, -82, -78, -74, -74, -68, -62, -62, -56, -56, -50, -46, -44, -26, -18, -14, -8, -8, -6, 8, 16, 20, 20, 22, 26, 36, 42, 44, 44, 52, 60, 66, 68, 68, 70, 76, 84}
		param0_5  []int  = []int{1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0}
		param0_6  []int  = []int{5, 12, 38, 39, 52, 54, 62, 81, 87, 93}
		param0_7  []int  = []int{86, -18, -32, 70, 40, -76, -8, 8, -84, -10, 92, 94, -18, -12, -26, -40, -74, 60, 16, -70, 44, -32, 40, -24, 0, 4}
		param0_8  []int  = []int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}
		param0_9  []int  = []int{86, 62, 98, 97, 61, 31, 23, 56, 63, 72, 44, 74, 58, 97}
		param0    [][]int = [][]int{param0_0, param0_1, param0_2, param0_3, param0_4, param0_5, param0_6, param0_7, param0_8, param0_9}
		param1    []int  = []int{33, 6, 16, 13, 25, 32, 6, 25, 37, 12}
		param2    []int  = []int{27, 10, 16, 17, 34, 32, 8, 20, 29, 13}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(([]int)(param0[i]), param1[i], param2[i]) == f_gold(([]int)(param0[i]), param1[i], param2[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
