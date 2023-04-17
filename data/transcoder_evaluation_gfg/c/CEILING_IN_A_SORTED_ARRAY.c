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

int f_gold ( int arr [ ], int low, int high, int x ) {
  int i;
  if ( x <= arr [ low ] ) return low;
  for ( i = low;
  i < high;
  i ++ ) {
    if ( arr [ i ] == x ) return i;
    if ( arr [ i ] < x && arr [ i + 1 ] >= x ) return i + 1;
  }
  return - 1;
}


int f_filled ( int arr [ ], int low, int high, int x ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,3,4,6,8,9,9,10,11,16,19,20,21,21,21,24,24,25,28,30,30,30,32,34,35,39,41,42,49,52,57,59,61,62,66,68,71,73,76,79,83,84,85,86,87,87};
int param0_1[] = {92,50,-84,60,32,-54,84,-82,-42,-72,-64,-28,-48,66,92,-42,42,-66,52,-30,48,42,36,-4,64,62,-16,0,20,26,78,78,12,-6,-30,-14,76,72,70,-34,98,32};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1};
int param0_3[] = {26,68,73,76,14,19,56,80,17,7,15,64,99,98,21,21,72,12,14,10,44,82,25,42,46,86,79,43,91};
int param0_4[] = {-90,-86,-84,-50,-30,-24,-12,-2,8,22,30,44,58,58,60,60,62,90};
int param0_5[] = {0,0,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,0,1,1};
int param0_6[] = {2,2,29,31,34,39,48,50,56,61,66,66,69,73,88};
int param0_7[] = {-98,48,-58,8,70,62,92,84,-58,-46,-26,-92,18,-88,40,-12,60,14,54,-64,88,52,-44,88,-46,-8,36,-22,28,-20,-50,58,-82,-44,-44,54,-86,40,10,0,-24,-84,-10,62,58,0,-88};
int param0_8[] = {0,0,0,0,1,1};
int param0_9[] = {56,30,33,5,67,35,22,54,36,55,94,89,40,65,29,76,17,14,14,49,40,44,35,69,63,2,81,78,19,67,12,14,68,30,82,85,12,2,94,33,85,75,97,31,69,31,85,26};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {23,36,11,23,9,12,9,40,5,46};
    int param2[] = {37,35,9,27,16,15,12,29,5,47};
    int param3[] = {44,34,13,26,10,18,10,24,5,47};
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