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

double f_gold ( vector < int > & A, int K ) {
  int n = len(A);
  double pre_sum [ n + 1 ];
  pre_sum [ 0 ] = 0;
  for ( int i = 0;
  i < n;
  i ++ ) pre_sum [ i + 1 ] = pre_sum [ i ] + A [ i ];
  double dp [ n ] = {
    0 };
    double sum = 0;
    for ( int i = 0;
    i < n;
    i ++ ) dp [ i ] = ( pre_sum [ n ] - pre_sum [ i ] ) / ( n - i );
    for ( int k = 0;
    k < K - 1;
    k ++ ) for ( int i = 0;
    i < n;
    i ++ ) for ( int j = i + 1;
    j < n;
    j ++ ) dp [ i ] = max ( dp [ i ], ( pre_sum [ j ] - pre_sum [ i ] ) / ( j - i ) + dp [ j ] );
    return dp [ 0 ];
  }
  

double f_filled ( vector < int > & A, int K ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,11,14,27,32,37,39,49,52,53,57,62,67,67,68,69,76,77,78,81,85,85,87,91,91,91,99,99,99};
int param0_1[] = {80,12,32,44,24,82,-40,42,26,36,58,52,-34,44,12,-18,-72,52,2,-8,22,-18,98,-60,62,92,-46,20,20,-46,52,94,0,-28,-22,80,26,-92,-50,48,-80};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {32,16,67,53,99,56,80,92,84,21,36,46,94,31,63,67,59,88,41,17,74,47,95,12,27,99,32,4,82,31,65,40,93,72,23,33,93,9,62,47};
int param0_4[] = {-92,-86,-80,-78,-72,-70,-70,-68,-66,-62,-60,-54,-54,-52,-52,-40,-36,-32,-28,-26,-22,-22,-20,-16,-16,-8,0,6,8,10,14,18,20,42,46,52,60,66,68,70,74,86,88,88,92,94,98};
int param0_5[] = {1,0,0,0,1,0,1,1,0,1,0,1,1,1,1,0,1,0,0};
int param0_6[] = {1,1,3,3,6,7,10,11,12,13,16,16,22,23,24,27,28,30,30,30,31,33,35,35,39,40,41,52,52,58,59,60,61,61,66,66,71,73,74,75,75,76,80,83,85,95,96,97,97};
int param0_7[] = {28,-52,48,96,54,94,60,18};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {26,80,12,87,90,98,46,91,38,46,20,64,53,4,60,87,44,88,22,30};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {24,26,15,36,36,16,34,7,31,19};
    for(int i = 0; i < len(param0); ++i)
    {
        if(abs(1 - (0.0000001 + abs(f_gold(param0[i],param1[i])) )/ (abs(f_filled(param0[i],param1[i])) + 0.0000001)) < 0.001)
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}