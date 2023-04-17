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

bool f_gold ( long long a, long long b ) {
  if ( a == 0 || b == 0 ) return false;
  long long result = a * b;
  if ( a == result / b ) return false;
  else return true;
}


bool f_filled ( long long a, long long b ) {}

int main(void) {
    int n_success = 0;
    long param0[] = {37,10000000000,10000000000,999999999,39,92,14,19,14,88};
    long param1[] = {80,-10000000000,10000000000,999999999,36,56,21,38,82,41};
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