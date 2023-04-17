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

int f_gold ( int n, int a [ ] ) {
  int res = 0;
  for ( int i = 0;
  i < 2 * n;
  i ++ ) {
    if ( i % 2 == 0 ) res += a [ i ] * a [ i ];
    else res -= a [ i ] * a [ i ];
  }
  return res;
}


int f_filled ( int n, int a [ ] ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {22,18,18,11,21,26,6,1,13,11};
    int param1_0[] = {4,4,5,11,13,14,19,20,25,25,26,33,34,37,43,44,44,45,47,48,50,50,60,61,64,65,71,73,79,80,83,85,87,90,95,96,98};
int param1_1[] = {-16,-38,-68,52,-92,76,94,-28,62,-26,38,-14,66,80,-70,52,-84,64,80,-36};
int param1_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_3[] = {11,35,61,21,61,26,27,93,95,77,5,33,94,67};
int param1_4[] = {-96,-90,-64,-60,-52,-50,-42,-36,-30,-16,-8,-8,-4,18,20,22,24,34,52,54,58,64,74,78,80,86,88,96};
int param1_5[] = {0,0,1,0,1,1,1,1,1,0,1,0,0,0,0,1,1,1,0,1,0,0,1,0,0,0,1,0,0,0,1,1,1,0,0,1,0,0,1,1,0};
int param1_6[] = {4,28,35,42,44,58,64,69,72,76,90};
int param1_7[] = {-44,-34};
int param1_8[] = {0,0,0,0,0,0,0,1,1,1,1,1,1,1};
int param1_9[] = {83,48,93,25,25,35,39,34,98,80,22,14,48,64,77,87,56,27,33,15,81};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
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