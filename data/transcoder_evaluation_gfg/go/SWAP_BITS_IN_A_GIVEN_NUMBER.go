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


func f_gold(x uint, p1 uint, p2 uint, n uint) int {
	var (
		set1 uint = (x >> p1) & ((1 << n) - 1)
		set2 uint = (x >> p2) & ((1 << n) - 1)
		Xor  uint = (set1 ^ set2)
	)
	Xor = (Xor << p1) | Xor<<p2
	var result uint = x ^ Xor
	return int(result)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{95, 16, 55, 75, 90, 58, 69, 5, 36, 62}
		param1    []int = []int{88, 26, 56, 35, 12, 65, 64, 1, 33, 69}
		param2    []int = []int{97, 59, 40, 79, 59, 25, 17, 59, 97, 66}
		param3    []int = []int{92, 42, 41, 30, 34, 19, 94, 38, 44, 9}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(uint(param0[i]), uint(param1[i]), uint(param2[i]), uint(param3[i])) == f_gold(uint(param0[i]), uint(param1[i]), uint(param2[i]), uint(param3[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
