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

int f_gold ( int price [ ], int n ) {
  int * profit = new int [ n ];
  for ( int i = 0;
  i < n;
  i ++ ) profit [ i ] = 0;
  int max_price = price [ n - 1 ];
  for ( int i = n - 2;
  i >= 0;
  i -- ) {
    if ( price [ i ] > max_price ) max_price = price [ i ];
    profit [ i ] = max ( profit [ i + 1 ], max_price - price [ i ] );
  }
  int min_price = price [ 0 ];
  for ( int i = 1;
  i < n;
  i ++ ) {
    if ( price [ i ] < min_price ) min_price = price [ i ];
    profit [ i ] = max ( profit [ i - 1 ], profit [ i ] + ( price [ i ] - min_price ) );
  }
  int result = profit [ n - 1 ];
  delete [ ] profit;
  return result;
}


int f_filled ( int price [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {9,10,10,12,17,18,23,32,41,44,47,50,59,69,69,75,82,84,87,89,97,99};
int param0_1[] = {6,6,60,40,32,-70,-92,88,10,-8,-54,4,16,8,-44,80,-70,36,36,-74,-94,18,-64,-66,-46,0,-54,-84,16,-88,-34,-24,92,84,62};
int param0_2[] = {0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {2,67,50,8,20,42,37,69,86,74,85,96,78,89,91};
int param0_4[] = {-68,-52,-14,-2,18,22,30,34,64,64,70};
int param0_5[] = {1,1,0,0,0,1,0,0,1,1,1,1,1,0,0,1,1,0,1,1,0,1,0,0,1,1,0,1};
int param0_6[] = {4,17,19,28,29,30,30,30,35,36,36,38,40,40,42,43,45,51,55,57,58,59,64,65,66,82,84,85,87,91,92,94,98,98};
int param0_7[] = {52,88,-40,60,30,8,-96,66,-96,-28,-56,-14,76,-92,56,58,64,-60,-90,26,64,-2,54,-24,54,-46,-44};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {82,14,51,12,5,15,50,88,91,82,16,98,23,58,86,91,30,81,7,73,67,47,10,50,43,31,19,2,22};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {20,34,13,8,9,21,25,14,22,18};
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