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


func f_gold(a float64, b float64) float64 {
	var mod float64
	if a < 0 {
		mod = -a
	} else {
		mod = a
	}
	if b < 0 {
		b = -b
	}
	for mod >= b {
		mod = mod - b
	}
	if a < 0 {
		return -mod
	}
	return mod
}
//TOFILL
func main() {
	var (
		n_success int         = 0
		param0    []float64 = []float64{3243.229719038493, -4362.665881044217, 7255.066257575837, -6929.554320261099, 3569.942027998315, -6513.849053096595, 7333.183189243961, -2856.1752826258803, 9787.228111241662, -1722.873699288031}
		param1    []float64 = []float64{5659.926861939672, -9196.507113304497, 2623.200060506935, -3009.0234530313287, 6920.809419868375, -70.95992406437102, 580.3500610971768, -9625.97442825802, 2419.6844962423256, -8370.700544254058}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i], param1[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i], param1[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
