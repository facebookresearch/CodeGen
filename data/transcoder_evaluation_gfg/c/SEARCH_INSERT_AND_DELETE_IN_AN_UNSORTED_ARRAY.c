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

int f_gold ( int arr [ ], int n, int key ) {
  int i;
  for ( i = 0;
  i < n;
  i ++ ) if ( arr [ i ] == key ) return i;
  return - 1;
}


int f_filled ( int arr [ ], int n, int key ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,8,11,23,55,57,73,74,77,79,93};
int param0_1[] = {-88,12,-62,-66,-24,18,12,22,94,30,-50,-42,-94,18,76,-6,-48,-68,48,36,-78,52,-82,76,2,-44,-10,88};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1};
int param0_3[] = {33,9,93,70,81,70,56,66,72,81,74,32,71,72,3,81,70,22,82,2,75,18,90,29,48};
int param0_4[] = {-98,-70,-62,-60,-60,-54,-48,-48,-46,-44,-34,-26,-18,-6,4,18,28,32,34,40,50,54,56,62,64,64,98};
int param0_5[] = {1,1,1,1,0,0,0,0,1,0,0,1,0,0,1,1,0,1,1,0,0,1};
int param0_6[] = {4,6,7,10,10,12,13,18,23,29,29,34,46,54,60,61,63,67,69,70,72,76,79,79,81,82,88,90,99};
int param0_7[] = {94,34,-60,-74,86,80,68,-48,78,-62,-98,-44,-44,92,-94,-86,-36,12,84,-90,52,42,-42,-66,88,76,66};
int param0_8[] = {0,0,0,1};
int param0_9[] = {76,59,38,83,38,93,27,11,17,80,26,28,35,53,88,10,9,75};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {8,27,11,24,18,17,15,21,2,12};
    int param2[] = {11,12,0,72,23,16,28,16,3,13};
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