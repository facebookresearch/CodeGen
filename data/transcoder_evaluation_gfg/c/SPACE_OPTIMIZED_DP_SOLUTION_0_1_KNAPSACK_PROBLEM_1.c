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

int f_gold ( int val [ ], int wt [ ], int n, int W ) {
  int dp [ W + 1 ];
  memset ( dp, 0, sizeof ( dp ) );
  for ( int i = 0;
  i < n;
  i ++ ) for ( int j = W;
  j >= wt [ i ];
  j -- ) dp [ j ] = max ( dp [ j ], val [ i ] + dp [ j - wt [ i ] ] );
  return dp [ W ];
}


int f_filled ( int val [ ], int wt [ ], int n, int W ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {11,25,72,90,95};
int param0_1[] = {70,84,-24,-34,50,-10,-12,-98,6,-6,-34,34,80,-70,-72,-54,8,-84,8,-28,68,4,-88,94,-44,0,-24,-40,62,46,84,8,42,-8,-44,-66,-4,-12,20};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {32,49,97,60,46,68,94,41,81,67,13,18,87,99,97,51,36,81,34,12,5,48,91,40,13,26,14,96,11,38,80,57,22,16,77,76,82,29,82,2,54,2,3,93,56,72,11};
int param0_4[] = {-60,-44,-30,-26,8,40,44,60,90};
int param0_5[] = {0,0,1,0,0,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1,1};
int param0_6[] = {19,25,31,35,56,75,79,81,88,96,99};
int param0_7[] = {-98,-4,-50,-52,-6,68,88,38};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {33,19,16,99,11};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {10,28,50,60,66};
int param1_1[] = {20,-90,38,56,40,-86,6,-66,18,-82,90,-56,-10,46,18,60,96,-74,66,-76,-28,-80,-68,84,-62,-88,-92,-40,90,-8,-46,-10,70,-26,-82,22,-30,-6,-58};
int param1_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_3[] = {76,32,4,9,88,56,16,81,86,71,10,93,36,24,64,56,78,78,89,22,52,50,47,23,96,90,91,76,83,19,52,34,96,29,61,85,35,5,76,7,41,2,89,10,44,70,91};
int param1_4[] = {-82,-78,-54,-40,-36,-16,76,84,84};
int param1_5[] = {0,0,0,1,0,1,1,0,0,1,0,0,1,0,0,0,1,0,0,1,1,1,1,0};
int param1_6[] = {1,8,10,26,34,47,50,58,63,81,87};
int param1_7[] = {34,-36,-66,22,38,-78,-24,36};
int param1_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_9[] = {75,74,98,69,87};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {4,35,21,25,6,13,7,6,24,4};
    int param3[] = {2,24,21,32,7,23,10,6,29,2};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i]) == f_gold(param0[i],param1[i],param2[i],param3[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}