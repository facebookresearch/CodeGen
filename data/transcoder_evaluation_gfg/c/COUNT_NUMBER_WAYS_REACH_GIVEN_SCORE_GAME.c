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
  int table [ n + 1 ], i;
  for ( int j = 0;
  j < n + 1;
  j ++ ) table [ j ] = 0;
  table [ 0 ] = 1;
  for ( i = 3;
  i <= n;
  i ++ ) table [ i ] += table [ i - 3 ];
  for ( i = 5;
  i <= n;
  i ++ ) table [ i ] += table [ i - 5 ];
  for ( i = 10;
  i <= n;
  i ++ ) table [ i ] += table [ i - 10 ];
  return table [ n ];
}


int f_filled ( int n ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {83,29,17,12,93,55,97,75,22,52};
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