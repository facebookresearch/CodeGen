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
  int T [ m + 1 ] [ n + 1 ];
  for ( int i = 0;
  i < m + 1;
  i ++ ) {
    for ( int j = 0;
    j < n + 1;
    j ++ ) {
      if ( i == 0 || j == 0 ) T [ i ] [ j ] = 0;
      else if ( i < j ) T [ i ] [ j ] = 0;
      else if ( j == 1 ) T [ i ] [ j ] = i;
      else T [ i ] [ j ] = T [ i - 1 ] [ j ] + T [ i / 2 ] [ j - 1 ];
    }
  }
  return T [ m ] [ n ];
}


int f_filled ( int m, int n ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {10,5,2,83,91,18,83,98,43,31};
    int param1[] = {4,2,8,7,0,53,41,53,37,20};
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