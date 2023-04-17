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

int f_gold ( int limit ) {
  if ( limit < 2 ) return 0;
  long long int ef1 = 0, ef2 = 2;
  long long int sum = ef1 + ef2;
  while ( ef2 <= limit ) {
    long long int ef3 = 4 * ef2 + ef1;
    if ( ef3 > limit ) break;
    ef1 = ef2;
    ef2 = ef3;
    sum += ef2;
  }
  return sum;
}


int f_filled ( int limit ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {67,89,12,94,96,25,49,8,33,59};
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