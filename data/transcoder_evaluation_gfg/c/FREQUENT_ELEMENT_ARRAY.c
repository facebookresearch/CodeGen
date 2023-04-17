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
  sort ( arr, arr + n );
  int max_count = 1, res = arr [ 0 ], curr_count = 1;
  for ( int i = 1;
  i < n;
  i ++ ) {
    if ( arr [ i ] == arr [ i - 1 ] ) curr_count ++;
    else {
      if ( curr_count > max_count ) {
        max_count = curr_count;
        res = arr [ i - 1 ];
      }
      curr_count = 1;
    }
  }
  if ( curr_count > max_count ) {
    max_count = curr_count;
    res = arr [ n - 1 ];
  }
  return res;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,1,3,11,11,11,18,20,26,26,27,30,33,39,39,42,42,48,51,51,51,51,60,66,66,68,68,69,71,72,73,76,76,77,77,77,78,90,96};
int param0_1[] = {46,-8,64,-46,-38,92,-14,-22,-32,48,72,96,30,66,94,36,42,-18,14,-74,80,96,-4};
int param0_2[] = {0,0,0,0,0,0,1};
int param0_3[] = {93,32,3,31,67,96,52,80,70,49,45,23,58,87,31,56,21,71,55,97};
int param0_4[] = {-98,-96,-84,-82,-72,-64,-62,-56,-52,-52,-48,-46,-42,-36,-32,-30,-30,-18,-16,-10,-2,0,6,18,22,22,40,42,50,54,64,68,68,72,80,82,84,96};
int param0_5[] = {1,1,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,1,1,0,0,1,0,1,1,0};
int param0_6[] = {9,12,13,28,43,46,64,66,68,89,92};
int param0_7[] = {22,-8,-56,68,-12,-26,-40,-46,-42,-80,4,-42,-72,-22,36,22,-94,48,96,80,-52,46,90,94,36,92,-12,-24,-60,-32,92,18,76,40,-32,6,-22,86,86,-88,38,50,32,78,-82,54,-40,18};
int param0_8[] = {0,0,0,0,0,0,1,1,1};
int param0_9[] = {81,74,32,41,85,65,81,74,40,64,97,4,61,43,54,96,62,2,97,86,80,25,9,31,16,29,4,63,76,41,5,95};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {25,18,6,15,20,29,6,41,4,16};
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