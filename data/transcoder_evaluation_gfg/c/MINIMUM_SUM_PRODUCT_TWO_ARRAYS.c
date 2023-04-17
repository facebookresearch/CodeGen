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

int f_gold ( int a [ ], int b [ ], int n, int k ) {
  int diff = 0, res = 0;
  int temp;
  for ( int i = 0;
  i < n;
  i ++ ) {
    int pro = a [ i ] * b [ i ];
    res = res + pro;
    if ( pro < 0 && b [ i ] < 0 ) temp = ( a [ i ] + 2 * k ) * b [ i ];
    else if ( pro < 0 && a [ i ] < 0 ) temp = ( a [ i ] - 2 * k ) * b [ i ];
    else if ( pro > 0 && a [ i ] < 0 ) temp = ( a [ i ] + 2 * k ) * b [ i ];
    else if ( pro > 0 && a [ i ] > 0 ) temp = ( a [ i ] - 2 * k ) * b [ i ];
    int d = abs ( pro - temp );
    if ( d > diff ) diff = d;
  }
  return res - diff;
}


int f_filled ( int a [ ], int b [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {8,9,9,16,19,21,24,26,26,27,31,33,36,44,46,47,69,71,72,74,74,74,74,76,76,77,89,91,91};
int param0_1[] = {-64,-58,26,-42,-18,-52,26,-70,0,-68,38,-98,-14,-92,-74,-90,86,-76,-8,-80,-80,54,-26,-56,48,86,-60};
int param0_2[] = {0,0,0,0,1,1,1,1};
int param0_3[] = {62,73,67,96,95,31,58,13,63,13,29,97,7,36,13,54,67,8,9,36,6,29,92,7,82,5,27,65,80,20,22,1,11,67,23,31,86,27,53,87,39,99,69};
int param0_4[] = {-86,-82,-42,-30,-12,-4,14,16,20,20,22,26,30,40,46,48,48,50,60,60,66,70,74,76,90,96,96,98};
int param0_5[] = {1,1,1,0,1,0,0,1,1,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,1,1,1,1,1,0,0,1};
int param0_6[] = {4,7,14,14,30,38,44,49,51,53,54,56,58,62,67,76,86,86,88,91,95};
int param0_7[] = {2,90,-92,58,56,94,12,-2,86,-70,46,-80,42,-6,72,-52,4,96,-42,50,-28,42,8,26,46,70,-2,-24,-36,50,26,70,74,-52,34,-88,-66,74,52,62,-24,-80,40,42,90};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {61,96,7,59,86,74,7,95,13,52,18,77,25,97,74,18};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {1,8,10,10,12,16,17,19,20,20,23,33,37,38,58,66,69,70,70,76,79,80,83,84,84,86,87,87,93};
int param1_1[] = {90,-2,-8,12,-58,46,-54,-40,-10,-76,-62,66,42,-66,4,-6,50,8,-18,92,-42,30,-34,74,-86,-56,52};
int param1_2[] = {0,0,0,0,0,1,1,1};
int param1_3[] = {88,64,94,64,4,23,6,85,92,68,78,53,96,88,69,28,12,34,92,67,39,68,72,64,10,14,26,61,96,1,79,87,45,9,16,70,63,84,79,63,11,85,46};
int param1_4[] = {-98,-78,-68,-68,-64,-40,-38,-38,-26,-12,-6,0,2,8,18,34,52,58,64,64,70,72,76,82,84,90,96,96};
int param1_5[] = {1,0,0,0,0,1,0,0,0,1,1,0,0,1,1,0,0,1,1,0,1,0,1,0,0,1,0,1,1,0,0,0};
int param1_6[] = {2,2,7,19,20,21,22,26,42,45,46,46,59,63,63,72,73,74,77,83,89};
int param1_7[] = {98,62,-52,-92,-14,-92,62,86,20,36,-80,-12,-38,70,-28,-28,42,-10,94,-16,-72,-96,76,-14,-18,-12,38,14,46,16,-90,10,-34,-6,-34,-62,96,14,0,-10,32,-6,96,-72,-2};
int param1_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_9[] = {56,38,75,57,82,30,38,79,39,73,74,73,36,10,80,50};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {20,20,7,23,14,20,11,25,46,13};
    int param3[] = {28,16,5,23,14,16,17,25,33,12};
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