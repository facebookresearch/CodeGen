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


func f_gold(a int, b int) float64 {
	var (
		AM float64
		GM float64
		HM float64
	)
	AM = float64((a + b) / 2)
	GM = math.Sqrt(float64(a * b))
	HM = (GM * GM) / AM
	return HM
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{54, 42, 63, 19, 41, 7, 39, 11, 96, 15}
		param1    []int = []int{83, 56, 12, 76, 50, 26, 42, 64, 81, 54}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i], param1[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i], param1[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
