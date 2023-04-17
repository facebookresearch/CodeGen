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

int f_gold ( int a [ ], int n ) {
  int x1 = a [ 0 ];
  int x2 = 1;
  for ( int i = 1;
  i < n;
  i ++ ) x1 = x1 ^ a [ i ];
  for ( int i = 2;
  i <= n + 1;
  i ++ ) x2 = x2 ^ i;
  return ( x1 ^ x2 );
}


int f_filled ( int a [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,5,7,8,10,14,27,32,51,52,57,58,65,68,68,72,73,73,83,92,98};
int param0_1[] = {-60,-48,38,-78,88,86,-4,-94,16,-64,32,88,58,-78,-16,48,38,30,66,-60,20,40,-28,-64,-48,-86,-80,-8,-58,52,80,-32,46,-4,-70,76,-4,78,-64,38,-40};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {69,59,22,33,69,28,11,34,72,88,16,30,69,89,43,4,65,85,27};
int param0_4[] = {-98,-98,-92,-88,-88,-82,-74,-70,-68,-60,-60,-48,-38,-34,-34,-24,14,38,50,58,62,64,64,68,76,78,78,86,88,90,92,98,98};
int param0_5[] = {0,1,0,1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,0,0,0,1,1,0,0,0,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,0};
int param0_6[] = {1,9,12,12,24,25,33,33,36,39,46,48,48,52,52,53,57,69,71,72,75,76,78,80,82,86,89,91,94,95,96,97,98,99};
int param0_7[] = {62,-66,60,-92,46,6,-52,48,72,-64,34,20,50,70,-34,20,-70,14,-44,66,-70};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {33,10,6,71,18,22,15,57,56,63,35,93,31,43,98,99,62,39,44,86,78,95,6,76,71};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {12,28,38,13,23,41,30,17,30,12};
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