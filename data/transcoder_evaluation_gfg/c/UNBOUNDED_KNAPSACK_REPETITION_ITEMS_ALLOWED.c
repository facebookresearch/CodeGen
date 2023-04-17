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

int f_gold ( int W, int n, int val [ ], int wt [ ] ) {
  int dp [ W + 1 ];
  memset ( dp, 0, sizeof dp );
  int ans = 0;
  for ( int i = 0;
  i <= W;
  i ++ ) for ( int j = 0;
  j < n;
  j ++ ) if ( wt [ j ] <= i ) dp [ i ] = max ( dp [ i ], dp [ i - wt [ j ] ] + val [ j ] );
  return dp [ W ];
}


int f_filled ( int W, int n, int val [ ], int wt [ ] ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {12,1,30,25,10,20,2,23,13,18};
    int param1[] = {19,1,24,22,12,32,3,25,13,28};
    int param2_0[] = {2,12,13,13,13,24,29,34,45,47,53,55,58,64,66,74,78,80,82,83,83,84,88,91,91};
int param2_1[] = {54,82};
int param2_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param2_3[] = {37,72,57,18,31,44,81,13,75,91,16,96,55,8,65,47,98,7,88,89,28,78,91,41,34,78,38,71,79,61,37,99,16,87,13,93,20,84,30,53,26,54,23,33,54};
int param2_4[] = {-80,-70,-40,-38,-38,-36,-34,24,26,38,44,62,64,92};
int param2_5[] = {1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,1,0,1,1,0,0,0,0,1,1,1,1};
int param2_6[] = {30,50,64,71};
int param2_7[] = {8,96,72,-88,42,-40,64,-24,68,46,-84,-58,66,-86,-12,78,-24,50,-34,88,-30,74,-82,-68,-54,72};
int param2_8[] = {0,0,0,1,1,1,1,1,1,1,1,1,1,1,1};
int param2_9[] = {4,76,50,27,10,35,96,98,59,77,52,52,80,61,12,49,51,15,30,27,29,2,45,27,57,90,47,56,45};
int *param2[10] = {param2_0,param2_1,param2_2,param2_3,param2_4,param2_5,param2_6,param2_7,param2_8,param2_9};
    int param3_0[] = {5,5,5,28,30,33,36,37,43,50,60,61,67,70,74,79,80,81,84,85,86,86,92,92,99};
int param3_1[] = {12,14};
int param3_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param3_3[] = {37,70,43,47,9,27,30,30,16,91,34,12,98,36,66,91,79,53,16,52,87,99,83,71,79,8,9,55,66,76,77,28,85,82,56,57,11,41,19,48,76,49,83,21,21};
int param3_4[] = {-98,-88,-78,-70,-58,-10,-2,8,20,38,40,56,66,86};
int param3_5[] = {0,0,1,1,1,1,1,1,0,1,0,0,0,1,0,0,1,1,0,0,0,1,1,0,1,0,1,1,0,1,1,1,1,0,1,1,0,0,0};
int param3_6[] = {6,10,23,97};
int param3_7[] = {-42,48,66,-84,98,-14,84,80,-20,-76,-74,44,-44,18,86,58,68,80,-72,-52,-2,58,90,64,54,80};
int param3_8[] = {0,0,0,0,0,0,0,1,1,1,1,1,1,1,1};
int param3_9[] = {73,26,38,19,54,61,62,52,40,49,93,1,73,55,31,77,75,84,73,54,93,57,15,67,54,43,17,16,89};
int *param3[10] = {param3_0,param3_1,param3_2,param3_3,param3_4,param3_5,param3_6,param3_7,param3_8,param3_9};
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