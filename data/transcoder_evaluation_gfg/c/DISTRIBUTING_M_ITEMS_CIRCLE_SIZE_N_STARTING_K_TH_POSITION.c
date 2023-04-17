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

int f_gold ( int n, int m, int k ) {
  if ( m <= n - k + 1 ) return m + k - 1;
  m = m - ( n - k + 1 );
  return ( m % n == 0 ) ? n : ( m % n );
}


int f_filled ( int n, int m, int k ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {19,23,92,9,20,68,66,77,90,26};
    int param1[] = {14,51,10,50,67,25,30,22,1,34};
    int param2[] = {34,5,24,34,20,40,24,32,71,54};
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