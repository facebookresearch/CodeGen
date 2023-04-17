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

bool f_gold ( int x, int y, int n ) {
  int dp [ n + 1 ];
  dp [ 0 ] = false;
  dp [ 1 ] = true;
  for ( int i = 2;
  i <= n;
  i ++ ) {
    if ( i - 1 >= 0 and ! dp [ i - 1 ] ) dp [ i ] = true;
    else if ( i - x >= 0 and ! dp [ i - x ] ) dp [ i ] = true;
    else if ( i - y >= 0 and ! dp [ i - y ] ) dp [ i ] = true;
    else dp [ i ] = false;
  }
  return dp [ n ];
}


bool f_filled ( int x, int y, int n ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {6,32,99,22,26,67,69,39,7,91};
    int param1[] = {27,88,18,1,78,51,57,8,82,56};
    int param2[] = {51,69,48,74,95,27,91,9,41,7};
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