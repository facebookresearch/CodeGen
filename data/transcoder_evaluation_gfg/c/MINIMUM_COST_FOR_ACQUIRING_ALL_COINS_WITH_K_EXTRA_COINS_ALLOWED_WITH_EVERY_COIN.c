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

int f_gold ( int coin [ ], int n, int k ) {
  sort ( coin, coin + n );
  int coins_needed = ceil ( 1.0 * n / ( k + 1 ) );
  int ans = 0;
  for ( int i = 0;
  i <= coins_needed - 1;
  i ++ ) ans += coin [ i ];
  return ans;
}


int f_filled ( int coin [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,4,5,9,10,10,11,14,15,19,21,22,29,36,36,38,39,39,39,41,41,42,45,45,48,55,56,57,64,66,66,66,66,69,74,76,80,81,82,82,85,87,95,95};
int param0_1[] = {-6,-52,20,-98,-10,48,36,66,-88,94,68,16};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {91,62,29,49,6,11,10,43,78,35,32,5,1,48,15,24,4,71};
int param0_4[] = {-98,-92,-88,-84,-82,-78,-74,-74,-68,-62,-62,-56,-56,-50,-46,-44,-26,-18,-14,-8,-8,-6,8,16,20,20,22,26,36,42,44,44,52,60,66,68,68,70,76,84};
int param0_5[] = {1,0,0,0,1,1,1,0,1,0,0,0,0,0,0,1,1,0,1,1,0,1,0,1,1,1,0,1,1,1,1,0,0,0,1,1,0,1,1,0,0,1,0};
int param0_6[] = {5,12,38,39,52,54,62,81,87,93};
int param0_7[] = {86,-18,-32,70,40,-76,-8,8,-84,-10,92,94,-18,-12,-26,-40,-74,60,16,-70,44,-32,40,-24,0,4};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {86,62,98,97,61,31,23,56,63,72,44,74,58,97};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {33,6,16,13,25,32,6,25,37,12};
    int param2[] = {27,10,16,17,34,32,8,20,29,13};
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