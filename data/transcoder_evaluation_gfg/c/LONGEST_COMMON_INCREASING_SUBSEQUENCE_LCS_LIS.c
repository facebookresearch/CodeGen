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

int f_gold ( int arr1 [ ], int n, int arr2 [ ], int m ) {
  int table [ m ];
  for ( int j = 0;
  j < m;
  j ++ ) table [ j ] = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    int current = 0;
    for ( int j = 0;
    j < m;
    j ++ ) {
      if ( arr1 [ i ] == arr2 [ j ] ) if ( current + 1 > table [ j ] ) table [ j ] = current + 1;
      if ( arr1 [ i ] > arr2 [ j ] ) if ( table [ j ] > current ) current = table [ j ];
    }
  }
  int result = 0;
  for ( int i = 0;
  i < m;
  i ++ ) if ( table [ i ] > result ) result = table [ i ];
  return result;
}


int f_filled ( int arr1 [ ], int n, int arr2 [ ], int m ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,7,9,35,43,51,51,66,88};
int param0_1[] = {-52,52,-92,-46,-94,30,-36,18,-98,22,-36,96,-88,-50,50};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {5,74,29};
int param0_4[] = {-84,-74,-70,-62,-56,-56,-52,-2,6,24,28,44,44,52};
int param0_5[] = {0,0,0,1,0,1,0,0,1,1,1,1,0,0,1,0,1,0,1,1,0,0,1,0,1,1,0,0,1,0};
int param0_6[] = {3,4,4,7,15,15,16,22,32,32,37,39,39,41,43,46,47,47,49,75,79,80,86,88,93};
int param0_7[] = {70,-64,0,52,32,-98,38,-8,34,70,98,58,-48,-60,-28,-22,-72,82,-98,-36};
int param0_8[] = {0,0,1,1,1,1,1,1};
int param0_9[] = {46,87,98};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {5,7,36,1,8,17,19,16,7,2};
    int param2_0[] = {10,21,38,50,65,67,87,93,99};
int param2_1[] = {-58,40,56,-62,-92,-94,40,18,-2,-76,-78,-14,44,84,4};
int param2_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param2_3[] = {57,33,48};
int param2_4[] = {-98,-96,-88,-66,-32,-26,-24,-20,-4,20,48,74,90,96};
int param2_5[] = {1,0,1,1,0,0,0,0,1,1,1,0,1,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1,1,0};
int param2_6[] = {9,12,15,20,22,27,28,28,30,31,35,39,47,58,58,60,73,74,76,78,80,86,95,96,98};
int param2_7[] = {-18,88,-40,-52,30,-10,-18,-56,84,-22,-64,80,-14,-64,40,92,48,-8,24,82};
int param2_8[] = {0,1,1,1,1,1,1,1};
int param2_9[] = {67,31,54};
int *param2[10] = {param2_0,param2_1,param2_2,param2_3,param2_4,param2_5,param2_6,param2_7,param2_8,param2_9};
    int param3[] = {8,10,22,1,12,15,14,12,7,2};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i]) == f_gold(param0[i],param1[i],param2[i],param3[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}