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

int f_gold ( int n ) {
  int * dp = new int [ n + 1 ];
  dp [ 0 ] = 0;
  dp [ 1 ] = 1;
  dp [ 2 ] = 2;
  dp [ 3 ] = 3;
  for ( int i = 4;
  i <= n;
  i ++ ) {
    dp [ i ] = i;
    for ( int x = 1;
    x <= ceil ( sqrt ( i ) );
    x ++ ) {
      int temp = x * x;
      if ( temp > i ) break;
      else dp [ i ] = min ( dp [ i ], 1 + dp [ i - temp ] );
    }
  }
  int res = dp [ n ];
  delete [ ] dp;
  return res;
}


int f_filled ( int n ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {16,33,47,98,36,81,55,19,4,22};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i]) == f_gold(param0[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}