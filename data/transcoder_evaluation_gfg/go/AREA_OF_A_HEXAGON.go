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


func f_gold(s float64) float64 {
	return (math.Sqrt(3) * 3 * (s * s)) / 2
}
//TOFILL
func main() {
	var (
		n_success int         = 0
		param0    []float64 = []float64{1772.6589509256596, -599.737107809315, 1074.1765931782, -1182.4087746714795, 8083.035797247716, -6126.414356565494, 5370.057504189614, -6947.020794285176, 2110.5107873533325, -6458.751326919488}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
