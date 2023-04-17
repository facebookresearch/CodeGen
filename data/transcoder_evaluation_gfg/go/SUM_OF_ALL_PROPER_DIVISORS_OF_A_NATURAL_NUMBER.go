package main

import (
		"fmt"
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


func f_gold(num int) int {
	var result int = 0
	for i := int(2); float64(i) <= math.Sqrt(float64(num)); i++ {
		if num%i == 0 {
			if i == (num / i) {
				result += i
			} else {
				result += i + num/i
			}
		}
	}
	return result + 1
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{2, 57, 28, 43, 38, 29, 45, 47, 44, 3}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
