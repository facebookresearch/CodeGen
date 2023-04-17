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
	return (side * side * side) * (math.Sqrt(2) / 3)
}
//TOFILL
func main() {
	var (
		n_success int         = 0
		param0    []float64 = []float64{3355.322051344013, -891.0551553192736, 8242.699647177868, -9259.146104439229, 7712.806145993083, -4998.858862079315, 9771.127582524628, -5415.8106399098115, 670.0774772280249, -7068.634369272122}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
