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
	return math.Sqrt(3) * 2 * (side * side)
}
//TOFILL
func main() {
	var (
		n_success int         = 0
		param0    []float64 = []float64{1449.255716877097, -8772.104874265995, 2948.419328234334, -1184.220109553511, 7422.825800698956, -5808.280006171851, 829.8963781665169, -7368.438572511732, 5572.033890611617, -3998.9441642787706}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
