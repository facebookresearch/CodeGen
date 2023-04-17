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


func f_gold(n uint) uint {
	var count uint = 0
	if n != 0 && (n&(n-1)) == 0 {
		return n
	}
	for n != 0 {
		n >>= 1
		count += 1
	}
	return 1 << count
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{74, 70, 85, 78, 71, 32, 97, 90, 64, 48}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(uint(param0[i])) == f_gold(uint(param0[i])) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
