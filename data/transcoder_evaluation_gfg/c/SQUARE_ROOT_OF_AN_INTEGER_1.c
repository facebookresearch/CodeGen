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

int f_gold ( int x ) {
  if ( x == 0 || x == 1 ) return x;
  int start = 1, end = x, ans;
  while ( start <= end ) {
    int mid = ( start + end ) / 2;
    if ( mid * mid == x ) return mid;
    if ( mid * mid < x ) {
      start = mid + 1;
      ans = mid;
    }
    else end = mid - 1;
  }
  return ans;
}


int f_filled ( int x ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {40,10,46,54,1,67,64,10,75,11};
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