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


func f_gold(input int, unlock_code int) int {
	var (
		rotation    int = 0
		input_digit int
		code_digit  int
	)
	for input != 0 || unlock_code != 0 {
		input_digit = input % 10
		code_digit = unlock_code % 10
		rotation += min(int(math.Abs(float64(input_digit-code_digit))), int(10-math.Abs(float64(input_digit-code_digit))))
		input /= 10
		unlock_code /= 10
	}
	return rotation
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{71, 90, 28, 41, 32, 39, 33, 89, 50, 92}
		param1    []int = []int{46, 65, 84, 23, 58, 82, 58, 32, 51, 77}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
