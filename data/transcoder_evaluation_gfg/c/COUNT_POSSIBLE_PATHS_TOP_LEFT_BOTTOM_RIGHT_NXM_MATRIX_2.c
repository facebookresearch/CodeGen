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

int f_gold ( int m, int n ) {
  int dp [ n ] = {
    1 };
    dp [ 0 ] = 1;
    for ( int i = 0;
    i < m;
    i ++ ) {
      for ( int j = 1;
      j < n;
      j ++ ) {
        dp [ j ] += dp [ j - 1 ];
      }
    }
    return dp [ n - 1 ];
  }
  

int f_filled ( int m, int n ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {73,70,53,80,9,38,41,80,42,54};
    int param1[] = {75,5,62,70,59,48,49,72,52,1};
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