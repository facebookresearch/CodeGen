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

int f_gold ( int low, int high ) {
  int fact = 1, x = 1;
  while ( fact < low ) {
    fact = fact * x;
    x ++;
  }
  int res = 0;
  while ( fact <= high ) {
    res ++;
    fact = fact * x;
    x ++;
  }
  return res;
}


int f_filled ( int low, int high ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {57,57,31,62,49,82,31,5,76,55};
    int param1[] = {79,21,37,87,98,76,45,52,43,6};
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