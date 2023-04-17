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

int f_gold ( int a, int b ) {
  if ( a == b ) return a;
  if ( a == 0 ) return b;
  if ( b == 0 ) return a;
  if ( ~ a & 1 ) {
    if ( b & 1 ) return f_gold ( a >> 1, b );
    else return f_gold ( a >> 1, b >> 1 ) << 1;
  }
  if ( ~ b & 1 ) return f_gold ( a, b >> 1 );
  if ( a > b ) return f_gold ( ( a - b ) >> 1, b );
  return f_gold ( ( b - a ) >> 1, a );
}


int f_filled ( int a, int b ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {52,36,12,69,45,7,45,62,96,89};
    int param1[] = {29,94,6,7,11,51,55,86,63,12};
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