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
  int min_ending_here = INT_MAX;
  int min_so_far = INT_MAX;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( min_ending_here > 0 ) min_ending_here = arr [ i ];
    else min_ending_here += arr [ i ];
    min_so_far = min ( min_so_far, min_ending_here );
  }
  return min_so_far;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,9,13,14,15,18,19,19,25,26,29,29,29,30,31,36,37,37,38,39,39,40,40,42,42,46,50,53,58,60,62,64,65,67,68,69,72,77,78,83,85,89,90,93,95,95,97};
int param0_1[] = {14,-58,8,78,-26,-20,-60,42,-64,-12};
int param0_2[] = {0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_3[] = {44,88,20,47,69,42,26,49,71,91,18,95,9,66,60,37,47,29,98,63,15,9,80,66,1,9,57,56,20,2,1};
int param0_4[] = {-78,-64,-62,-60,-52,4,8,46,72,74};
int param0_5[] = {0,0,1,0,0,0,0,1,1,0,0,1,1,0,1,1};
int param0_6[] = {3,7,16,17,23,23,23,28,29,30,34,38,40,41,43,43,44,46,51,51,51,55,57,58,61,62,66,66,67,69,70,73,75,77,79,80,85,85,87,87,93,96};
int param0_7[] = {80,22,38,26,62,-48,-48,46,-54,4,76,46,48,40,-92,-98,-88,12,-42,-94,76,-16,-82,62,18,-24};
int param0_8[] = {0,0,0,0,0,0,0,0,1,1,1,1,1,1};
int param0_9[] = {85,44,1,97,50,74,62,90,3,78,8,48,96,41,36,91,57,97,85,90,78,43,28,92,85,59,29,38,34,65,20,26,27,23,71,22,47,99,68,93,67,66,69,82,98,15,44,51,65};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {24,6,8,26,8,11,38,22,13,45};
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