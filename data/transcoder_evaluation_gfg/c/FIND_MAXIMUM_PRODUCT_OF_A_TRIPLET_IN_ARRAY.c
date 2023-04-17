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
  if ( n < 3 ) return - 1;
  int max_product = INT_MIN;
  for ( int i = 0;
  i < n - 2;
  i ++ ) for ( int j = i + 1;
  j < n - 1;
  j ++ ) for ( int k = j + 1;
  k < n;
  k ++ ) max_product = max ( max_product, arr [ i ] * arr [ j ] * arr [ k ] );
  return max_product;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {41,66,77};
int param0_1[] = {92,-34,-36,-50,20,-94,2,-86,22,-50,74,84,52,-84,98,-50,88,26,-36,-36,6,-50,-48,-84,38,-96,-62,34,52,92,40,-84,18,-90,54,-38,-74,-98,-8,-92,-60,86,-36,94,56};
int param0_2[] = {0,0,1};
int param0_3[] = {2,77,99,95,78,15,69,39,34,43,66,45,97,27,67,62,64,2,28,94,41,87,97,52,14,61,78,50};
int param0_4[] = {-62,-28,40,76};
int param0_5[] = {0,1,1,0,1,1,1,1,1};
int param0_6[] = {2,6,10,11,12,12,17,18,18,19,20,22,24,25,30,35,36,37,40,41,42,47,60,60,64,69,69,70,73,79,80,83,97,97,97};
int param0_7[] = {-72,98,68,18,92,-84,50,32,-90,-40,50,60,-50,-50,50,24,30,94,-98,-6,46,-46,-24,-62,-20,62,-76};
int param0_8[] = {0,0,0,0,0,1,1,1};
int param0_9[] = {85,36,7,69,9,45,18,47,1,78,72,53,37,20,95,71,58,41};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {2,40,1,26,3,5,25,14,7,14};
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