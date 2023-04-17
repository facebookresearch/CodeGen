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

int f_gold ( int arr [ ], int N, int K ) {
  sort ( arr, arr + N );
  int dp [ N ];
  dp [ 0 ] = 0;
  for ( int i = 1;
  i < N;
  i ++ ) {
    dp [ i ] = dp [ i - 1 ];
    if ( arr [ i ] - arr [ i - 1 ] < K ) {
      if ( i >= 2 ) dp [ i ] = max ( dp [ i ], dp [ i - 2 ] + arr [ i ] + arr [ i - 1 ] );
      else dp [ i ] = max ( dp [ i ], arr [ i ] + arr [ i - 1 ] );
    }
  }
  return dp [ N - 1 ];
}


int f_filled ( int arr [ ], int N, int K ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {48,53,67,78,78,93,95};
int param0_1[] = {-2,52,18,70,32,88,-70,-32,72,30};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {98,84,13,61,58,90,45,89,45,80,3,5,57,86,40,80,60,51,60,73,67,10,52,56,60,36,34,60,75,63,23,86,51,68,86,13,71,86,99,6,42,2,39,82,16,5,23,47,12};
int param0_4[] = {-84,-56,68,78};
int param0_5[] = {0,0,1,0,0,1,1,0,0,0,1,0,1,1,1,1,0};
int param0_6[] = {1,2,3,9,12,12,16,17,18,19,20,21,21,26,29,42,44,45,48,48,48,54,54,55,60,63,63,64,64,67,67,68,69,74,78,78,79,83,95,95,95,96,97,99};
int param0_7[] = {40,-48,-14,64,-58,60,-42,-56,54,28,-16,-92,42};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {64,25,96};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {6,8,37,31,3,14,27,9,21,1};
    int param2[] = {4,8,31,37,3,9,42,8,19,1};
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