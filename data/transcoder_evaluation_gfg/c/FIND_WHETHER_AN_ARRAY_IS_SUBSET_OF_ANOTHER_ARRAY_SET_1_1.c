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

bool f_gold ( int arr1 [ ], int arr2 [ ], int m, int n ) {
  int i = 0, j = 0;
  if ( m < n ) return 0;
  sort ( arr1, arr1 + m );
  sort ( arr2, arr2 + n );
  while ( i < n && j < m ) {
    if ( arr1 [ j ] < arr2 [ i ] ) j ++;
    else if ( arr1 [ j ] == arr2 [ i ] ) {
      j ++;
      i ++;
    }
    else if ( arr1 [ j ] > arr2 [ i ] ) return 0;
  }
  return ( i < n ) ? false : true;
}


bool f_filled ( int arr1 [ ], int arr2 [ ], int m, int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {7,10,10,10,13,17,23,24,25,28,30,33,37,49,49,50,57,60,60,63,63,64,65,65,72,81,84,85,85,94,96};
int param0_1[] = {12,30,-94,-92,-62,-18,-56,44,-50,-92,6,2,56,-90,0,0,18,86,-58,58,-54,62,-94,94,0,8,82,-68,-88,-18,8,-80,-42,18,62,-8,56,-76,-42,56,44,-2,-20,62,-14,74,-86,-76};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {94,26,32,20,46,55,9,51,57,80,45,38,68,12,90,10,80,65,12,52,51,86,64,57,93,19,30,92,85,82,24,26,36,56};
int param0_4[] = {-98,-90,-86,-86,-84,-84,-82,-80,-78,-72,-70,-68,-66,-64,-52,-52,-50,-38,-28,-26,-24,-14,-8,16,26,26,28,34,36,40,42,44,44,46,50,60,68,78,80,86,90,92,98};
int param0_5[] = {1,0,1,0,1,0,0,0,1,0,0,0,0,1,1,0,1,1};
int param0_6[] = {6,8,11,13,14,26,26,41,48,70,82,83,84,88,96};
int param0_7[] = {-88,80,62,76,48,92,18,-94,-62,98,-46,-50,70,32,68,-54,26,16,94,0,-84,2,-16,88,26,-38,18,64,90,80,76,2,14,-90,50,4,76,30};
int param0_8[] = {0,0,0,0,0,1,1,1,1,1,1,1};
int param0_9[] = {54,44,97,92,13,54,27,8,43,70,77,84,55,64,5,59,27,19,65,68,66,26,33,38,7};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {44};
int param1_1[] = {0,0,0};
int param1_2[] = {80,58,32,2};
int param1_3[] = {-99,-90,-90,-86};
int param1_4[] = {0,0,1,1};
int param1_5[] = {1,9,12,16};
int param1_6[] = {-76,-54,4,78};
int param1_7[] = {0,1,0,1};
int param1_8[] = {93,5,9,13};
int *param1[9] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8};
    int param2[] = {29,46,34,17,23,10,10,27,10,19};
    int param3[] = {4,3,3,4,4,4,4,4,4,4};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i]) == f_gold(param0[i],param1[i],param2[i],param3[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}