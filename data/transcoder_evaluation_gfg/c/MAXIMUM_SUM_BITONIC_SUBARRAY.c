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
  int msis [ n ], msds [ n ];
  int max_sum = INT_MIN;
  msis [ 0 ] = arr [ 0 ];
  for ( int i = 1;
  i < n;
  i ++ ) if ( arr [ i ] > arr [ i - 1 ] ) msis [ i ] = msis [ i - 1 ] + arr [ i ];
  else msis [ i ] = arr [ i ];
  msds [ n - 1 ] = arr [ n - 1 ];
  for ( int i = n - 2;
  i >= 0;
  i -- ) if ( arr [ i ] > arr [ i + 1 ] ) msds [ i ] = msds [ i + 1 ] + arr [ i ];
  else msds [ i ] = arr [ i ];
  for ( int i = 0;
  i < n;
  i ++ ) if ( max_sum < ( msis [ i ] + msds [ i ] - arr [ i ] ) ) max_sum = msis [ i ] + msds [ i ] - arr [ i ];
  return max_sum;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {7,12,16,23,26,27,39,39,40,44,57,58,77,78,81,82,84,86,91,94,94,95,97};
int param0_1[] = {72,38,-60,98,-52,-38,-2,94,34,56,90,46,6,-2,30,-96,-76,-96,-76,32,68,64,-32,-4,72,-62,58,20,-84,0,-96,70,-22,-56,70,-74,-90,-86,-14,82,-90,40,-64,94};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {69,31,85,84,28,28};
int param0_4[] = {-80,-74,-24,-22,-22,4,20,28,30,32,36,58,58,68,92,94,98};
int param0_5[] = {1,1,0,0,0,1,0,1,1,1,1};
int param0_6[] = {2,2,2,4,6,7,8,10,15,17,19,20,21,27,28,29,32,32,40,44,46,47,49,50,50,52,55,56,58,59,64,69,73,74,74,77,80,80,84,89,91,95,96,96,97,98,98,99};
int param0_7[] = {26,-86,8,64,-40,64,60,-16,54,-42,-86,14,-48,-20,-42,-4,-34,-52,-74,22,10};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {8,5,5,56,5,38};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {13,37,33,5,16,10,46,18,27,3};
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