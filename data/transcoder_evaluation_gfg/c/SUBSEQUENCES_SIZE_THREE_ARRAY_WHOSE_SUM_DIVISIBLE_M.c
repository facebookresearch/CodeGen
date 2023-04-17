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

int f_gold ( int A [ ], int N, int M ) {
  int sum = 0;
  int ans = 0;
  for ( int i = 0;
  i < N;
  i ++ ) {
    for ( int j = i + 1;
    j < N;
    j ++ ) {
      for ( int k = j + 1;
      k < N;
      k ++ ) {
        sum = A [ i ] + A [ j ] + A [ k ];
        if ( sum % M == 0 ) ans ++;
      }
    }
  }
  return ans;
}


int f_filled ( int A [ ], int N, int M ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {14,35,56,70,88};
int param0_1[] = {-50,-92,16,-68,-36};
int param0_2[] = {0,0,0,1,1,1};
int param0_3[] = {76,43,22,41,49,99,25,40,3,45,60,16,83,62,26,93,64,73,72,53,6,32,35,67,17};
int param0_4[] = {-90,-86,-86,-66,-50,-48,-44,-42,-42,-38,-24,-22,-20,-18,-8,8,24,28,34,48,60,62,66,68,74,76,80,82,88};
int param0_5[] = {1,1,1,0,0,1,0,1,0,1,1,0,0,1,1,0,1,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,1,0,1,1,0};
int param0_6[] = {4,5,8,9,10,12,13,16,17,18,21,21,25,27,28,30,36,36,54,55,56,57,60,62,67,67,68,71,72,72,73,73,77,77,83,86,86,86,87,89,92,92,96,97,97,98};
int param0_7[] = {-64,52,-32,38,8,-62,-56,20,72,-12,32,44};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {77,68,45,6,27,19,29,95,21,2,39,48,72,67,49,45,1,16,56,78,25,22,27,40,31,34,26,35,12};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {3,3,4,14,24,24,24,6,12,25};
    int param2[] = {4,4,5,21,20,30,23,6,15,25};
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