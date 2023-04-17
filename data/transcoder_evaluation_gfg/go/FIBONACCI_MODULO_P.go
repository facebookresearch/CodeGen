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


func f_gold(p int) int {
	var (
		first  int = 1
		second int = 1
		number int = 2
		next   int = 1
	)
	for next != 0 {
		next = (first + second) % p
		first = second
		second = next
		number++
	}
	return number
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{51, 40, 68, 7, 8, 32, 93, 75, 71, 15}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
