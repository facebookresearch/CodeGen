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


func f_gold(n int) int {
	var (
		ans  int = 0
		temp int = 0
		num  int
	)
	for i := int(1); i <= n && temp < n; i++ {
		temp = i - 1
		num = 1
		for temp < n {
			if temp+i <= n {
				ans += i * num
			} else {
				ans += (n - temp) * num
			}
			temp += i
			num++
		}
	}
	return ans
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{35, 93, 7, 81, 80, 47, 7, 41, 59, 34}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
