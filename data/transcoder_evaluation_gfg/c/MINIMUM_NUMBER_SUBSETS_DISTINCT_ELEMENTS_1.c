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
  unordered_map < int, int > mp;
  for ( int i = 0;
  i < n;
  i ++ ) mp [ arr [ i ] ] ++;
  int res = 0;
  for ( auto x : mp ) res = max ( res, x . second );
  return res;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,6,9,12,15,19,21,23,24,24,25,27,29,35,36,37,41,44,44,47,48,51,56,59,59,59,60,64,64,66,67,68,68,69,73,74,77,78,81,82,83,85,89,94,95,96,98,99};
int param0_1[] = {96,20,-40,74,-44,98,-24,92,58,-84,-76,-14,64,-2,-84,52,-8,38,-26,-10,-62,-30,-76,58};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {35,16,42,3,57,70,4,31,93,60,98,97,81,57,62,98,88,51,5,58,48,14,58,22,40,26,66,41,9,78,62,32,79,88,65,75,80,12,15,93,92,13,83,26};
int param0_4[] = {-62,-44,-36,-18,-16,-6,4,14,22,42,68,90};
int param0_5[] = {1,0,1,0,1,1,1,1,0,1,0,1,0,0,0,0};
int param0_6[] = {20,25,27,29,47,47,49,53,59,66,74,82,86,86,94,94,97};
int param0_7[] = {92,50,76,46,14,40,22};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {8,82,92,42,55,4,94,73,57,7,21,71,68,97};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {30,20,31,37,11,12,13,3,27,12};
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