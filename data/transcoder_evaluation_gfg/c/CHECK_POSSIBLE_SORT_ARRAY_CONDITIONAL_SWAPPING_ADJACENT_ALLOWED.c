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

bool f_gold ( int arr [ ], int n ) {
  for ( int i = 0;
  i < n - 1;
  i ++ ) {
    if ( arr [ i ] > arr [ i + 1 ] ) {
      if ( arr [ i ] - arr [ i + 1 ] == 1 ) swap ( arr [ i ], arr [ i + 1 ] );
      else return false;
    }
  }
  return true;
}


bool f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,4,12,16,37,44,47,51,55,57,57,62,62,62,64,69,69,70,72,81,81,88,89,97};
int param0_1[] = {-86,0,14,-16,-12,-72,62,-34,-72,30,84,-60,84,-64,50,74,18,-82,-64,-64,-74,-56,86,84,-32,-10,20,4,8,96,82,26,42};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {48,66,83,12,77,98,18,33,21,16,28,24,46,43};
int param0_4[] = {-92,-58,-36,-28,-6,2,4,26,48,58,60,62,62,98};
int param0_5[] = {1,0,0,0,0,1};
int param0_6[] = {22,38,41,41,42,51,54,58,68,76,80,85};
int param0_7[] = {84,-38,52,-72,-24,82,54,74,0};
int param0_8[] = {0,1,1};
int param0_9[] = {63,31,14,19,77,64,62,23,22,19,39,9,79,1,87,29,58,3,3,39,1,39,35,64,64};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {15,18,31,13,10,4,9,8,2,13};
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