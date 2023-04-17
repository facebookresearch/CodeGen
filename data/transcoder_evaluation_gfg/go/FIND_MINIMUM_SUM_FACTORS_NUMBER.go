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


func f_gold(num int) int {
	var sum int = 0
	for i := int(2); i*i <= num; i++ {
		for num%i == 0 {
			sum += i
			num /= i
		}
	}
	sum += num
	return sum
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{83, 88, 60, 6, 26, 98, 38, 90, 76, 66}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
