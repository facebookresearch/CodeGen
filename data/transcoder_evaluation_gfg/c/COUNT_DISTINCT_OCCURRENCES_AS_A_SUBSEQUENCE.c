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

int f_gold ( char S [], char T [] ) {
  int m = strlen(T), n = strlen(S);
  if ( m > n ) return 0;
  int mat [ m + 1 ] [ n + 1 ];
  for ( int i = 1;
  i <= m;
  i ++ ) mat [ i ] [ 0 ] = 0;
  for ( int j = 0;
  j <= n;
  j ++ ) mat [ 0 ] [ j ] = 1;
  for ( int i = 1;
  i <= m;
  i ++ ) {
    for ( int j = 1;
    j <= n;
    j ++ ) {
      if ( T [ i - 1 ] != S [ j - 1 ] ) mat [ i ] [ j ] = mat [ i ] [ j - 1 ];
      else mat [ i ] [ j ] = mat [ i ] [ j - 1 ] + mat [ i - 1 ] [ j - 1 ];
    }
  }
  return mat [ m ] [ n ];
}


int f_filled ( char S [], char T [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"banana","49597223","1000010000011","BTlzufK","3474007","0010","dKHhoTD","9123259723","11001000111110","iY WJlIZ"};
    char param1[][100] = {"ban","42","010","lf","370","00000","doT","123","0","iI"};
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