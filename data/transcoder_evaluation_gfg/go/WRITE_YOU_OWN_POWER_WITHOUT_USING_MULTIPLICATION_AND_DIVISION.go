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
	if b == 0 {
		return 1
	}
	var answer int = a
	var increment int = a
	var i int
	var j int
	for i = 1; i < b; i++ {
		for j = 1; j < a; j++ {
			answer += increment
		}
		increment = answer
	}
	return answer
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{66, 82, 12, 55, 34, 22, 13, 57, 76, 76}
		param1    []int = []int{4, 66, 38, 33, 26, 23, 98, 84, 94, 95}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i], param1[i]) == f_gold(param0[i], param1[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
