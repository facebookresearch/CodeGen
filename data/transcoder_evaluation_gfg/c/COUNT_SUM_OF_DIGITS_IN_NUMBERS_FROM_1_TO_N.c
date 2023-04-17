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
  if ( n < 10 ) return n * ( n + 1 ) / 2;
  int d = log10 ( n );
  int * a = new int [ d + 1 ];
  a [ 0 ] = 0, a [ 1 ] = 45;
  for ( int i = 2;
  i <= d;
  i ++ ) a [ i ] = a [ i - 1 ] * 10 + 45 * ceil ( pow ( 10, i - 1 ) );
  int p = ceil ( pow ( 10, d ) );
  int msd = n / p;
  return msd * a [ d ] + ( msd * ( msd - 1 ) / 2 ) * p + msd * ( 1 + n % p ) + f_gold ( n % p );
}


int f_filled ( int n ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {29,97,71,82,69,30,82,32,77,39};
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