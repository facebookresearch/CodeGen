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

int f_gold ( int arr [ ], int N, int K ) {
  sort ( arr, arr + N );
  int res = INT_MAX;
  for ( int i = 0;
  i <= ( N - K );
  i ++ ) {
    int curSeqDiff = arr [ i + K - 1 ] - arr [ i ];
    res = min ( res, curSeqDiff );
  }
  return res;
}


int f_filled ( int arr [ ], int N, int K ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,1,4,18,21,35,37,39,76,81,86,92,96};
int param0_1[] = {-8,-6,62,52,-86,2,-94,0,-48,-38,24,-48,34};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {23,36,43,50,74,81,94,13,30,57,30,71,10,99,66,94,83,39,37,3,89,34};
int param0_4[] = {-96,-94,-92,-84,-80,-72,-24,-22,-18,-14,6,8,26,28,30,36,50,58,80,84,92,92};
int param0_5[] = {0,0,0,0,0,0,1,1,0,1,1,1,1,0,1,0,0,1,1,0,0,1,1};
int param0_6[] = {6,7,9,27,30,42,54,55,57,57,59,76,84,84,84};
int param0_7[] = {88,44,-96,-72,-80,0,-64,-64,-68,4,38,4,-38,68,-54,92,-16,62,24,54,0,54,62,-70,80,-12,84,-16,-10,88,-30,-56,48,50,-24,94,40,28,-86,-12};
int param0_8[] = {0,1};
int param0_9[] = {89,18,7,54,67,93,10,61,59,59,69,63,98,8,78,55,6,1,56,97,75,88,10};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {7,9,16,17,21,21,13,31,1,22};
    int param2[] = {6,12,26,20,12,22,14,26,1,14};
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