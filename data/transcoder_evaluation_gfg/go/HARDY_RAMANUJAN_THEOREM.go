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
	var count int = 0
	if n%2 == 0 {
		count++
		for n%2 == 0 {
			n = n / 2
		}
	}
	for i := int(3); float64(i) <= math.Sqrt(float64(n)); i = i + 2 {
		if n%i == 0 {
			count++
			for n%i == 0 {
				n = n / i
			}
		}
	}
	if n > 2 {
		count++
	}
	return count
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{99, 33, 50, 17, 18, 69, 23, 18, 94, 16}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
