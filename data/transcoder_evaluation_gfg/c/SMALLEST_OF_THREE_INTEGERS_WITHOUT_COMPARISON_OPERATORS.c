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

int f_gold ( int x, int y, int z ) {
  int c = 0;
  while ( x && y && z ) {
    x --;
    y --;
    z --;
    c ++;
  }
  return c;
}


int f_filled ( int x, int y, int z ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {23,87,35,25,93,52,95,91,75,96};
    int param1[] = {98,55,90,9,22,42,88,64,1,44};
    int param2[] = {25,94,29,41,39,96,26,51,6,76};
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