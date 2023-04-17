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


func f_gold(a float32) float32 {
	var area float32
	area = float32((math.Sqrt((math.Sqrt(5)*2+5)*5) * float64(a) * float64(a)) / 4)
	return area
}
//TOFILL
func main() {
	var (
		n_success int         = 0
		param0    []float32 = []float32{2009.019461888707, -1480.5131394215787, 357.7870347569567, -8040.293697508038, 3821.882657293133, -6840.635072240347, 1623.036598830132, -9714.00706195298, 3916.454769669618, -669.068424712943}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
