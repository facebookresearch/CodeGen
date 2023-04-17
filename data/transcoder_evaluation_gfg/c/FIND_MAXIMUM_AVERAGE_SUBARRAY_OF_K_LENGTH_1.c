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

int f_gold ( int arr [ ], int n, int k ) {
  if ( k > n ) return - 1;
  int sum = arr [ 0 ];
  for ( int i = 1;
  i < k;
  i ++ ) sum += arr [ i ];
  int max_sum = sum, max_end = k - 1;
  for ( int i = k;
  i < n;
  i ++ ) {
    int sum = sum + arr [ i ] - arr [ i - k ];
    if ( sum > max_sum ) {
      max_sum = sum;
      max_end = i;
    }
  }
  return max_end - k + 1;
}


int f_filled ( int arr [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,5,11,37,41,49,49,63,98};
int param0_1[] = {84,-72,12,0,86,-32,-18,48,60,42,8,-6,-10,-6,-52,-84,-98,76,-10,-14,-94,-48,94,-10,-20,40,-52,0,94,-68,44,-34,-26,-6,-94,34,-80,-62,-40,56,52,-20,74,-46,-88,-26,22};
int param0_2[] = {0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {94,97,74,88,14,66,65,50,76,55,70,93,53,30,2,60,65,24,80,73,84,95,49,32,55,70,17,26,96,20,36,2,89,49,83,67,42,51,71,11,61,78,17,78,94,68};
int param0_4[] = {-98,-90,-60,-38,38,42};
int param0_5[] = {1,0,0,1,1,1,1};
int param0_6[] = {4,9,17,17,19,32,35,36,37,40,44,45,47,48,48,56,56,60,61,65,66,79,83,91,93,99};
int param0_7[] = {78,82,-92,-46,-16,-64,28,60,64,52,54,-84,70,22,24,0,-14,20,-90,30,0,86,12,72,-64,-52,86,16,-42};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {81,77,6,3,72,24,75,47,17,29,69,15,15,50,30,83,11,7,59,7,12,82,45,76,9,48,98,49,29,66,3,53,37,13,72,58,37,87,55};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {8,34,11,35,3,3,22,25,25,34};
    int param2[] = {7,43,18,33,5,4,24,27,20,23};
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