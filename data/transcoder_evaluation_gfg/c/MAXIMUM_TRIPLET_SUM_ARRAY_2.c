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
  int maxA = INT_MIN, maxB = INT_MIN, maxC = INT_MIN;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( arr [ i ] > maxA ) {
      maxC = maxB;
      maxB = maxA;
      maxA = arr [ i ];
    }
    else if ( arr [ i ] > maxB ) {
      maxC = maxB;
      maxB = arr [ i ];
    }
    else if ( arr [ i ] > maxC ) maxC = arr [ i ];
  }
  return ( maxA + maxB + maxC );
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,7,12,21,22,25,27,28,28,31,32,32,41,45,47,51,53,60,61,61,63,71,74,82,83,85,88,92,96,96};
int param0_1[] = {-52,26,74,-62,-76};
int param0_2[] = {0,0,0,0,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {63,71,15,28,31,84,8,17,24,42,66,95,30};
int param0_4[] = {-94,-92,-92,-90,-88,-88,-86,-82,-80,-78,-66,-54,-52,-52,-46,-46,-42,-36,-32,-24,-24,-14,-14,-14,-12,-10,0,6,8,20,24,24,28,38,38,52,54,56,64,74,74,76,82,94,94};
int param0_5[] = {0,0,0,1,1,0,1,0,1,1,0,1,0,1,0,0,0,1,0,1,1,1,0,1,0,0,0,0,1,1,0,0,0,0,1,0,1,1,0,1,0,0,0,1,0};
int param0_6[] = {15,19,80};
int param0_7[] = {4,80,18,74,36,-30,-72,-28,-32,-16,-8,38,78,-48,98,-64,86,-60,-44,84,-98,40,14,30,44,90,-30,-42,24,-28,24,40,-96,98,90,-68,-54,-52,62,34,-98,68,-56,-94,-78,-12,28};
int param0_8[] = {0,1,1,1,1,1};
int param0_9[] = {2,18,96,7,99,83,3,88,23,77,6,28,55,49,69,55,48,76,43,11,43,44,17,74,27,64,76,77,53,26,73,12,19,62,18,34,13,31,97,96,85,27,30,97,89,25};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {28,2,11,6,31,30,2,41,3,41};
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