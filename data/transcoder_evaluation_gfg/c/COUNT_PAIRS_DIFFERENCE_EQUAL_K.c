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
  int count = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    for ( int j = i + 1;
    j < n;
    j ++ ) if ( arr [ i ] - arr [ j ] == k || arr [ j ] - arr [ i ] == k ) count ++;
  }
  return count;
}


int f_filled ( int arr [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {9,14,17,19,22,23,23,27,30,31,34,37,37,39,39,42,57,61,68,73,77,79,91,96,97};
int param0_1[] = {-78,-42,28,-88,18,-52};
int param0_2[] = {0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1};
int param0_3[] = {8,46,57,28,80,2,75,57,83,45,32,49,77,30,94,33,23,29,35,81,85};
int param0_4[] = {-90,-72,-72,-62,-62,-54,-54,-52,-48,-38,-22,-22,-22,-12,-12,-8,-8,-8,-6,-6,-2,6,12,26,26,28,28,38,40,48,52,52,58,60,68,70,72,76,76,76,92};
int param0_5[] = {0,0,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,1,1,0,0,1,0,1,1,1,1,1,0,0,0,0,0,0,1,0,1,0,1,0,0,1,0,0,1,0,1};
int param0_6[] = {3,13,19,23,27,32,49,52,54,57,58,58,63,67,68,68,69,70,75,80,86,90,91,95};
int param0_7[] = {-56,40,-66,42,8,-40,-8,-42};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {99,12,90,10,86,86,81,19,1,1,98,82,34,39,34,1,54,47,39,82,21,50,82,41,98,47,88,46,72,28,28,29,60,87,92,53,93,29,74,75,11,32,48,47,85,16,20};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {19,3,16,15,22,45,19,7,16,24};
    int param2[] = {19,4,14,11,25,39,21,6,28,45};
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