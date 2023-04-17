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

int f_gold ( char str [ ], int l, int h ) {
  if ( l > h ) return INT_MAX;
  if ( l == h ) return 0;
  if ( l == h - 1 ) return ( str [ l ] == str [ h ] ) ? 0 : 1;
  return ( str [ l ] == str [ h ] ) ? f_gold ( str, l + 1, h - 1 ) : ( min ( f_gold ( str, l, h - 1 ), f_gold ( str, l + 1, h ) ) + 1 );
}


int f_filled ( char str [ ], int l, int h ) {}

int main(void) {
    int n_success = 0;
    char param0_0[] = {'};
char *param0[1] = {param0_0};
    int param1[] = {11,19,0,24,33,13,16,31,37,26};
    int param2[] = {11,22,0,27,34,8,14,25,35,27};
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