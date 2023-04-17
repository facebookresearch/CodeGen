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


func f_gold(num int) bool {
	if num/10 == 0 {
		return true
	}
	for num != 0 {
		if num/10 == 0 {
			return true
		}
		var digit1 int = num % 10
		var digit2 int = (num / 10) % 10
		if math.Abs(float64(digit2-digit1)) > 1 {
			return false
		}
		num = num / 10
	}
	return true
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{67, 77, 35, 79, 45, 22, 68, 17, 5, 85}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
