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


func f_gold(h float64, m float64) int {
	if h < 0 || m < 0 || h > 12 || m > 60 {
		fmt.Print("Wrong input")
	}
	if h == 12 {
		h = 0
	}
	if m == 60 {
		m = 0
	}
	var hour_angle int = int((h*60 + m) * 0.5)
	var minute_angle int = int(m * 6)
	var angle int = int(math.Abs(float64(hour_angle - minute_angle)))
	angle = min(360-angle, angle)
	return angle
}
//TOFILL
func main() {
	var (
		n_success int         = 0
		param0    []float64 = []float64{7322.337365895532, -0.5025472034247969, 8735.336068205026, -5478.862697905712, 8264.126919165505, -9671.311773842834, 9995.328351000411, -5274.574323066984, 1310.8711644223736, -2829.678131972794}
		param1    []float64 = []float64{6996.326968156217, -2910.070017192333, 1910.3752934680874, -9470.18148108585, 7058.937313484608, -3867.070379361206, 2145.339179488316, -3583.7503371694124, 5214.059687285893, -9371.556600288217}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
