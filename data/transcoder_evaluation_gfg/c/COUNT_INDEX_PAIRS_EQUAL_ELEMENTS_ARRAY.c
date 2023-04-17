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
  int ans = 0;
  for ( int i = 0;
  i < n;
  i ++ ) for ( int j = i + 1;
  j < n;
  j ++ ) if ( arr [ i ] == arr [ j ] ) ans ++;
  return ans;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,6,9,16,16,21,36,41,58,60,62,73,77,81,95};
int param0_1[] = {-86,-72,-26,-34,18,-62,-66};
int param0_2[] = {1};
int param0_3[] = {16};
int param0_4[] = {-88,-80,-72,-68,-64,-26,4,14,16,22,30,32,60,74,82};
int param0_5[] = {0,0,1,1,1,0,1,0,0,0,1};
int param0_6[] = {3,9,10,12,17,23,27,29,42,44,59,61,71,76,78,82,84,84,89,90,93,93,97,97};
int param0_7[] = {68,-40,-46,-20,-64,90};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {99,17,94,43,97,17,11,58,75,94,37,22,54,31,41,4,55,69,92,80,45,97,16,33,36,17,43,82,81,64,22,65,85,44,47,14};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {12,3,0,0,11,9,15,5,15,23};
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