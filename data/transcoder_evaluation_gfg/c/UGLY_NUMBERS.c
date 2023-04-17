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

unsigned f_gold ( unsigned n ) {
  unsigned ugly [ n ];
  unsigned i2 = 0, i3 = 0, i5 = 0;
  unsigned next_multiple_of_2 = 2;
  unsigned next_multiple_of_3 = 3;
  unsigned next_multiple_of_5 = 5;
  unsigned next_ugly_no = 1;
  ugly [ 0 ] = 1;
  for ( int i = 1;
  i < n;
  i ++ ) {
    next_ugly_no = min ( next_multiple_of_2, min ( next_multiple_of_3, next_multiple_of_5 ) );
    ugly [ i ] = next_ugly_no;
    if ( next_ugly_no == next_multiple_of_2 ) {
      i2 = i2 + 1;
      next_multiple_of_2 = ugly [ i2 ] * 2;
    }
    if ( next_ugly_no == next_multiple_of_3 ) {
      i3 = i3 + 1;
      next_multiple_of_3 = ugly [ i3 ] * 3;
    }
    if ( next_ugly_no == next_multiple_of_5 ) {
      i5 = i5 + 1;
      next_multiple_of_5 = ugly [ i5 ] * 5;
    }
  }
  return next_ugly_no;
}


unsigned f_filled ( unsigned n ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {27,64,93,90,85,86,72,86,32,1};
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