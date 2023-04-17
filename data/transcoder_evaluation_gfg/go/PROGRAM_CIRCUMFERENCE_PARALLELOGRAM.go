package main

import (
	"math"
		"fmt"
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


func f_gold(a float32, b float32) float32 {
	return (a * 2) + b*2
}
//TOFILL
func main() {
	var (
		n_success int         = 0
		param0    []float32 = []float32{801.0366882228715, -7069.610056819919, 7723.966966568705, -7935.859205856963, 6094.247432557289, -7371.490363309265, 8368.473889617526, -3761.921143166053, 3139.1089185587884, -5218.286665567171}
		param1    []float32 = []float32{456.71190645582783, -4226.483870778477, 5894.65405158763, -5333.225064296693, 1660.420120702062, -1095.4543576847332, 4735.838330834498, -5315.871691690649, 6490.194159517967, -8265.153014320813}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i], param1[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i], param1[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
