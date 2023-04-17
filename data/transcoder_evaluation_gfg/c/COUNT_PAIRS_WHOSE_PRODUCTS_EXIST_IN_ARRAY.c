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
  int result = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    for ( int j = i + 1;
    j < n;
    j ++ ) {
      int product = arr [ i ] * arr [ j ];
      for ( int k = 0;
      k < n;
      k ++ ) {
        if ( arr [ k ] == product ) {
          result ++;
          break;
        }
      }
    }
  }
  return result;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {3,7,26,40,46,89,99};
int param0_1[] = {98,42,-24,-60,74,86,6,8,72,-58,38,-20,6,-6,8,48,-34,30,60,66,38,-54,8,-94,-8,0,-64,-94,-94,-72,-84,-36,88,-62,-88,46,-4,88};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {37,97,57,82,29,68,94,38,81,48,13,84,57,5,27,87,11,35,82,53,67,31,15,99,6,93,91,92,3,23,90,27,6,33,78,3,19,19,27};
int param0_4[] = {-80,-74,-72,-72,-66,-66,-62,-50,-44,-44,-28,-24,-24,-22,-16,-10,-6,-4,-2,2,2,4,12,16,16,28,30,32,32,38,38,72,84,86,88,90,96};
int param0_5[] = {0,1,0,0,1,0,1,1,0,1,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,1,1,1};
int param0_6[] = {25,67};
int param0_7[] = {82,74,-82,22,-28,-78,-22,-86,-74,42,-6,54,-88,-92,-14,-50,68,46,-50,46,-18,66,-76,-30,36,12,66};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {50,23,56,9};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {5,24,44,36,34,18,1,14,32,3};
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