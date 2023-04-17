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
  int neg = 0, pos = 0;
  int sum = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    sum += arr [ i ];
    if ( arr [ i ] < 0 ) neg ++;
    else pos ++;
  }
  return ( sum / abs ( neg - pos ) );
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {49,98};
int param0_1[] = {82,66,-68,24,-10};
int param0_2[] = {0,0,0,0,0,0,0,1,1,1,1,1,1,1};
int param0_3[] = {56,3,18,5,20,56,47,29,60,98,60,40,42,2,54,56,91,8,93,14,31,27,61,49,23,12,71};
int param0_4[] = {-94,-94,-92,-86,-50,-48,-6,8,28,40,44,58,62,72,94};
int param0_5[] = {0,0,1,0,1,0,1,1,1,0,1,0,0,0,1,0,0,1,0,0,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,0,0,1,1,1,0,1,0,1};
int param0_6[] = {16,56,56};
int param0_7[] = {74,-90,-92,30,-18,66,-66,22};
int param0_8[] = {0,0,0,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {21,64,82,78,30,34,35};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {1,2,8,25,12,36,1,5,7,5};
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