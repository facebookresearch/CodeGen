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
  int * jumps = new int [ n ];
  int i, j;
  if ( n == 0 || arr [ 0 ] == 0 ) return INT_MAX;
  jumps [ 0 ] = 0;
  for ( i = 1;
  i < n;
  i ++ ) {
    jumps [ i ] = INT_MAX;
    for ( j = 0;
    j < i;
    j ++ ) {
      if ( i <= j + arr [ j ] && jumps [ j ] != INT_MAX ) {
        jumps [ i ] = min ( jumps [ i ], jumps [ j ] + 1 );
        break;
      }
    }
  }
  return jumps [ n - 1 ];
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,5,9,9,12,13,13,13,15,16,17,18,20,20,20,25,28,30,30,33,34,34,37,42,45,49,50,52,52,54,65,68,72,74,75,82,85,87,91,91,94,95};
int param0_1[] = {-28,90,30,-80,-10,26,-12,24,12,44,-38,20,26,38,-8,-40,88,26};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {74,37,37,71,85,89,44,72,55,8,5,98,54,37,7,76,93,74,84,51,18,37};
int param0_4[] = {-68,14,76};
int param0_5[] = {0,0,1,1,0,0,0,1,0,0,1,0,0,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,0,1,0,0,1,0,1,1,0,1,0,0,1,1,1};
int param0_6[] = {3,4,6,6,7,14,28,36,37,44,46,47,50,51,52,55,55,61,68,69,70,73,74,77,86,90,90,91,98,99};
int param0_7[] = {-4,-24,-84,-76};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {78,88,1,98,26,31,56,12,71};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {22,9,37,20,1,27,23,2,32,8};
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