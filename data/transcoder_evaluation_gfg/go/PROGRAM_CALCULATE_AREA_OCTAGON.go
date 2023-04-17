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


func f_gold(side float64) float64 {
	return float64(float32((math.Sqrt(2) + 1) * 2 * side * side))
}
//TOFILL
func main() {
	var (
		n_success int         = 0
		param0    []float64 = []float64{5859.798616323926, -6381.210375893524, 2442.246292006922, -9624.81536339737, 8679.436805247444, -2682.3245401089525, 7216.9161613024435, -5881.789859815442, 2497.776395789202, -9598.912195459263}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
