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

int f_gold ( int arr [ ], int n, int x ) {
  int curr_sum = 0, min_len = n + 1;
  int start = 0, end = 0;
  while ( end < n ) {
    while ( curr_sum <= x && end < n ) curr_sum += arr [ end ++ ];
    while ( curr_sum > x && start < n ) {
      if ( end - start < min_len ) min_len = end - start;
      curr_sum -= arr [ start ++ ];
    }
  }
  return min_len;
}


int f_filled ( int arr [ ], int n, int x ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {6,11,11,14,18,19,21,22,22,23,26,27,28,28,29,30,31,34,39,42,42,44,45,49,49,53,57,61,65,66,67,70,71,73,74,74,78,85,88,94,95,97};
int param0_1[] = {-30,-22,-66,-80,18,-64,-28,-46,94,60,-64,2,26,-94,58,56,56,88,50,-78,-12,68,54,-78,42,-30,24,-48,84,12,-88,0,54,-92,-4,42,-60,-72,-32};
int param0_2[] = {0,0,0,0,0,0,0,1,1,1,1,1,1,1,1};
int param0_3[] = {86,8,23,40,55,93,11,35,33,37,96,91,35,66,37,57,83,99,96,15,18,93};
int param0_4[] = {-92,-68,-48,-48,-42,-26,-22,-18,2,4,8,14,20,22,32,46,52,62,70,96,98};
int param0_5[] = {0,0,0,0,1,0,1,1,0,1,0,0,0};
int param0_6[] = {4,4,11,11,13,15,16,18,19,19,19,23,26,27,34,39,39,40,41,46,47,51,52,52,53,57,58,58,60,64,68,70,72,84,84,85,95,98,99};
int param0_7[] = {12,-22,2,-90,-92,84,-26,-76,-72,50,-36,30,78,-18,-94,-30,22,28,10,32,34,-86,0,-4,40,0,80,50,66,-48,-40,-94,64,58,-14,0,-32,-58,-22,-94,-68,-36,-94,-48,40,78,-74};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {1,33,20,32,76,27,8,95,78,72,25,56};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {37,31,8,16,17,11,31,42,25,9};
    int param2[] = {23,29,12,13,14,10,35,26,21,10};
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