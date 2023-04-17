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


func f_gold(a int, b int) int {
	if a == b {
		return a
	}
	if a == 0 {
		return b
	}
	if b == 0 {
		return a
	}
	if ^a&1 != 0 {
		if b&1 != 0 {
			return f_gold(a>>1, b)
		} else {
			return f_gold(a>>1, b>>1) << 1
		}
	}
	if ^b&1 != 0 {
		return f_gold(a, b>>1)
	}
	if a > b {
		return f_gold((a-b)>>1, b)
	}
	return f_gold((b-a)>>1, a)
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{52, 36, 12, 69, 45, 7, 45, 62, 96, 89}
		param1    []int = []int{29, 94, 6, 7, 11, 51, 55, 86, 63, 12}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
