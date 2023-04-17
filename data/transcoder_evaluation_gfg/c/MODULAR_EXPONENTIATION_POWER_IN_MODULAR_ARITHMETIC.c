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

int f_gold ( int x, unsigned int y, int p ) {
  int res = 1;
  x = x % p;
  while ( y > 0 ) {
    if ( y & 1 ) res = ( res * x ) % p;
    y = y >> 1;
    x = ( x * x ) % p;
  }
  return res;
}


int f_filled ( int x, unsigned int y, int p ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {45,67,26,33,35,68,14,5,23,37};
    int param1[] = {5,25,91,61,8,41,76,89,42,63};
    int param2[] = {68,49,44,9,13,5,20,13,45,56};
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