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
	var (
		pPrevPrev int = 1
		pPrev     int = 1
		pCurr     int = 1
		pNext     int = 1
	)
	for i := int(3); i <= n; i++ {
		pNext = pPrevPrev + pPrev
		pPrevPrev = pPrev
		pPrev = pCurr
		pCurr = pNext
	}
	return pNext
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{1, 92, 29, 52, 55, 13, 83, 83, 10, 67}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
