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


func f_gold(n uint) bool {
	var count int = 0
	if n != 0 && (n&(n-1)) == 0 {
		for n > 1 {
			n >>= 1
			count += 1
		}
		if count%2 == 0 {
			return true
		}
		return false
	}
	return false
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{1, 4, 64, -64, 128, 1024, 45, 33, 66, 74}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(uint(param0[i])) == f_gold(uint(param0[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
