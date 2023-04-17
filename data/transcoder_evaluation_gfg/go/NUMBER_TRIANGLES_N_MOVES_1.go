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
	var ans int = int(math.Pow(3, float64(n))*2 - 1)
	return ans
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{78, 89, 46, 56, 79, 71, 80, 77, 48, 16}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
