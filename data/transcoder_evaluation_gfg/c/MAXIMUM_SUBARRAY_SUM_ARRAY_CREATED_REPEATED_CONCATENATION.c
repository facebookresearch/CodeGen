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
  int max_so_far = INT_MIN, max_ending_here = 0;
  for ( int i = 0;
  i < n * k;
  i ++ ) {
    max_ending_here = max_ending_here + a [ i % n ];
    if ( max_so_far < max_ending_here ) max_so_far = max_ending_here;
    if ( max_ending_here < 0 ) max_ending_here = 0;
  }
  return max_so_far;
}


int f_filled ( int a [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {5,6,12,20,23,28,33,37,47,51,53,56,63,65,65,68,69,76,76,78,83};
int param0_1[] = {68,10,52,-44,34,-4,-34,2,50,-60,50,94,-98,-98,-44,-36,-4,-62,-2,-92,-70,-48,-78,-10,94};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {71,59,21,82,73,29,30,25,21,10,85,22,60,43,49,20,34,39,69,6,44,27,50,33,57,29,65,18,68,56,50,28};
int param0_4[] = {-84,-74,-74,-56,-54,-48,-48,-46,-42,-34,-32,-30,-18,-16,-16,6,12,20,24,26,30,32,34,42,42,42,44,46,46,50,50,62,72,78,90};
int param0_5[] = {0,1,1,1,1,1,1,1,1,0,1,1,0,0,1,1,0,1,1,1,0,1,1,0,0,0,1,1,1,0};
int param0_6[] = {3,7,11,11,26,60,68,71,77,91,95};
int param0_7[] = {28,48,-86,-52,6,4,30,18,-32,60,-2,16,-88,-36};
int param0_8[] = {1};
int param0_9[] = {76};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {18,22,34,23,17,16,8,8,0,0};
    int param2[] = {20,22,29,30,23,25,10,11,0,0};
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