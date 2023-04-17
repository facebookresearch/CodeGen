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


func f_gold(l float32, b float32, h float32) float32 {
	var volume float32 = (l * b * h) / 2
	return volume
}
//TOFILL
func main() {
	var (
		n_success int         = 0
		param0    []float32 = []float32{8448.900678262902, -1849.728957491451, 412.667844022232, -5954.835911765373, 8437.913444665008, -7183.181663518317, 2340.7905920227954, -7281.157547371143, 471.3930826982504, -7550.426360065503}
		param1    []float32 = []float32{8135.461799983198, -4240.89241631363, 9798.083992381831, -661.8872499003203, 8182.675681595904, -6846.746446198541, 5479.00956987109, -615.8705455524116, 1357.3753126091392, -2693.2262997056355}
		param2    []float32 = []float32{6577.239053611328, -9953.518310747193, 1449.9204200270522, -8049.6051526695055, 9863.296545513396, -971.2199894221352, 7073.449591910562, -3343.0245192607968, 1907.815700915636, -9110.64755244532}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i], param1[i], param2[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i], param1[i], param2[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
