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


func f_gold(p float64) int {
	return int(math.Ceil(math.Sqrt(math.Log(1/(1-p)) * (2 * 365))))
}
//TOFILL
func main() {
	var (
		n_success int         = 0
		param0    []float64 = []float64{0.9303713975220878, 0.48126843587453594, 0.4877678952475791, 0.3518440592733779, 0.8000415444743662, 0.3528645948885943, 0.33594265260473666, 0.3603861267753616, 7218.247044923335, -4701.904717953173}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
