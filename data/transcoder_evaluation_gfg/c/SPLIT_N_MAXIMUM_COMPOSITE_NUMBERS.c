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
  if ( n < 4 ) return - 1;
  int rem = n % 4;
  if ( rem == 0 ) return n / 4;
  if ( rem == 1 ) {
    if ( n < 9 ) return - 1;
    return ( n - 9 ) / 4 + 1;
  }
  if ( rem == 2 ) return ( n - 6 ) / 4 + 1;
  if ( rem == 3 ) {
    if ( n < 15 ) return - 1;
    return ( n - 15 ) / 4 + 2;
  }
}


int f_filled ( int n ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {55,35,24,75,5,7,50,28,67,59};
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