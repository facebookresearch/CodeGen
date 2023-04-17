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

bool f_gold ( int arr [ ], int n, int m ) {
  if ( n > m ) return true;
  bool DP [ m ];
  memset ( DP, false, m );
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( DP [ 0 ] ) return true;
    bool temp [ m ];
    memset ( temp, false, m );
    for ( int j = 0;
    j < m;
    j ++ ) {
      if ( DP [ j ] == true ) {
        if ( DP [ ( j + arr [ i ] ) % m ] == false ) temp [ ( j + arr [ i ] ) % m ] = true;
      }
    }
    for ( int j = 0;
    j < m;
    j ++ ) if ( temp [ j ] ) DP [ j ] = true;
    DP [ arr [ i ] % m ] = true;
  }
  return DP [ 0 ];
}


bool f_filled ( int arr [ ], int n, int m ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {6};
int param0_1[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_2[] = {50,20,79,42,85,24,20,76,36,88,40,5,24,85,7,19,43,51,94,13,53,93,92,43,97,38,80,48,52,47,77,56,41,80,32,34,77,14,70,3};
int param0_3[] = {-96,-94,-72,-58,-48,-36,-28,-26,-10,-10,-8,-8,-6,2,14,30,30,54,58,60,64,68,78,84,96,98};
int param0_4[] = {1,0,1,1,0,0,1,1,1,0,0};
int param0_5[] = {2,7,8,15,18,23,24,25,27,35,40,42,43,46,48,50,53,64,66,69,70,71,72,77,78,80,81,81,81,82,82,82,84,87,97,98};
int param0_6[] = {46,54,24,-10};
int param0_7[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_8[] = {39,21,38,6,38,44,96,1,16,1,28,4,55,8};
int *param0[9] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8};
    int param1[] = {36,2,32,29,16,7,23,3,21,12};
    int param2[] = {3540,5,101,27,18,8,33,37,34,228};
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