package main

import (
	"math"
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


func f_gold(n int) float64 {
	var (
		i    int     = 1
		res  float64 = 0.0
		sign bool    = true
	)
	for n > 0 {
		n--
		if sign {
			sign = !sign
			res = res + float64(func() int {
				p := &i
				*p++
				return *p
			}())/float64(func() int {
				p := &i
				*p++
				return *p
			}())
		} else {
			sign = !sign
			res = res - float64(func() int {
				p := &i
				*p++
				return *p
			}())/float64(func() int {
				p := &i
				*p++
				return *p
			}())
		}
	}
	return res
}
//TOFILL
func main() {
	var (
		n_success int     = 0
		param0    []int = []int{49, 4, 60, 90, 96, 29, 86, 47, 77, 87}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
