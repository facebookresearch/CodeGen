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

int f_gold ( int arr [ ], int n, int X ) {
  if ( X < arr [ 0 ] ) return 0;
  else if ( X > arr [ n - 1 ] ) return n;
  int lowerPnt = 0;
  int i = 1;
  while ( i < n && arr [ i ] < X ) {
    lowerPnt = i;
    i = i * 2;
  }
  while ( lowerPnt < n && arr [ lowerPnt ] < X ) lowerPnt ++;
  return lowerPnt;
}


int f_filled ( int arr [ ], int n, int X ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,2,5,5,16,16,20,26,32,35,39,39,41,44,48,48,51,59,59,62,66,66,70,74,75,78,80,86,86,96};
int param0_1[] = {-76,80,-6,-2,50,72,84,-56,70,8,48,6,-24,-50,-72};
int param0_2[] = {0,0,0,0,0,1,1,1,1};
int param0_3[] = {74,65,84,71};
int param0_4[] = {-96,-92,-90,-86,-84,-76,-76,-62,-58,-54,-50,-50,-44,-42,-38,-34,-14,-8,6,12,24,38,40,50,62,84,86,92};
int param0_5[] = {1,1,0,0,0,1,1,1,0,0,1,1,0,1,0,1,0,0,0,1,1,1,1};
int param0_6[] = {6,10,14,14,16,19,23,23,25,26,29,34,42,42,43,45,47,49,50,51,51,56,59,65,69,72,75,78,79,80,82,82,82,84,85,91,98};
int param0_7[] = {-90,-2,22,-2,58,-2,96,38,36,-66,-98,22,-80,-32,22,0,-34,-16,82,76,12,84,66,8,32,18,-98,-10};
int param0_8[] = {0,0,0,1,1,1,1};
int param0_9[] = {85,59,22,52,93,14,42,71,69,15,52,78,35,61,92,90,70,48,47,72,74,46,22,74,83,32,14,24,18,27,18,68,29,31};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {17,14,8,2,19,12,31,22,3,19};
    int param2[] = {29,9,4,3,19,17,24,16,5,33};
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