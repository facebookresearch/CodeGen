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
  int brr [ 2 * n + 1 ];
  for ( int i = 0;
  i < n;
  i ++ ) brr [ i ] = arr [ i ];
  for ( int i = 0;
  i < n;
  i ++ ) brr [ n + i ] = arr [ i ];
  int maxHam = 0;
  for ( int i = 1;
  i < n;
  i ++ ) {
    int currHam = 0;
    for ( int j = i, k = 0;
    j < ( i + n );
    j ++, k ++ ) if ( brr [ j ] != arr [ k ] ) currHam ++;
    if ( currHam == n ) return n;
    maxHam = max ( maxHam, currHam );
  }
  return maxHam;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,4,18,22,28,34,35,39,44,45,67,73,75,79,81,83,89,93,96};
int param0_1[] = {52,-28};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {24};
int param0_4[] = {-68,14,36,62};
int param0_5[] = {1,0,1,1,1,1,1,0,0,0,1,0,0,0,1,1,0,1,0,1,1,0,1,0,0};
int param0_6[] = {7,10,19,22,24,28,29,39,46,55,62,66,68,73,74,76,83,84,85,99};
int param0_7[] = {-38,56,86,12,24,-90,-20,-46,38,92,-44,-74,54,50,46,50,-94,64,32,-84,70};
int param0_8[] = {0,0,0,0,0,0,1,1,1,1,1,1,1};
int param0_9[] = {61,89,8};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {12,1,21,0,2,12,15,14,8,2};
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