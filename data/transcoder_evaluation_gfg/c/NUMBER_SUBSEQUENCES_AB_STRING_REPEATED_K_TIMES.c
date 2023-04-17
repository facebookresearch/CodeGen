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

int f_gold ( char s [], int K ) {
  int n = strlen(s);
  int C, c1 = 0, c2 = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( s [ i ] == 'a' ) c1 ++;
    if ( s [ i ] == 'b' ) {
      c2 ++;
      C += c1;
    }
  }
  return C * K + ( K * ( K - 1 ) / 2 ) * c1 * c2;
}


int f_filled ( char s [], int K ) {}

int main(void) {
    int n_success = 0;
    char param0[][100] = {"KdJ","031","11000","zPbB","9","1010","c","06064629743411","1111","PFXAhru"};
    int param1[] = {96,70,59,60,80,41,87,4,18,83};
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