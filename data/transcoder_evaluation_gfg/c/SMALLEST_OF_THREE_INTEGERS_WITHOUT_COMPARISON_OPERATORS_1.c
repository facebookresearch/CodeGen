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

int f_gold ( int x, int y, int z ) {
  if ( ! ( y / x ) ) return ( ! ( y / z ) ) ? y : z;
  return ( ! ( x / z ) ) ? x : z;
}


int f_filled ( int x, int y, int z ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {48,11,50,21,94,22,3,67,59,50};
    int param1[] = {63,55,89,71,39,44,41,62,2,11};
    int param2[] = {56,84,96,74,42,86,68,94,83,1};
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