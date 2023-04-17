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
  if ( n == 1 ) return arr [ 0 ];
  int dec [ n ];
  memset ( dec, 0, sizeof ( dec ) );
  int inc [ n ];
  memset ( inc, 0, sizeof ( inc ) );
  dec [ 0 ] = inc [ 0 ] = arr [ 0 ];
  int flag = 0;
  for ( int i = 1;
  i < n;
  i ++ ) {
    for ( int j = 0;
    j < i;
    j ++ ) {
      if ( arr [ j ] > arr [ i ] ) {
        dec [ i ] = max ( dec [ i ], inc [ j ] + arr [ i ] );
        flag = 1;
      }
      else if ( arr [ j ] < arr [ i ] && flag == 1 ) inc [ i ] = max ( inc [ i ], dec [ j ] + arr [ i ] );
    }
  }
  int result = INT_MIN;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( result < inc [ i ] ) result = inc [ i ];
    if ( result < dec [ i ] ) result = dec [ i ];
  }
  return result;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,5,9,15,15,20,21,26,28,32,34,38,42,42,42,46,47,48,50,54,55,60,60,61,63,63,66,74,79,80,85,91,93};
int param0_1[] = {-98};
int param0_2[] = {0,0,0,0,0,0,0,0,0,1,1,1};
int param0_3[] = {70,5,20,22,44,94,69,89,45,92,56,58,36,91,82,95,9,60,4,34,37,95,38,47,81,68,73,15,88,8,95,28,97,12,24,5,26,82,47,88,28,33,17,28,11,71,74};
int param0_4[] = {-98,-96,-94,-94,-92,-86,-86,-84,-82,-68,-66,-66,-50,-48,-46,-36,-26,-8,-6,8,14,16,18,22,32,48,48,50,62,70,70,74,78,78,84,86,92,94,98};
int param0_5[] = {0,1,1,1,0,0,1,1,1,0,1};
int param0_6[] = {1,2,8,8,12,14,19,24,25,32,36,45,47,53,54,56,56,58,59,60,65,68,86,86,91,98};
int param0_7[] = {-94,88,94,78,-34,84,-32,68,-72,80};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {76,62,62,61,63,15,61,74,50,86,60,35,91,32,93,14,52,18,14,39};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {23,0,6,24,32,5,13,7,30,18};
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