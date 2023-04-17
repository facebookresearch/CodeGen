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
	if n%2 != 0 {
		return 0
	}
	var res int = 1
	for i := int(2); float64(i) <= math.Sqrt(float64(n)); i++ {
		var (
			count     int = 0
			curr_sum  int = 1
			curr_term int = 1
		)
		for n%i == 0 {
			count++
			n = n / i
			if i == 2 && count == 1 {
				curr_sum = 0
			}
			curr_term *= i
			curr_sum += curr_term
		}
		res *= curr_sum
	}
	if n >= 2 {
		res *= n + 1
	}
	return res
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{71, 78, 39, 36, 49, 17, 53, 66, 92, 71}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
