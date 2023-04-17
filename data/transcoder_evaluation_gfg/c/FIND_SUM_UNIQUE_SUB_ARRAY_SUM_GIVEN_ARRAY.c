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

long long int f_gold ( int arr [ ], int n ) {
  int res = 0;
  unordered_map < int, int > m;
  for ( int i = 0;
  i < n;
  i ++ ) {
    int sum = 0;
    for ( int j = i;
    j < n;
    j ++ ) {
      sum += arr [ j ];
      m [ sum ] ++;
    }
  }
  for ( auto x : m ) if ( x . second == 1 ) res += x . first;
  return res;
}


long long int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {7,24,34,35,36,40,49,51,53,74,78};
int param0_1[] = {-34,60,32};
int param0_2[] = {0};
int param0_3[] = {80,64,10,82,14,75,51,91,1,25,98,22,36,27,21,31,93,6,52,91,80,8,62,95,10,71,40,80,35,86,85,26,74,72,64,88,4,71,4,16};
int param0_4[] = {-94,-46,-36,-24,-22,0,10,14,34,34,90,92,98};
int param0_5[] = {1,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,1,0,0,0,0,0,1,1,0,1,1,1,1,1,1,0,0,0,1,0,1,0,1};
int param0_6[] = {19,20,20,24,25,33,43,47,57,61,61,64,65,71,72,73,75,82,90,93,95};
int param0_7[] = {-6,56,58,-36,70,-92,30,58,-40,98,80,-96,-4,-88,34,76,40,-32,-94,-26,8,72,-56,-96,-88,-24,36,14,-88,-32,90,4,-88,28,18};
int param0_8[] = {0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {91,51,15,78,55,3,10,24,42,84,66,78,10,41,21,53,69,57,20,22,50,72,8,80,12,91,29,95,38,74,95,26,10,57,51,25,49,74,15,42,99,21,27};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {9,2,0,31,9,21,15,24,11,36};
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