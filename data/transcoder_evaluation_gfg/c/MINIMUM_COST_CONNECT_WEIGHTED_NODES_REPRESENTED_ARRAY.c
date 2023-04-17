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
  int mn = INT_MAX;
  int sum = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    mn = min ( a [ i ], mn );
    sum += a [ i ];
  }
  return mn * ( sum - mn );
}


int f_filled ( int a [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {3,8,14,15,17,17,19,21,22,23,29,32,36,37,43,45,46,47,47,53,57,57,70,71,72,76,81,82,90,95,96,98,99};
int param0_1[] = {94,-18,50,94,-74,-50,-44,-92,-58,14,-66,-78};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {15,18,64,28};
int param0_4[] = {-96,-88,-88,-84,-82,-78,-78,-60,-58,-56,-54,-52,-48,-44,-28,-26,-14,-12,6,10,10,14,14,50,52,54,60,62,62,64,66,70,72,72,78,80,84};
int param0_5[] = {0,1,1,0,1,1,1,1};
int param0_6[] = {3,10,14,14,15,16,18,20,21,30,31,33,35,39,46,48,59,59,61,77,78,79,81,83,85,92,97,97,99};
int param0_7[] = {4,-32,68,-48,54,24,78,98,-70,44,-82,-92,-16,-92,-70,52,-58,-62,-58,32,14,-4,80,-78,-26,-24,-8};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {82,74,53,91,81,88,42,62,38,43,29,60,43,44,19,28,20,1,5,94,18,77,52,38,55,1,10,29,34,91,64,80,81,39,4,47,30,62,58,66,73,52,62,9,36,49};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {32,10,24,2,31,6,23,18,35,38};
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