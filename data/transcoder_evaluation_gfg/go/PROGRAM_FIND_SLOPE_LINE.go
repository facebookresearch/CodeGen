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


func f_gold(x1 float32, y1 float32, x2 float32, y2 float32) float32 {
	return (y2 - y1) / (x2 - x1)
}
//TOFILL
func main() {
	var (
		n_success int         = 0
		param0    []float32 = []float32{236.27324548309292, -9201.144918204123, 3480.4716834445326, -6915.538971485092, 8887.97173657486, -3785.5177159369946, 3037.6696554256832, -7925.458496016523, 1404.2919985268031, -4748.744241168378}
		param1    []float32 = []float32{5792.493225762838, -2716.3347716140406, 3577.9608612055613, -4113.601103381095, 1678.4080012662428, -3084.67461899163, 4432.445827549, -3350.27411882042, 8971.636233373416, -675.557388148954}
		param2    []float32 = []float32{7177.837879115863, -5161.142121227645, 8611.515262945342, -748.3462104020822, 8709.574949883017, -7415.76208254121, 8387.304165588026, -5619.767086756504, 3039.112051378511, -5998.241086029875}
		param3    []float32 = []float32{1289.5700425822731, -3205.784279961129, 6744.864707668983, -9245.271700539257, 8548.492675510739, -887.5389305564152, 611.3373507518394, -1185.7423219907591, 1947.6756252708972, -4236.658178504375}
	)
	for i := int(0); i < len(param0[:]); i++ {
		if float64(math.Abs(float64(1-(float64(math.Abs(float64(f_gold(param0[i], param1[i], param2[i], param3[i]))))+1e-07)/(float64(math.Abs(float64(f_filled(param0[i], param1[i], param2[i], param3[i]))))+1e-07)))) < 0.001 {
			n_success += 1
		}
	}
	fmt.Print("#Results:", " ", n_success, ", ", len(param0[:]))
	os.Exit(0)
}
