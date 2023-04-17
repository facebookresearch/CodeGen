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
  int res = INT_MIN;
  for ( int i = 0;
  i < n;
  i ++ ) {
    int prefix_sum = arr [ i ];
    for ( int j = 0;
    j < i;
    j ++ ) prefix_sum += arr [ j ];
    int suffix_sum = arr [ i ];
    for ( int j = n - 1;
    j > i;
    j -- ) suffix_sum += arr [ j ];
    if ( prefix_sum == suffix_sum ) res = max ( res, prefix_sum );
  }
  return res;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {3,3,9,19,22,27,32,41,45,63,66,67,81,91};
int param0_1[] = {-64,-2,68,-48,22,-14,-98};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {86,79,23,55,4,22,37,1,72,22,82,62,96,47};
int param0_4[] = {-96,-96,-96,-96,-92,-82,-72,-72,-62,-58,-52,-48,-44,-44,-40,-34,-28,-26,-26,0,0,2,4,4,12,12,18,34,36,40,48,48,54,60,66,66,72,76,78,82,82,96,98};
int param0_5[] = {0,1,0,1,1,0,0,0,1,1,1,0,0,1,0,0,1,1,0,0,0,0,1,1,0,1,0,0,0,0,0,1,1,1,1,1,0,0,1,1,0,0,0,1,0};
int param0_6[] = {2,3,7,13,20,24,39,49,53,58,72,80,90,99};
int param0_7[] = {-48,44,60,-30,8,20,70,-50,80,-2,-28,-14};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_9[] = {64,13,18,3,22,29,51,45,21,13,47,15,17,34,60,99,30,54,16,47,13,49,60,66,28,57,85,66,65,7,62,29,9};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {13,4,19,8,33,38,11,11,16,21};
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