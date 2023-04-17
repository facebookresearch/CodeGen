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

char f_gold [] ( char num [] ) {
  int n = len(num);
  int rightMin [ n ], right;
  rightMin [ n - 1 ] = - 1;
  right = n - 1;
  for ( int i = n - 2;
  i >= 1;
  i -- ) {
    if ( num [ i ] >= num [ right ] ) rightMin [ i ] = right;
    else {
      if ( num [ i ] == num [ i + 1 ] ) {
        rightMin [ i ] = right;
      }
      else {
        rightMin [ i ] = - 1;
        right = i;
      }
    }
  }
  int small = - 1;
  for ( int i = 1;
  i < n;
  i ++ ) if ( num [ i ] != '0' ) {
    if ( small == - 1 ) {
      if ( num [ i ] < num [ 0 ] ) small = i;
    }
    else if ( num [ i ] <= num [ small ] ) small = i;
  }
  if ( small != - 1 ) swap ( num [ 0 ], num [ small ] );
  else {
    for ( int i = 1;
    i < n;
    i ++ ) {
      if ( rightMin [ i ] != - 1 && num [ i ] != num [ rightMin [ i ] ] ) {
        swap ( num [ i ], num [ rightMin [ i ] ] );
        break;
      }
    }
  }
  return num;
}


char f_filled [] ( char num [] ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"ncYltuhSxEfG","26615541616459","0101","hK","422162103899","0010","zfcSh","92","0","v"};
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