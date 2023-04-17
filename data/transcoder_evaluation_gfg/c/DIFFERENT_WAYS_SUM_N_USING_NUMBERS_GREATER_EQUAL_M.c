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

int f_gold ( int n, int m ) {
  int dp [ n + 2 ] [ n + 2 ];
  memset ( dp, 0, sizeof ( dp ) );
  dp [ 0 ] [ n + 1 ] = 1;
  for ( int k = n;
  k >= m;
  k -- ) {
    for ( int i = 0;
    i <= n;
    i ++ ) {
      dp [ i ] [ k ] = dp [ i ] [ k + 1 ];
      if ( i - k >= 0 ) dp [ i ] [ k ] = ( dp [ i ] [ k ] + dp [ i - k ] [ k ] );
    }
  }
  return dp [ n ] [ m ];
}


int f_filled ( int n, int m ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {20,77,59,5,41,39,23,7,82,11};
    int param1[] = {18,74,85,76,62,40,58,1,45,66};
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