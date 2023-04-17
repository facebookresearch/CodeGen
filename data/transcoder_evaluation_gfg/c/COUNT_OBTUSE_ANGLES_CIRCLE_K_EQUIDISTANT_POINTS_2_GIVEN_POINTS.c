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

int f_gold ( int a, int b, int k ) {
  int c1 = ( b - a ) - 1;
  int c2 = ( k - b ) + ( a - 1 );
  if ( c1 == c2 ) return 0;
  return min ( c1, c2 );
}


int f_filled ( int a, int b, int k ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {83,3,11,50,40,62,40,66,6,25};
    int param1[] = {98,39,96,67,16,86,78,11,9,5};
    int param2[] = {86,87,30,48,32,76,71,74,19,5};
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