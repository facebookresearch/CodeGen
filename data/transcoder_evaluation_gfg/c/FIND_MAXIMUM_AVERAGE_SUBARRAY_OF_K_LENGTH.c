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

int f_gold ( int arr [ ], int n, int k ) {
  if ( k > n ) return - 1;
  int * csum = new int [ n ];
  csum [ 0 ] = arr [ 0 ];
  for ( int i = 1;
  i < n;
  i ++ ) csum [ i ] = csum [ i - 1 ] + arr [ i ];
  int max_sum = csum [ k - 1 ], max_end = k - 1;
  for ( int i = k;
  i < n;
  i ++ ) {
    int curr_sum = csum [ i ] - csum [ i - k ];
    if ( curr_sum > max_sum ) {
      max_sum = curr_sum;
      max_end = i;
    }
  }
  delete [ ] csum;
  return max_end - k + 1;
}


int f_filled ( int arr [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,4,6,19,21,23,32,34,47,51,56,57,57,65,68,68,69,70,71,73,74,74,77,77,79,82,82,86,87,87,88,89,90,91,92};
int param0_1[] = {24,62,-32,-28,42,-46,-96,-70,-68,60,44,34,-30,96,-26,92,62,42,-46,-38,44,54,-94,52,66,68,-96,-58,84,-2,66,30,42};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {94,6,48,34,31};
int param0_4[] = {-98,-88,-82,-80,-76,-70,-70,-60,-60,-52,-50,-46,-44,-44,-44,-20,-18,-12,-12,-12,-10,-8,-6,-4,4,4,18,28,32,34,42,42,44,46,48,54,60,70,70,72,78,78,78,78,84,86,90,96,98};
int param0_5[] = {0,1,0,0,1,0,1,1,0,0,1,1,0,0,0,0,0};
int param0_6[] = {1,5,13,17,26,26,32,35,38,38,39,45,52,58,60,61,62,63,82,83,85,89,89,91};
int param0_7[] = {-68,-52,4,-90,90,88,38,-18,86,4,14,-32,-14,-44,-88,-50,-12,-26,-68,-20,-30,22,0,14,-40,58,-6,28,-44,8,28,96,-46,-12};
int param0_8[] = {0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_9[] = {17,33,36,34,32,10,37,48,47,32,21,18,75,8,18,52,21,73,25,25,80,32,10,24,1,89,7,42,86,85,73,12,20,20,1,74,77,4,24,74,8};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {29,23,32,4,45,15,13,32,13,20};
    int param2[] = {20,31,31,3,30,8,22,22,11,28};
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