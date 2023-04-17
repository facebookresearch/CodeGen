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
  int i;
  for ( i = 0;
  i < n;
  i ++ ) {
    if ( arr [ i ] == i ) return i;
  }
  return - 1;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {8,16,21,26,27,29,34,35,35,37,38,40,48,52,58,59,60,61,63,63,65,66,69,75,79,83,86,88,91,91,96};
int param0_1[] = {22,-70,34,-44,84,54,14,-88};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {59,67,70,34,18,22,52,95,11,66,60,24,7,71,52,88,32,52,85,81,32,44,25,51,47,97,81,33,88,38,36,54,80,25,70,27,75,29,94};
int param0_4[] = {-96,-96,-94,-88,-88,-82,-72,-72,-70,-70,-66,-64,-64,-62,-58,-54,-46,-44,-30,-26,-22,-8,-6,-2,0,26,30,30,34,42,42,48,64,76,90,96};
int param0_5[] = {0,1,0,0,1,1,1,0,0,1,1,0,1,0,0,0,0,0,1,0,1,1,0,0,1,0,1,1};
int param0_6[] = {2,2,4,7,10,15,16,16,23,24,27,39,42,58,60,64,72,74,78,78,78,80,80,84,85,86,88,88,90,92,93,94,95,96};
int param0_7[] = {-68,-48,36,22,-80,-48,-74,-14,44,-46,-76,18,-16,-36,-68,0,-30,-56,42,92,82,64,-18,-6,-78,-86,26,86,36,-66,-50,18,-26,48,8};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {3,76,99,1,1,29,9,12,57,12,74,22,83,77,39,84,50,60,36,90,88,62,79,58,58,40,44,99,84,63,23,21,16,98,68,8,46};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {23,7,31,37,34,15,22,20,23,35};
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