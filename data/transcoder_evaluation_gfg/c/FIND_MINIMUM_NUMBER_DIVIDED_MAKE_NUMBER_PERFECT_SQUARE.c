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

int f_gold ( int n ) {
  int count = 0, ans = 1;
  while ( n % 2 == 0 ) {
    count ++;
    n /= 2;
  }
  if ( count % 2 ) ans *= 2;
  for ( int i = 3;
  i <= sqrt ( n );
  i += 2 ) {
    count = 0;
    while ( n % i == 0 ) {
      count ++;
      n /= i;
    }
    if ( count % 2 ) ans *= i;
  }
  if ( n > 2 ) ans *= n;
  return ans;
}


int f_filled ( int n ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {95,48,3,10,82,1,77,99,23,61};
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