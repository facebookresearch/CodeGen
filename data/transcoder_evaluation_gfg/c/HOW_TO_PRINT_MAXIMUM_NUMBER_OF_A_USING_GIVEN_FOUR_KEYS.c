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

int f_gold ( int N ) {
  if ( N <= 6 ) return N;
  int screen [ N ];
  int b;
  int n;
  for ( n = 1;
  n <= 6;
  n ++ ) screen [ n - 1 ] = n;
  for ( n = 7;
  n <= N;
  n ++ ) {
    screen [ n - 1 ] = max ( 2 * screen [ n - 4 ], max ( 3 * screen [ n - 5 ], 4 * screen [ n - 6 ] ) );
  }
  return screen [ N - 1 ];
}


int f_filled ( int N ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {41,94,80,40,76,5,43,67,24,90};
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