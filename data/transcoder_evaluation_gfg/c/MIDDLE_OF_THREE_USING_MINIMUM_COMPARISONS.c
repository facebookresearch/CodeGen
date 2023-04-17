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
  if ( ( a < b && b < c ) || ( c < b && b < a ) ) return b;
  else if ( ( b < a && a < c ) || ( c < a && a < b ) ) return a;
  else return c;
}


int f_filled ( int a, int b, int c ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {56,56,36,71,3,84,30,82,90,38};
    int param1[] = {5,60,56,54,70,57,80,54,70,4};
    int param2[] = {82,17,51,6,81,47,85,32,55,5};
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