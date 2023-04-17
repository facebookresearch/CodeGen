// Copyright (c) 2019-present, Facebook, Inc.
// All rights reserved.
//
// This source code is licensed under the license found in the
// LICENSE file in the root directory of this source tree.
//


#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <limits.h>
#include <stdbool.h>

int min(int x, int y) { return (x < y)? x: y; }
int max(int x, int y) { return (x > y)? x: y; }
int cmpfunc (const void * a, const void * b) {return ( *(int*)a - *(int*)b );}
int len (int arr [ ]) {return ((int) (sizeof (arr) / sizeof (arr)[0]));}
void sort (int arr [ ], int n) {qsort (arr, n, sizeof(int), cmpfunc);}

float f_gold ( float r1, float r2, float r3 ) {
  float pi = 3.14;
  return 1.33 * pi * r1 * r2 * r3;
}


float f_filled ( float r1, float r2, float r3 ) {}

int main(void) {
    int n_success = 0;
    float param0[] = {3287.4842316041018F,-3707.427510963942F,8980.643174783816F,-2698.0187368852694F,8627.156664162168F,-7316.329924623669F,7857.3846206400485F,-6502.657905007728F,4468.400513325576F,-7231.864791620428F};
    float param1[] = {4503.332888443404F,-6671.335781753231F,3584.781688607942F,-1004.7289573934537F,9572.27618966978F,-6591.043206581106F,3671.761679299217F,-1412.2240121470609F,2272.1999139470304F,-8036.087711033032F};
    float param2[] = {8590.24729914204F,-2780.4954870801926F,2818.469507143102F,-9602.530725071243F,4783.930377855004F,-9760.465488363216F,2534.5825334137794F,-6135.238350044512F,4753.075799180736F,-6456.263512521035F};
    for(int i = 0; i < len(param0); ++i)
    {
        if(abs(1 - (0.0000001 + abs(f_gold(param0[i],param1[i],param2[i])) )/ (abs(f_filled(param0[i],param1[i],param2[i])) + 0.0000001)) < 0.001F)
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}