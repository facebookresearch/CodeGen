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

long long f_gold ( long long a, long long b, long long mod ) {
  long long res = 0;
  a %= mod;
  while ( b ) {
    if ( b & 1 ) res = ( res + a ) % mod;
    a = ( 2 * a ) % mod;
    b >>= 1;
  }
  return res;
}


long long f_filled ( long long a, long long b, long long mod ) {}

int main(void) {
    int n_success = 0;
    long param0[] = {60,46,4,67,93,89,8,53,96,38};
    long param1[] = {24,43,50,1,35,97,78,73,92,64};
    long param2[] = {58,29,71,66,73,8,55,22,83,83};
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