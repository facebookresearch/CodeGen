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
  sort ( arr, arr + n );
  int minXor = INT_MAX;
  int val = 0;
  for ( int i = 0;
  i < n - 1;
  i ++ ) {
    val = arr [ i ] ^ arr [ i + 1 ];
    minXor = min ( minXor, val );
  }
  return minXor;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {8,11,12,27,32,32,36,56,57,66,68,70,74,78,82,83,96};
int param0_1[] = {40,48,66,4,-60,42,-8,38};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {98,6,82,95,87,20,11,63,78,70,37,12,57,67,10,49,38,28,86,7,61,50,32,68,91,66,57,29,2,64,65,15,16,4,7,76,44,52,81,89,3,36,57,95,48,24};
int param0_4[] = {-88,-84,-76,-58,-40,-38,-28,-24,-20,-14,-12,16,20,28,28,30,40,44,56,58,60,92,92};
int param0_5[] = {0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,0,1,1,0,1,0};
int param0_6[] = {6,6,19,31,41,45,49,56,78,96,98};
int param0_7[] = {62,-90,22,-84,-4};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {83,13,43,99,34,74,56,20,93,65,92,58,91,72,37,10,39,7,29,69,42,28};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {10,7,19,36,13,20,6,3,21,14};
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