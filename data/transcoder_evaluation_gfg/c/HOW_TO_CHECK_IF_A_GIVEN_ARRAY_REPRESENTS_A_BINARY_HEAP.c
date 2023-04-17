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

bool f_gold ( int arr [ ], int i, int n ) {
  if ( i > ( n - 2 ) / 2 ) return true;
  if ( arr [ i ] >= arr [ 2 * i + 1 ] && arr [ i ] >= arr [ 2 * i + 2 ] && f_gold ( arr, 2 * i + 1, n ) && f_gold ( arr, 2 * i + 2, n ) ) return true;
  return false;
}


bool f_filled ( int arr [ ], int i, int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,2,3,5,24,24,25,25,36,37,37,39,42,44,46,50,51,54,56,60,62,70,71,73,75,80,80,85,86,89,91,95,99};
int param0_1[] = {-44,-58,88,-42,42,-14,-44,42,64,94,-46,-70,34,-10,-46,-52,-6,-78,64,56,74,98,-34,-4,-92,6,-52,-20,78,-72,-40};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {10,2,1,34,21,37,49,31,70,97,87,50,76,55};
int param0_4[] = {-94,-84,-82,-66,-64,-62,-56,-38,-24,-24,-4,2,4,4,8,14,16,20,30,34,34,48,58,58,70,76,78,86,88,96,98};
int param0_5[] = {1,0,1,0,1,1,1,1,1,0,0,0,1,0,1,1,0,0};
int param0_6[] = {5,20,30,5,10,21,5};
int param0_7[] = {50,20,30,5,10,21,5};
int param0_8[] = {50,20,30,5,10,21,5};
int param0_9[] = {50,20,30,5,10,21,5};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {0,0,0,0,29,12,0,0,2,7};
    int param2[] = {18,27,20,8,26,11,7,7,7,7};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i]) == f_gold(param0[i],param1[i],param2[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}