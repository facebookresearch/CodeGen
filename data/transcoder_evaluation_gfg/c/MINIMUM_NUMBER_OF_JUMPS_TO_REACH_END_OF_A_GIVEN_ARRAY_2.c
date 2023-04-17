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
  int * jumps = new int [ n ];
  int min;
  jumps [ n - 1 ] = 0;
  for ( int i = n - 2;
  i >= 0;
  i -- ) {
    if ( arr [ i ] == 0 ) jumps [ i ] = INT_MAX;
    else if ( arr [ i ] >= n - i - 1 ) jumps [ i ] = 1;
    else {
      min = INT_MAX;
      for ( int j = i + 1;
      j < n && j <= arr [ i ] + i;
      j ++ ) {
        if ( min > jumps [ j ] ) min = jumps [ j ];
      }
      if ( min != INT_MAX ) jumps [ i ] = min + 1;
      else jumps [ i ] = min;
    }
  }
  return jumps [ 0 ];
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,6,7,14,22,32,42,42,43,48,54,57,59,69,84,92,98};
int param0_1[] = {98,-66,-70,-64,-88,-76,-90,16,58,68,-10,-42,-28,10,72,68,-30,60,92,-56,80,-4,-82,30,58,98,-56,98,-14,-38,-20,-74,-46,-22,78,36,-54,-64,80,-10,-26,82,96,-72,-36,-36,-32,-88,0};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {64,25,63,54,7,43,79,27,34,13,84,80,34,48,5,56,67,2};
int param0_4[] = {2,28,68};
int param0_5[] = {1,0,0,0,0,1,1,1,1,0,1,0,0};
int param0_6[] = {1,1,9,16,17,18,19,20,21,22,25,28,29,29,36,37,40,40,42,48,49,49,55,63,65,66,69,70,72,73,76,77,77,79,79,81,81,93,95,99};
int param0_7[] = {38,-42,-8,98,-90,38,88,-8,70,-28,-50,-22,28,24,88,-26,58,48,6,0,68,-6,8,54,-2,46,-44,96,-82,-14,-48,-18,-16,-48,-44,-16,-58,-64};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {98,46,12,55,57,11,25,64,92,35,90,72,95,30,75,67,64,12,31,84,70,96,71,80,62,34,70,10,54};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {11,26,41,10,2,11,24,34,14,25};
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