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
  int sum = 0;
  int leftsum = 0;
  for ( int i = 0;
  i < n;
  ++ i ) sum += arr [ i ];
  for ( int i = 0;
  i < n;
  ++ i ) {
    sum -= arr [ i ];
    if ( leftsum == sum ) return i;
    leftsum += arr [ i ];
  }
  return - 1;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {24,31,44,52,78,95};
int param0_1[] = {-78,-38,22,58,68,-60,-30,6,58,20,-64,-40,-14,80,-2,-88,-68,-16,-4,78,-38,-74,78,-72,46,-12,82,-76,-98,-28,-32,88,72,72,64,-10,98,-24,-96};
int param0_2[] = {0,0,0,0,0,0,0,0,1,1,1,1};
int param0_3[] = {98,69,41,48,40,90,76,61,17,81,74,92,54,16,11,15,8,16,84,86,34,34,75,92,67,54,93,19,31,62,89,26,96,91,32,78,42,84,66,79,29,48,49,5};
int param0_4[] = {-28,42};
int param0_5[] = {1,1,1,1,0,0,0,0,0,1,0,1,1,0,1,1,0,1,0,1,0,0,0,1,0,1};
int param0_6[] = {18,21,23,24,36,37,39,49,55,68,80,81,88,90};
int param0_7[] = {94,22,42,-42,78,50,96,98,46,74,98,84,-2,-76,48,18,28,-62,78,6,-76,-12,46,62,14,76,44,-26,-92,12,62,-72,-42};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_9[] = {1,23,18,91,65,2,73,12,91,47,14,48,1,69,95,81,59,36,79,35,9,52,55,73,54,25,8,41,64,96};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {4,19,11,27,1,25,11,32,14,19};
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