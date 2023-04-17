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

bool f_gold ( char str [] ) {
  int n = strlen(str);
  int dp [ n + 1 ] [ 10 ];
  memset ( dp, 0, sizeof ( dp ) );
  int arr [ n + 1 ];
  for ( int i = 1;
  i <= n;
  i ++ ) arr [ i ] = str [ i - 1 ] - '0';
  for ( int i = 1;
  i <= n;
  i ++ ) {
    dp [ i ] [ arr [ i ] % 8 ] = 1;
    for ( int j = 0;
    j < 8;
    j ++ ) {
      if ( dp [ i - 1 ] [ j ] > dp [ i ] [ ( j * 10 + arr [ i ] ) % 8 ] ) dp [ i ] [ ( j * 10 + arr [ i ] ) % 8 ] = dp [ i - 1 ] [ j ];
      if ( dp [ i - 1 ] [ j ] > dp [ i ] [ j ] ) dp [ i ] [ j ] = dp [ i - 1 ] [ j ];
    }
  }
  for ( int i = 1;
  i <= n;
  i ++ ) {
    if ( dp [ i ] [ 0 ] == 1 ) return true;
  }
  return false;
}


bool f_filled ( char str [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"n jcjfyMoJEK","70507","0000111","YjRiCqr","4730248784","010101110","nLJV duUNH","27","1000","L"};
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