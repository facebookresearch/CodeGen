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
		l  int = int(math.Sqrt(float64(n)))
		sq int = l * l
	)
	if sq == n {
		return l * 4
	} else {
		var (
			row       float64 = float64(n / l)
			perimeter float64 = float64((l + int(row)) * 2)
		)
		if n%l != 0 {
			perimeter += 2
		}
		return int(perimeter)
	}
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{45, 80, 54, 48, 83, 68, 32, 20, 68, 66}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
