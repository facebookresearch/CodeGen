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

int f_gold ( int arr [ ], int n ) {
  int ones = 0, twos = 0;
  int common_bit_mask;
  for ( int i = 0;
  i < n;
  i ++ ) {
    twos = twos | ( ones & arr [ i ] );
    ones = ones ^ arr [ i ];
    common_bit_mask = ~ ( ones & twos );
    ones &= common_bit_mask;
    twos &= common_bit_mask;
  }
  return ones;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {7,26,26,48,59,62,66,70,72,75,76,81,97,98};
int param0_1[] = {-42,-48,-64,-74,56,-34,20,16,34,-84,86,38,56,-86,30,-74,-96,96,12,10,-46,10,-36,38,34,-46,-20,14,12,62,-54,20,-82,24,96};
int param0_2[] = {0,0,1,1};
int param0_3[] = {68,91,61,6,32,47,76,69,44,71,29,79,74,33,44,33,45,75,43,82,83,81,95,16,86,33,69,61,73,21,54,17,98,62,14,72,80,31,56,82,14,48,76};
int param0_4[] = {-98,-96,-92,-62,-52,-42,-42,-26,4,10,14,38,64,66,72,74,82};
int param0_5[] = {0,1,1,1,0,0,0,1,0,1};
int param0_6[] = {53,63,63};
int param0_7[] = {-96,-38,-26,-46,68,-36,20,-18,-10,52,40,94,-8,-64,82,-22};
int param0_8[] = {0,0,0,0,0,1,1};
int param0_9[] = {99,46,48,81,27,97,26,50,77,32,45,99,46};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {7,27,3,38,14,5,2,15,3,12};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i]) == f_gold(param0[i],param1[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}