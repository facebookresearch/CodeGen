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
	if n == 1 {
		return 1
	}
	var z int
	var e float32 = 2.71
	z = int(math.Sqrt(float64(n)*(2*3.14)) * math.Pow(float64(float32(n)/e), float64(n)))
	return z
}
//TOFILL
func main() {
	var (
		n_success int         = 0
		param0    []float64 = []float64{1.0, 5.0, 10.0, 20.0, 40.0, 2.0, 3.0, -1.0, 4663.43115050185, -3722.039522409859}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(int(param0[i])) == f_gold(int(param0[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
