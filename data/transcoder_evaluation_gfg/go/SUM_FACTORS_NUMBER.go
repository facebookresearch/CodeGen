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


func f_gold(n int) int {
	var result int = 0
	for i := int(2); float64(i) <= math.Sqrt(float64(n)); i++ {
		if n%i == 0 {
			if i == (n / i) {
				result += i
			} else {
				result += i + n/i
			}
		}
	}
	return result + n + 1
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{76, 21, 4, 49, 35, 55, 43, 39, 36, 5}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
