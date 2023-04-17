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

int f_gold ( int m, int n, int x ) {
  int table [ n + 1 ] [ x + 1 ];
  memset ( table, 0, sizeof ( table ) );
  for ( int j = 1;
  j <= m && j <= x;
  j ++ ) table [ 1 ] [ j ] = 1;
  for ( int i = 2;
  i <= n;
  i ++ ) for ( int j = 1;
  j <= x;
  j ++ ) for ( int k = 1;
  k <= m && k < j;
  k ++ ) table [ i ] [ j ] += table [ i - 1 ] [ j - k ];
  return table [ n ] [ x ];
}


int f_filled ( int m, int n, int x ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {94,7,20,90,50,32,46,82,43,6};
    int param1[] = {4,12,44,94,58,90,25,50,82,83};
    int param2[] = {69,33,24,88,27,29,6,87,70,19};
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