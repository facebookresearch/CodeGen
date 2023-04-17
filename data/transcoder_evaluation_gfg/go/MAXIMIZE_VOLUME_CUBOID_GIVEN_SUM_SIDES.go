package main

import (
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


func f_gold(s int) int {
	var maxvalue int = 0
	for i := int(1); i <= s-2; i++ {
		for j := int(1); j <= s-1; j++ {
			var k int = s - i - j
			maxvalue = max(maxvalue, i*j*k)
		}
	}
	return maxvalue
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{67, 48, 59, 22, 14, 66, 1, 75, 58, 78}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
