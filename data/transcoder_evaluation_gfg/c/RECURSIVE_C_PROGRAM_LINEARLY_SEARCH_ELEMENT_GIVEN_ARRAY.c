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

int f_gold ( int arr [ ], int l, int r, int x ) {
  if ( r < l ) return - 1;
  if ( arr [ l ] == x ) return l;
  if ( arr [ r ] == x ) return r;
  return f_gold ( arr, l + 1, r - 1, x );
}


int f_filled ( int arr [ ], int l, int r, int x ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {10,74,3};
int param0_1[] = {-90,72,36,96,42,0,-66,4};
int param0_2[] = {0};
int param0_3[] = {99,70,67,5};
int param0_4[] = {-98,-98,-26,-26,-24,-18,-16,80,5};
int param0_5[] = {1,1,1,1,0,1,0};
int param0_6[] = {1,5,12,12,17,17,12,95,96,98,4};
int param0_7[] = {50,-70,-30,-54,6,-10,70,84,5};
int param0_8[] = {0,1,5};
int param0_9[] = {59,21,28,3,14,5};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {0,0,0,0,0,0,0,0,0,0};
    int param2[] = {2,7,1,3,8,6,10,8,2,5};
    int param3[] = {1,96,-1,3,80,1,12,27,14,28};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i]) == f_gold(param0[i],param1[i],param2[i],param3[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}