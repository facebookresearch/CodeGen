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

int f_gold ( int a, int b, int k ) {
  int p = pow ( a, b );
  int count = 0;
  while ( p > 0 && count < k ) {
    int rem = p % 10;
    count ++;
    if ( count == k ) return rem;
    p = p / 10;
  }
  return 0;
}


int f_filled ( int a, int b, int k ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {11,41,5,1,24,5,66,7,77,60};
    int param1[] = {2,3,4,2,1,2,5,10,30,50};
    int param2[] = {1,0,3,4,5,3,8,3,10,1};

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