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
  unordered_map < int, int > h;
  for ( int i = 0;
  i < n;
  i ++ ) h [ arr [ i ] ] ++;
  if ( len(h) < k ) return - 1;
  int dist_count = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( h [ arr [ i ] ] == 1 ) dist_count ++;
    if ( dist_count == k ) return arr [ i ];
  }
  return - 1;
}


int f_filled ( int arr [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {17,25,27,27,73,91};
int param0_1[] = {-86,-74,-88,28,-32,20,-34,32};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {5,11,36,27,6,24,58,44,14,68};
int param0_4[] = {-98,-98,-94,-92,-86,-86,-70,-66,-64,-64,-58,-52,-46,-44,-44,-38,-38,-28,-24,-12,-10,-4,-2,2,8,10,12,20,22,26,26,36,42,52,54,60,60,68,82,82,92,98};
int param0_5[] = {0,1,0,0,1,1,1,0,0,0,1,1,1,0,0,1,1,1,0,0,0,1,0,0,1,0,1,1,1,1};
int param0_6[] = {3,8,9,10,10,13,14,16,18,23,24,25,27,28,30,33,36,39,42,42,44,45,45,48,52,52,55,55,59,59,59,60,61,61,66,66,67,68,71,72,75,76,79,80,94,94};
int param0_7[] = {-12,56,-48,52,-96,-84,32,-12,-6,82,70,18,66,-6,-22,-46,-54,18,-14,-32,68,82,-44,-42,10,56,8,-56,24,20,-38,30,-52,-66,82,-64,68,-82,52,-88,-34,-26,94,58,-4,-84,-60};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {1,23,75,84,28,34,15,13,51,69,94,45,38,38};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {5,5,33,7,27,27,44,37,22,13};
    int param2[] = {3,6,32,5,27,20,26,46,21,12};
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