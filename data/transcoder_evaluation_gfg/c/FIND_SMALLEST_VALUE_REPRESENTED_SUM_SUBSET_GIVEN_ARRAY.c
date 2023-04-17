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
  int res = 1;
  for ( int i = 0;
  i < n && arr [ i ] <= res;
  i ++ ) res = res + arr [ i ];
  return res;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {16,23,24,41,48,58,72,75};
int param0_1[] = {-14,-82,12,-14,-38,12,40,12,-74,42,-36,64};
int param0_2[] = {0,0,1,1,1,1};
int param0_3[] = {17,89,44};
int param0_4[] = {-94,-92,-84,-82,-72,-58,-56,-40,-34,-34,-24,-22,-8,-8,12,14,16,16,22,22,34,46,54,58,68,72,74,78,88,96};
int param0_5[] = {0,0,0,0,0,1,0,0,1,0,1,0};
int param0_6[] = {2,12,13,13,13,16,28,32,34,41,41,47,49,49,50,52,58,61,63,65,67,68,68,74,80,80,84,84,89,93,94,98,99,99};
int param0_7[] = {-54};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {42,50,76,45,6,63,46,73,65,70,87,5,41,63,96,75,38,76,27,7,71,9,65,44,76,37,94,52,55,3,38,68,45,15,35,90,36,46,13,92,32,22,49,35,83};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {4,8,5,2,25,8,23,0,33,35};
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