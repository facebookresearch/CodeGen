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

int f_gold ( int n, int a = 0, int b = 1 ) {
  if ( n == 0 ) return a;
  if ( n == 1 ) return b;
  return f_gold ( n - 1, b, a + b );
}


int f_filled ( int n, int a = 0, int b = 1 ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {4,60,92,73,58,82,53,57,47,83};
    int param1[] = {43,48,21,79,38,26,10,37,91,3};
    int param2[] = {24,98,69,38,30,12,17,26,99,64};
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