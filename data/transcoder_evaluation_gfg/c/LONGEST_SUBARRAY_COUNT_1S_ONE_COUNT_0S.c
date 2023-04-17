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
  unordered_map < int, int > um;
  int sum = 0, maxLen = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    sum += arr [ i ] == 0 ? - 1 : 1;
    if ( sum == 1 ) maxLen = i + 1;
    else if ( um . find ( sum ) == um . end ( ) ) um [ sum ] = i;
    if ( um . find ( sum - 1 ) != um . end ( ) ) {
      if ( maxLen < ( i - um [ sum - 1 ] ) ) maxLen = i - um [ sum - 1 ];
    }
  }
  return maxLen;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {6,10,31,35};
int param0_1[] = {4,88,-72,28,-54,32,-34};
int param0_2[] = {0,0,0,1,1,1,1,1,1};
int param0_3[] = {39,22,15,10,34,87,46,83,74,77,61,90,43,67,64,72,92,52,68,53,67,32,82,76,76,47,74,47,8,80,85,58,75};
int param0_4[] = {-82,-58,-50,-30,-14,-4,-2,-2,0,22,36,58,70,80,80,82,84,90};
int param0_5[] = {1,0,1,0,0,1,1,1,0,0,1};
int param0_6[] = {4,11,17,21,21,22,30,31,36,37,39,40,45,46,47,48,52,53,53,60,60,65,66,66,67,67,87,88,91,97};
int param0_7[] = {-4,-60,-78,-50,64,18,0,76,12,86,-22};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_9[] = {4,39,50,37,71,66,55,34,1,41,34,99,69,31};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {2,6,4,26,14,7,29,7,17,11};
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