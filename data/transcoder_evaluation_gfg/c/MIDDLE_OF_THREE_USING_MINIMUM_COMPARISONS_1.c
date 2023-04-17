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

int f_gold ( int a, int b, int c ) {
  if ( a > b ) {
    if ( b > c ) return b;
    else if ( a > c ) return c;
    else return a;
  }
  else {
    if ( a > c ) return a;
    else if ( b > c ) return c;
    else return b;
  }
}


int f_filled ( int a, int b, int c ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {43,76,57,10,59,92,49,16,33,66};
    int param1[] = {24,54,5,13,47,14,62,95,41,63};
    int param2[] = {7,66,40,4,56,50,65,12,90,46};
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