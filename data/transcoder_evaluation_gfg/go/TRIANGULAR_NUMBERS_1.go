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


func f_gold(num int) bool {
	if num < 0 {
		return false
	}
	var c int = (num * (-2))
	var b int = 1
	var a int = 1
	var d int = (b * b) - a*4*c
	if d < 0 {
		return false
	}
	var root1 float32 = float32((float64(-b) + math.Sqrt(float64(d))) / float64(a*2))
	var root2 float32 = float32((float64(-b) - math.Sqrt(float64(d))) / float64(a*2))
	if root1 > 0 && math.Floor(float64(root1)) == float64(root1) {
		return true
	}
	if root2 > 0 && math.Floor(float64(root2)) == float64(root2) {
		return true
	}
	return false
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{1, 3, 6, 10, 55, 48, 63, 72, 16, 85}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
