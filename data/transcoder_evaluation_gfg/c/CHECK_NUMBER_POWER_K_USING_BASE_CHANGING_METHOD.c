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

bool f_gold ( unsigned int n, unsigned int k ) {
  bool oneSeen = false;
  while ( n > 0 ) {
    int digit = n % k;
    if ( digit > 1 ) return false;
    if ( digit == 1 ) {
      if ( oneSeen ) return false;
      oneSeen = true;
    }
    n /= k;
  }
  return true;
}


bool f_filled ( unsigned int n, unsigned int k ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {64,16,27,81,1,69,8,31,43,54};
    int param1[] = {4,2,3,72,9,17,20,79,81,89};
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