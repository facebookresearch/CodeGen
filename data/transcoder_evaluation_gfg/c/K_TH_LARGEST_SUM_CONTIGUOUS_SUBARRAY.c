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
  int sum [ n + 1 ];
  sum [ 0 ] = 0;
  sum [ 1 ] = arr [ 0 ];
  for ( int i = 2;
  i <= n;
  i ++ ) sum [ i ] = sum [ i - 1 ] + arr [ i - 1 ];
  priority_queue < int, vector < int >, greater < int > > Q;
  for ( int i = 1;
  i <= n;
  i ++ ) {
    for ( int j = i;
    j <= n;
    j ++ ) {
      int x = sum [ j ] - sum [ i - 1 ];
      if ( len(Q) < k ) Q . push ( x );
      else {
        if ( Q . top ( ) < x ) {
          Q . pop ( );
          Q . push ( x );
        }
      }
    }
  }
  return Q . top ( );
}


int f_filled ( int arr [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,3,5,7,8,29,29,44,47,52,60,65,73,83,87,92,92,95};
int param0_1[] = {44,-98,-10,14,-6,-46,6,-74,-4,36,10,-2,30,28,96,-84,-36,-76,64,-74,-20,94,-4,14,78,52,-56,98,-68,-76,-10,20,88,-98,96,80,96,-32,-40,-30,82};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {58,21,97,78,78,57,29,33,57,81,66,32,11,82,28,72,46,67,42,15,60,45,16,37};
int param0_4[] = {-92,-90,-88,-84,-68,-66,-62,-58,-52,-44,-22,-16,-4,-4,2,12,14,14,24,26,44,56,80,90,92,94,98};
int param0_5[] = {1,1,1,1,1,1,1,1,0,0,0};
int param0_6[] = {3,4,8,12,13,14,17,19,23,24,28,29,30,35,35,38,44,47,47,53,55,56,56,58,66,67,70,71,72,73,74,75,77,78,82,84,87,87,87,88,88,93,94,96};
int param0_7[] = {20,-58,94,-70,18,16,-46,38,-44,-92,-20,-70,-30,50};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {90,77,82,38,96,62,66,4,93,30,75,22,26,61,40,11,38,55,88,24,66,47,40,71,21,5,18,31,26,56,19,47,71,34};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {10,34,16,14,15,5,26,11,19,28};
    int param2[] = {12,37,15,20,25,5,25,7,23,32};
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