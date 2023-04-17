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
  unordered_map < int, int > vis;
  for ( int i = 0;
  i < n;
  ++ i ) vis [ arr [ i ] ] = 1;
  int k = len(vis);
  vis . clear ( );
  int ans = 0, right = 0, window = 0;
  for ( int left = 0;
  left < n;
  ++ left ) {
    while ( right < n && window < k ) {
      ++ vis [ arr [ right ] ];
      if ( vis [ arr [ right ] ] == 1 ) ++ window;
      ++ right;
    }
    if ( window == k ) ans += ( n - right + 1 );
    -- vis [ arr [ left ] ];
    if ( vis [ arr [ left ] ] == 0 ) -- window;
  }
  return ans;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {13,39,49,52,53,69,72,79,83,96};
int param0_1[] = {-98,-98,22,-10,-28,0,56,72,36,88,96,22,90,74,-60,-64,0,2,-42,0,94,-82,-74};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {35,23,41,58,66,92,3,33,78,70,80,86,21,21,74,19};
int param0_4[] = {-98,-80,-52,-10,4,76};
int param0_5[] = {1,0,0,0,1,0,0,0,1,1,0,0,0,1,0,1,0,1,0,0,1,1,1,0,0,1,0,1,0,1,1,1,0,0,0,1,1,0,1,1,1,1};
int param0_6[] = {2,7,10,17,26,36,37,85,87,88};
int param0_7[] = {64,-2,-94,-84,-48,86};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {91,49,94,81,64,5,13,70,82,9,80,82};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {5,20,26,12,3,36,8,5,20,9};
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