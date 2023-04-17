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
  int mls [ n ], max = 0;
  for ( int i = 0;
  i < n;
  i ++ ) mls [ i ] = 1;
  for ( int i = 1;
  i < n;
  i ++ ) for ( int j = 0;
  j < i;
  j ++ ) if ( abs ( arr [ i ] - arr [ j ] ) <= 1 && mls [ i ] < mls [ j ] + 1 ) mls [ i ] = mls [ j ] + 1;
  for ( int i = 0;
  i < n;
  i ++ ) if ( max < mls [ i ] ) max = mls [ i ];
  return max;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,5,9,31,31,37,41,55,56,61,79,81,89,93};
int param0_1[] = {-76,96,-68,-16,22,-24,-24,6,98,-82,54,-80,46,0,0,-50};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {97,93,43,51,15,33,13,96,39,89,78,25,45,6,64,54};
int param0_4[] = {-98,-78,-72,-70,-68,-58,-56,-54,-46,-44,-38,-34,-30,-24,-18,-16,-14,-12,2,6,8,8,10,10,16,24,26,28,40,42,44,56,58,62,66,66,78,86};
int param0_5[] = {1,1,0,1,0,0};
int param0_6[] = {7,8,10,11,12,15,16,16,19,21,23,23,23,25,26,35,38,43,46,47,51,52,53,57,60,61,66,67,69,74,75,81,83,84,88,92,94,98,98,99};
int param0_7[] = {14,-40};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {59,70,53};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {12,15,29,13,19,3,34,1,38,1};
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