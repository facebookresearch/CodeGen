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


func f_gold(n int) int {
	var (
		odd_count  int = 0
		even_count int = 0
	)
	if n < 0 {
		n = -n
	}
	if n == 0 {
		return 1
	}
	if n == 1 {
		return 0
	}
	for n != 0 {
		if n&1 != 0 {
			odd_count++
		}
		if n&2 != 0 {
			even_count++
		}
		n = n >> 2
	}
	return f_gold(int(math.Abs(float64(odd_count - even_count))))
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{94, 94, 79, 39, 16, 90, 64, 76, 83, 47}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
