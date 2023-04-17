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


func f_gold(r1 float32, r2 float32, r3 float32) float32 {
	var pi float32 = 3.14
	return float32(float64(pi) * 1.33 * float64(r1) * float64(r2) * float64(r3))
}
//TOFILL
func main() {
	var (
		n_success int         = 0
		param0    []float32 = []float32{3287.4842316041018, -3707.427510963942, 8980.643174783816, -2698.0187368852694, 8627.156664162168, -7316.329924623669, 7857.3846206400485, -6502.657905007728, 4468.400513325576, -7231.864791620428}
		param1    []float32 = []float32{4503.332888443404, -6671.335781753231, 3584.781688607942, -1004.7289573934537, 9572.27618966978, -6591.043206581106, 3671.761679299217, -1412.2240121470609, 2272.1999139470304, -8036.087711033032}
		param2    []float32 = []float32{8590.24729914204, -2780.4954870801926, 2818.469507143102, -9602.530725071243, 4783.930377855004, -9760.465488363216, 2534.5825334137794, -6135.238350044512, 4753.075799180736, -6456.263512521035}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i], param1[i], param2[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i], param1[i], param2[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
