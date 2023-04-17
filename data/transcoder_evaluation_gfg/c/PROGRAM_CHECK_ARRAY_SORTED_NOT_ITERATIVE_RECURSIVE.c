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
  if ( n == 1 || n == 0 ) return 1;
  if ( arr [ n - 1 ] < arr [ n - 2 ] ) return 0;
  return f_gold ( arr, n - 1 );
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,4,19,21,28,32,35,44,51,55,62,80,80,83,90,93,93};
int param0_1[] = {84,-28,-42,38,-94,-70,34,54,38,-58,-54,-6,72,-32,-18,80,-6,-38,-30,-86,-10,14,92,-56,40,-58,-2,-6,-46,-80,72,-12,2,-64,36,98,-24};
int param0_2[] = {0,1,1,1};
int param0_3[] = {74,75,9,13,57,82,57,37,47,11,28,6,33,14,47,29,15,56,69,86,31,19,18,58,70,73,30,95,35,17,16,97,68,95,33,36,11,60,4,63,5,64,85,77,4};
int param0_4[] = {-96,-92,-84,-78,-74,-68,-66,-64,-62,-50,-48,-48,-46,-38,-28,-28,-26,-24,-24,-20,-14,-12,-4,16,18,28,32,48,50,62,70,72,78,90,92};
int param0_5[] = {0,1,0,1,0,0,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,0,0,1,1,1,0,1,1,1,1,1,1,0,1,0,1,1,1,0,0,1,0,1,1,1,0,0};
int param0_6[] = {6,8,11,21,29,31,41,50,56,56,69,69,74,79,86,88,93,95,99};
int param0_7[] = {10,-12,-36,72,-42,-94,38,-78,-4,6,12,6,-48};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {97,58,88,20,63,1,23,33,57,81,54,66,95,31,54,16,37,7,1,94,18,42,39,26,75,65,57,69,86,77,17,7,71,12,38,87,48,55,54,72,15,30,55};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {8,21,2,31,31,38,10,6,35,29};
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