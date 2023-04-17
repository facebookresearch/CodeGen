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
  int dist_count = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    int j;
    for ( j = 0;
    j < n;
    j ++ ) if ( i != j && arr [ j ] == arr [ i ] ) break;
    if ( j == n ) dist_count ++;
    if ( dist_count == k ) return arr [ i ];
  }
  return - 1;
}


int f_filled ( int arr [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,3,8,18,20,33,53,56,60,71,76,80,81,87,88,89,92,95};
int param0_1[] = {-78,6,32,52,-12,-32,22,-40,-82,24,30,10,-40};
int param0_2[] = {0,0,0,0,0,1,1,1,1,1,1};
int param0_3[] = {3,28,55,21,42,60,96,83,98,75,29,73,51,21,27,65,19,47,12,81,19,94,50,43,21,32,52,44,52,91,49,59,52,10,75,86,46,43,3,49,70,60,77,99,27,63};
int param0_4[] = {-96,-90,-76,-44,-16,-8,0,0,2,2,8,14,16,18,18,20,20,28,34,44,68,74,84,90};
int param0_5[] = {0,1,1,0,0,0,0,0,1,0,0,1,0};
int param0_6[] = {3,4,5,8,9,15,26,26,26,35,39,40,42,43,45,45,48,52,54,56,57,67,74,77,79,80,81,86,87,92,95,97};
int param0_7[] = {-76,-24,-12,66,-40,26,72,46,-56,58,-68,2,-82};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {29,83,32,75,5,22,68,64,36,18,7,63,16,42,77,61,1,26,12,41,67,85,85,35,94,18,14,65,8,55,44,34,48,23,8,27,86,2,51,91};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {16,8,7,40,23,10,26,6,27,28};
    int param2[] = {16,6,5,39,12,8,24,10,17,24};
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