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
  int cum_sum = 0;
  for ( int i = 0;
  i < n;
  i ++ ) cum_sum += arr [ i ];
  int curr_val = 0;
  for ( int i = 0;
  i < n;
  i ++ ) curr_val += i * arr [ i ];
  int res = curr_val;
  for ( int i = 1;
  i < n;
  i ++ ) {
    int next_val = curr_val - ( cum_sum - arr [ i - 1 ] ) + arr [ i - 1 ] * ( n - 1 );
    curr_val = next_val;
    res = max ( res, next_val );
  }
  return res;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {6,6,13,14,16,20,24,24,24,27,28,36,49,51,55,56,62,69,74,74,76,85,86,90,92,98};
int param0_1[] = {-42,96,68,64,14,-74,76,42,34,-92,-20,28,-80,-34,-22,96,-46,96,10,-82,82,50,-24,48,56,72,-40,-86,84,66,-62,50,-76,34};
int param0_2[] = {0,0,0,0,0,1,1,1,1,1,1};
int param0_3[] = {37,88,70,86,24,62,34,44,37,42,46,34,23,32,55,2,5,70,30,46,40,65,91,4,7,74,46,12,30,22,1,91,89,88,97,6,6,11,33,14,68,24};
int param0_4[] = {-92,-90,-70,-70,-10,2,10,12,14,40,44,46,64,68,68,96};
int param0_5[] = {1,0,1,0,0,0,1,1,0,1,0,1,0,0,1,0,1,1,1,1};
int param0_6[] = {9,15,15,17,19,20,21,23,25,25,25,32,32,33,45,51,54,59,68,71,71,71,72,75,78,80,82,82,88,89,92,93,94,97};
int param0_7[] = {52,-78,-80,32,-56,-98,-36,86,34,-36,42,46,50,0,34,-46,-2,-18,-96,12,-42,62,32,78,66,-8,50,60,10,-18,66,80,-24,-98,8,48,34,44,-80,-34,72,0,-60,52,40,20};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {45,35,25,7,24,73,25,86,48,70,47,91,96,15,39,9};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {13,27,10,39,11,15,22,45,33,8};
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