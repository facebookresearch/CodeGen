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
  int dp [ k ] [ n ], sum = 0;
  memset ( dp, 0, sizeof ( dp ) );
  for ( int i = 0;
  i < n;
  i ++ ) dp [ 0 ] [ i ] = 1;
  for ( int l = 1;
  l < k;
  l ++ ) {
    for ( int i = l;
    i < n;
    i ++ ) {
      dp [ l ] [ i ] = 0;
      for ( int j = l - 1;
      j < i;
      j ++ ) {
        if ( arr [ j ] < arr [ i ] ) dp [ l ] [ i ] += dp [ l - 1 ] [ j ];
      }
    }
  }
  for ( int i = k - 1;
  i < n;
  i ++ ) sum += dp [ k - 1 ] [ i ];
  return sum;
}


int f_filled ( int arr [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {10,18,66,68,83,86,97};
int param0_1[] = {-30,-16,-70,80,68,96,54,64,-56,96,46,-70,-14,28,-38,-52,-96,-4,-8,16,24,-10,4,54};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {26,72,75,50,57,64,74,99,41,12,11,10,20,1,28,74,92,33,14,18,31,63,52,62,35,97,61,51,39,64,37,12,16,60,72,58,95,41,80,4,50,95,38,60,53};
int param0_4[] = {-94,-88,-74,-74,-72,-68,-62,-60,-60,-54,-54,-36,-30,-18,-6,12,28,32,32,44,50,52,72,74,84,84,88,92};
int param0_5[] = {1};
int param0_6[] = {2,2,10,11,16,23,32,34,34,35,35,41,42,43,44,44,44,45,46,47,49,51,52,52,54,56,59,60,64,65,66,66,67,69,71,77,78,79,82,86,88,89,90,93,95,95,98};
int param0_7[] = {-42,90,18,42,72,88,58,62,-86,14,76,-34,-64,12,-4,90,96,-34,-90,-84,54,-70,96,30,-26,44,-50,-14,50};
int param0_8[] = {0,0,0,0,1,1,1,1,1,1,1,1};
int param0_9[] = {44,19,10,19,84,31,68,2,35,94,18,83,93,84,37,79,50,22,77,3,60,4,70,26,58,60,59,22,75,92};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {6,18,14,35,17,0,24,18,9,20};
    int param2[] = {5,15,17,31,15,0,38,21,8,15};
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