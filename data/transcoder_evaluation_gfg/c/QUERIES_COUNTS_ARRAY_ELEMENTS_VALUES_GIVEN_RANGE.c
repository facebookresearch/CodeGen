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

int f_gold ( int arr [ ], int n, int x, int y ) {
  int count = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( arr [ i ] >= x && arr [ i ] <= y ) count ++;
  }
  return count;
}


int f_filled ( int arr [ ], int n, int x, int y ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {9,16,19,24,36,38,42,49,51,53,53,57,57,58,71,78,78,92,92,93};
int param0_1[] = {28,-74,-18,10,26,28,-96,-80,82,94,22,50,72,-90,76,50,20,-44,-80};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {25,8,66,90,50,65,76,90,27};
int param0_4[] = {-98,-96,-90,-82,-80,-78,-70,-66,-60,-60,-50,-48,-34,-26,-24,-16,-14,-8,-6,4,22,24,26,30,30,48,52,56,60,62,74,76,78,86};
int param0_5[] = {1,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,0};
int param0_6[] = {4,6,17,19,24,29,30,31,32,37,37,40,43,44,44,45,57,64,69,70,73,78,86,89,91,92,94};
int param0_7[] = {32,-88,70,-6,28,-48};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {37,84,97,74,12,26,47,10,14,33};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {13,18,30,4,32,15,17,4,13,5};
    int param2[] = {12,13,21,8,24,16,21,3,12,9};
    int param3[] = {13,13,31,5,24,12,15,4,11,8};
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