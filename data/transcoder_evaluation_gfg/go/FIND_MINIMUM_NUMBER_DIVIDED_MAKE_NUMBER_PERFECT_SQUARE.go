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
	var (
		count int = 0
		ans   int = 1
	)
	for n%2 == 0 {
		count++
		n /= 2
	}
	if count%2 != 0 {
		ans *= 2
	}
	for i := int(3); float64(i) <= math.Sqrt(float64(n)); i += 2 {
		count = 0
		for n%i == 0 {
			count++
			n /= i
		}
		if count%2 != 0 {
			ans *= i
		}
	}
	if n > 2 {
		ans *= n
	}
	return ans
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{95, 48, 3, 10, 82, 1, 77, 99, 23, 61}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
