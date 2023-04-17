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


func f_gold(x uint) uint {
	var (
		even_bits uint = x & 0xAAAAAAAA
		odd_bits  uint = x & 0x55555555
	)
	even_bits >>= 1
	odd_bits <<= 1
	return even_bits | odd_bits
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{99, 94, 11, 3, 77, 57, 54, 66, 98, 36}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(uint(param0[i])) == f_gold(uint(param0[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
