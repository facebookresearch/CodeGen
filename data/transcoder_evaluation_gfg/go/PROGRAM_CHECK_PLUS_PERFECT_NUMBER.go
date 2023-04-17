package main

import (
		"fmt"
	"math"
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


func f_gold(x int) bool {
	var (
		temp int = x
		n    int = 0
	)
	for x != 0 {
		x /= 10
		n++
	}
	x = temp
	var sum int = 0
	for x != 0 {
		sum += int(math.Pow(float64(x%10), float64(n)))
		x /= 10
	}
	return sum == temp
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{371, 9474, 85, 35, 54, 17, 97, 63, 12, 43}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if f_filled(param0[i]) == f_gold(param0[i]) {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
