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

int f_gold ( int arr [ ], int n ) {
  int min_prefix_sum = 0;
  int res = numeric_limits < int > :: min ( );
  int prefix_sum [ n ];
  prefix_sum [ 0 ] = arr [ 0 ];
  for ( int i = 1;
  i < n;
  i ++ ) prefix_sum [ i ] = prefix_sum [ i - 1 ] + arr [ i ];
  for ( int i = 0;
  i < n;
  i ++ ) {
    res = max ( res, prefix_sum [ i ] - min_prefix_sum );
    min_prefix_sum = min ( min_prefix_sum, prefix_sum [ i ] );
  }
  return res;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {8,9,11,17,18,19,23,24,27,30,31,31,35,44,46,47,49,51,55,58,59,61,65,67,71,71,71,71,78,78,82,91,98};
int param0_1[] = {-82,-28,-66,-52,-36,36,-88,52,-62,46,42,26,-60,18,-52,38,94,-68,44,-94,14,36,-70};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {28,36,42,42,5,52,74,86,55,82,59,81,4,90,24,34,20,99,86,25,52,48,62,5,67,83,60,72,80,73,38,55,8,70,95};
int param0_4[] = {-92,-52,-24,36,56};
int param0_5[] = {0,1,1,1,0,1,0,1,0,0,1,1,0,1,1,0,0,0};
int param0_6[] = {1,1,4,4,7,7,17,18,20,26,26,32,37,38,42,44,44,46,50,53,57,58,58,60,61,61,64,74,75,77,83,83,84,84,85,87,88,90,95,96,97,98,99,99};
int param0_7[] = {-86,2,26,54,-16,16,48,24,50,-10,-32,-62,48,-12,-66};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {58,14,79,11,31,28,61,86,25,27,75,78,32,55,86,48,15,51,6,78,23,82,16,62,35,51,91,16,79,38,97,30,23,58,95,57,82,35,57,43,22,41,58,69,25,65,13,79};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {20,15,19,19,3,13,25,13,14,39};
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