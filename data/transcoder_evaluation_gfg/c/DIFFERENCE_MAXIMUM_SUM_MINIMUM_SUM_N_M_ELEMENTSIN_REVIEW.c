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

int f_gold ( int arr [ ], int n, int m ) {
  int max = 0, min = 0;
  sort ( arr, arr + n );
  for ( int i = 0, j = n - 1;
  i < m;
  i ++, j -- ) {
    min += arr [ i ];
    max += arr [ j ];
  }
  return ( max - min );
}


int f_filled ( int arr [ ], int n, int m ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,3,6,16,21,22,23,27,27,28,29,29,31,31,37,37,38,40,41,43,51,52,53,55,55,56,57,63,67,67,67,72,75,79,82,84,91,92,93,96,96,97};
int param0_1[] = {58,-62,24,-10,-30,-92,-50,-32,54,-18,94,-14,-40,-16,48};
int param0_2[] = {0,0};
int param0_3[] = {7,51,6,71,10,29,49,63,77,13,13,56,65,34,76,16,84,2,89,83,65,1,5,99,11,59,71,54,17,9,11,48,2,65,62,77,29,80,97,83,44,91,4,44,21,12,24};
int param0_4[] = {-90,-58,6,16,20,34,36,38,48,66,82,84,86,90,90};
int param0_5[] = {0,0,1,1,0};
int param0_6[] = {7,12,15,15,21,37,40,45,50,52,53,68,68,72,75,78,86,86,88};
int param0_7[] = {22,-20,94,-88,72,44};
int param0_8[] = {0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {32,63,87,26,77,4,87,60,21,25,30,65,38,96,11,75};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {21,8,1,31,14,3,16,4,25,12};
    int param2[] = {25,12,1,34,8,2,18,3,17,15};
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