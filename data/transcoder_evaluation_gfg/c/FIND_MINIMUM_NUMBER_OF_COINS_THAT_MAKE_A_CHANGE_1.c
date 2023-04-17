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

int f_gold ( int coins [ ], int m, int V ) {
  int table [ V + 1 ];
  table [ 0 ] = 0;
  for ( int i = 1;
  i <= V;
  i ++ ) table [ i ] = INT_MAX;
  for ( int i = 1;
  i <= V;
  i ++ ) {
    for ( int j = 0;
    j < m;
    j ++ ) if ( coins [ j ] <= i ) {
      int sub_res = table [ i - coins [ j ] ];
      if ( sub_res != INT_MAX && sub_res + 1 < table [ i ] ) table [ i ] = sub_res + 1;
    }
  }
  return table [ V ];
}


int f_filled ( int coins [ ], int m, int V ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,7,9,10,10,15,25,27,38,38,51,52,52,56,56,57,61,61,61,65,67,67,68,69,71,71,81,85,87,88,91,97};
int param0_1[] = {42,-36,26,-46,-96,-98,-62,-10,42,22,50,-74,-20};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {87,49,10,12,82,51,34,92,61,4,70,18,13,14,86,40,36,61,66};
int param0_4[] = {-88,-86,-78,-74,-68,-66,-64,-62,-60,-56,-52,-50,-50,-46,-46,-36,-34,-30,-28,-28,-6,-4,0,2,18,24,30,34,36,36,40,46,46,46,48,56,56,60,62,64,68,68,68,82,86,90,92,92};
int param0_5[] = {1,0,0,1,1,0,1,0,0,0,1,1};
int param0_6[] = {8,24,35,70,79};
int param0_7[] = {66,52,10,-78,98,-26,48,66,74,92,30,-60,-92,-30,-82,-96};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {15,56,38,50,36,32,27,90,91,77,74,3,90,47,40,36};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {25,10,20,16,45,11,2,11,22,13};
    int param2[] = {20,11,22,15,27,11,2,13,19,12};
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