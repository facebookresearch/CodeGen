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
  int diff = INT_MAX;
  for ( int i = 0;
  i < n - 1;
  i ++ ) if ( arr [ i + 1 ] - arr [ i ] < diff ) diff = arr [ i + 1 ] - arr [ i ];
  return diff;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {3,25,44,46,54,60,81};
int param0_1[] = {82,68,-98,-66,-36,-42,98,-38,58,-6,-28,70,-24,18,16,10,92,44,28,-96,-72,24,28,-80,-4,38,88,76};
int param0_2[] = {1,1,1};
int param0_3[] = {87,25,80,45,44,20,48,47,51,54,68,47,89,95,15,29,5,45,2,64,53,96,94,22,23,43,61,75,74,50};
int param0_4[] = {-74,-48,-42,-26,-16,-12,0,4,8,18,46,46,62,70,74,88,92,96,98};
int param0_5[] = {0,1,1,1,0,1,1,0,0,1,1,1,0,0,1,1,0,1,0,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0};
int param0_6[] = {27,42,59,80};
int param0_7[] = {-96,-94,10,-36,18,-40};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_9[] = {96};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {3,22,2,15,18,36,2,4,12,0};
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