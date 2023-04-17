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

int f_gold ( int C, int l ) {
  if ( l >= C ) return C;
  double eq_root = ( std :: sqrt ( 1 + 8 * ( C - l ) ) - 1 ) / 2;
  return std :: ceil ( eq_root ) + l;
}


int f_filled ( int C, int l ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {91,99,11,23,12,1,18,14,13,36};
    int param1[] = {29,55,56,56,97,64,5,37,55,99};
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