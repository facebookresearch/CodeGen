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


func f_gold(n int) int {
	if n < 3 {
		return n
	}
	if n >= 3 && n < 10 {
		return n - 1
	}
	var po int = 1
	for n/po > 9 {
		po = po * 10
	}
	var msd int = n / po
	if msd != 3 {
		return f_gold(msd)*f_gold(po-1) + f_gold(msd) + f_gold(n%po)
	} else {
		return f_gold(msd*po - 1)
	}
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{85, 86, 3, 35, 59, 38, 33, 15, 75, 74}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
