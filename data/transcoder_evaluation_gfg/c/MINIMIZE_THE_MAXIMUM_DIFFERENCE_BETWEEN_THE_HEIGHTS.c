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

int f_gold ( int arr [ ], int n, int k ) {
  if ( n == 1 ) return 0;
  sort ( arr, arr + n );
  int ans = arr [ n - 1 ] - arr [ 0 ];
  int small = arr [ 0 ] + k;
  int big = arr [ n - 1 ] - k;
  if ( small > big ) swap ( small, big );
  for ( int i = 1;
  i < n - 1;
  i ++ ) {
    int subtract = arr [ i ] - k;
    int add = arr [ i ] + k;
    if ( subtract >= small || add <= big ) continue;
    if ( big - subtract <= add - small ) small = subtract;
    else big = add;
  }
  return min ( ans, big - small );
}


int f_filled ( int arr [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {31,33,40,43,44,51,52,56,60,64,66,79,91,93,99};
int param0_1[] = {-16,34,54,-86,-62};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {27,84,57,45,70,41,67,3,5,67,16,74,99,90,48,90,7,86,59,88,45,11,21,91,17,67,59,60,36,9,5,55,68,58,91,51,44,92,77,38};
int param0_4[] = {-88,-84,-78,-72,-66,-66,-58,-56,-56,-56,-54,-50,-50,-38,-24,-18,-12,-10,-8,-4,0,6,8,10,14,40,44,50,58,64,64,68};
int param0_5[] = {1,1,0,0,1,1,0,1,0,0,0};
int param0_6[] = {6,11,13,14,22,25,26,28,30,31,37,37,55,57,61,62,64,67,69,70,71,73,73,75,80,81,82,88,90,98};
int param0_7[] = {-86,4,-90,66,-10,-36,-18,82,20,6,-78,98,-64,52,-22,20,44,-70,-32,88,-80,24,-38,-62,92};
int param0_8[] = {0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {2};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {10,3,29,28,22,10,29,23,20,0};
    int param2[] = {13,4,22,28,28,8,26,18,19,0};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i]) == f_gold(param0[i],param1[i],param2[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}