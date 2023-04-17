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

int f_gold ( int arr [ ], int N, int k ) {
  int M, S = 0, S1 = 0, max_difference = 0;
  for ( int i = 0;
  i < N;
  i ++ ) S += arr [ i ];
  sort ( arr, arr + N, greater < int > ( ) );
  M = max ( k, N - k );
  for ( int i = 0;
  i < M;
  i ++ ) S1 += arr [ i ];
  max_difference = S1 - ( S - S1 );
  return max_difference;
}


int f_filled ( int arr [ ], int N, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,5,5,9,9,19,22,24,27,33,39,39,40,41,42,43,44,45,48,52,52,53,53,55,55,56,57,57,60,60,61,62,65,66,67,70,71,72,73,77,78,79,84,87,89,91,95,98};
int param0_1[] = {-22,-28};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {63,72,2,94,89,11,95,79,90,9,70,28,25,74,16,36,50,91,38,47,47,13,27,29,31,35};
int param0_4[] = {-86,-78,-76,-76,-66,-62,-62,-38,-34,-32,-30,-26,-22,-4,-4,2,8,8,10,22,52,52,58,64,66,66,66,70,82,82};
int param0_5[] = {0,0,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1,0,1,1,0,0,0,1,0,0,1,0,0};
int param0_6[] = {1,2,2,9,9,12,13,26,26,33,34,35,51,57,70,79,83};
int param0_7[] = {98,-72,2,40,-20,-14,42,8,14,-58,-18,-70,-8,-66,-68,72,82,-38,-78,2,-66,-88,-34,52,12,84,72,-28,-34,60,-60,12,-28,-42,22,-66,88,-96};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {21,85,64,20,4,5,2};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {41,1,20,23,29,42,9,28,37,5};
    int param2[] = {44,1,29,16,24,32,16,28,27,6};
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