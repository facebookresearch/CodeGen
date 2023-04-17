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

int f_gold ( int low, int high ) {
  int f1 = 0, f2 = 1, f3 = 1;
  int result = 0;
  while ( f1 <= high ) {
    if ( f1 >= low ) result ++;
    f1 = f2;
    f2 = f3;
    f3 = f1 + f2;
  }
  return result;
}


int f_filled ( int low, int high ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {76,96,19,36,60,20,76,63,2,41};
    int param1[] = {43,52,79,2,11,15,4,93,25,39};
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