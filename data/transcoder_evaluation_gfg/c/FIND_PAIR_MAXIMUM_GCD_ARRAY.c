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
  int high = 0;
  for ( int i = 0;
  i < n;
  i ++ ) high = max ( high, arr [ i ] );
  int divisors [ high + 1 ] = {
    0 };
    for ( int i = 0;
    i < n;
    i ++ ) {
      for ( int j = 1;
      j <= sqrt ( arr [ i ] );
      j ++ ) {
        if ( arr [ i ] % j == 0 ) {
          divisors [ j ] ++;
          if ( j != arr [ i ] / j ) divisors [ arr [ i ] / j ] ++;
        }
      }
    }
    for ( int i = high;
    i >= 1;
    i -- ) if ( divisors [ i ] > 1 ) return i;
  }
  

int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {3,3,8,10,12,13,14,16,16,19,20,21,25,29,33,35,35,35,35,36,38,41,42,45,45,45,46,48,51,52,53,55,56,57,58,62,69,73,73,76,76,80,89,91,92,93,93,96};
int param0_1[] = {12,52,-66,50,50,-78,-14,26,56,74,8,-58,58,-66,-58,-12,80};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {23,98,12,45,83,85,30,92,26,12,38,20,86,52,71,20,56,78,10,34,86,55,99,84,26,2,1,89,60,26,16,37,98,11,73,42,36,60,28};
int param0_4[] = {-98,-84,-80,-72,-66,-64,-52,-36,-28,-18,-12,-12,-4,8,12,40,42,56,68,70,90,94};
int param0_5[] = {1,0,0,1,1,1,0,0,0,1,0,0,1,1,0,1,0,1,1,0,0,1,0,0,1,0,1};
int param0_6[] = {3,5,6,7,8,9,11,13,18,20,24,25,26,27,36,41,41,45,48,48,49,65,69,70,85,90,99,99};
int param0_7[] = {80,-26,-38,-40,22,-28,0,-36,70,-32,38,58,76,-42,38,92,68,-70,36,-62,24,-84,42,4,0,8,-36,98,-84,82,-70,-12,6,-82,-20,-68,48,-12,42,18,58,-14,94,84};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {36,60,45,76,43,71,10,18,52,52,53,73,48,95,13,50,97,30,73,13,18,34,51};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {45,11,26,28,17,14,20,39,26,22};
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