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

int f_gold ( int a [ ], int n, int k ) {
  int result = 0;
  for ( int i = 0;
  i < n;
  ++ i ) {
    if ( a [ i ] != 1 && a [ i ] > k ) {
      result = result + min ( a [ i ] % k, k - a [ i ] % k );
    }
    else {
      result = result + k - a [ i ];
    }
  }
  return result;
}


int f_filled ( int a [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {3,7,27,32,36,37,44,48,50,64,86};
int param0_1[] = {-22,6,-20,60,-74,98,52,-22};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {77,11,51,11,84,79,43,12,14,50,15,6,85,32,74,49,7,2,58};
int param0_4[] = {-90,-66,-64,-58,-46,-44,-32,-30,-30,-22,-18,-14,12,12,18,34,44,60,70,70,74,76,86,98,98};
int param0_5[] = {1,1,0,0,0,0,1,0,0,1,1,1,0,1,1,1,0,0,0,1,1,1,1,0,1,0,1,1,1,1,1,0,0,0,0,1,1};
int param0_6[] = {9,22,27,27,37,53,53,56,63,73,76,81,82};
int param0_7[] = {-46,60,80,80,42,-98,30,-48,4,-32,-78,40,52,26,88,4,22,62,88,-94,2,0,58,38,52,-50,-52,58,-62,30,-38,-8,-82,-66};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {42,69,93,82,8,23,73,1,77,39,49,4,95,85};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {5,5,23,9,12,36,10,18,19,12};
    int param2[] = {10,4,29,17,22,31,11,19,22,13};
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