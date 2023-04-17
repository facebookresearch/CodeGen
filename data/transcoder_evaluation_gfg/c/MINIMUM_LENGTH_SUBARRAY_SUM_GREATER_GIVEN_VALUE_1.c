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
    while ( curr_sum <= x && end < n ) {
      if ( curr_sum <= 0 && x > 0 ) {
        start = end;
        curr_sum = 0;
      }
      curr_sum += arr [ end ++ ];
    }
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
    int param0_0[] = {2,4,5,10,14,15,16,20,23,28,31,35,36,36,43,48,49,55,57,57,58,61,64,64,68,70,70,73,74,76,76,77,81,81,82,87,89,92,99};
int param0_1[] = {66,-20,12,-48,22,28,40,-30,-6,-96,10,-88,40};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {28,19,38,31,17,27,60,35,19,47,34,51,3,95,33,29,84,46,74,87};
int param0_4[] = {-48,-2};
int param0_5[] = {1,1,0,1,1,1,1,0,1,0,1,1,0,1,1,0,1,1,0,1,1,1};
int param0_6[] = {1,4,4,6,8,10,12,12,13,15,18,20,21,23,25,28,28,33,33,35,35,36,37,38,42,44,63,63,65,65,65,66,70,74,77,78,80,80,84,87,87,89,92,93,94,97,98,99};
int param0_7[] = {-82,-12,-40,58,22,-76,-94,-28,42,36,64};
int param0_8[] = {0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_9[] = {76,65,96,76,1,91,22,29,95,21,73,68,30,52,73,86,52,66,67,37,76,53,68,6,95,81,98,42,63,38,92,78,59,86,10,38,18,15,52,62,16,66};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {33,11,42,15,1,12,42,10,10,23};
    int param2[] = {28,12,23,15,1,15,27,6,14,35};
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