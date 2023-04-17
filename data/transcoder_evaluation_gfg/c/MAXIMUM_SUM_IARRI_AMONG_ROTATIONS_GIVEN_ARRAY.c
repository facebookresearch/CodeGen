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
  int res = INT_MIN;
  for ( int i = 0;
  i < n;
  i ++ ) {
    int curr_sum = 0;
    for ( int j = 0;
    j < n;
    j ++ ) {
      int index = ( i + j ) % n;
      curr_sum += j * arr [ index ];
    }
    res = max ( res, curr_sum );
  }
  return res;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {11,12,16,26,29,40,54,59,65,70,71,73,78,81,87,87,88,90,95,97};
int param0_1[] = {-46,-32,54,96,-72,-58,-36,-44,26,-2,-68,42,90,26,-92,-96,88,-42,-18,46,-70,24,0,24,34,34,-52,50,94,-60,64,58};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {48,2,79,98,28,17,41,47,61,76,82,5,74,4,80,51,22,45,91,75,91,93,42,45,69,98,76,74,83,17,30,88,53,25,35,19,26};
int param0_4[] = {-88,-84,-82,-74,-44,-34,-32,-20,-20,-14,6,6,10,12,16,24,32,34,38,46,54,54,56,60,82,88,90,94,98};
int param0_5[] = {0,1,1,1,1,0,1,1,1,1,1,1,1};
int param0_6[] = {10,14,14,14,19,20,22,26,35,36,40,53,54,55,55,57,57,67,72,72,77,78,83,84,95,96};
int param0_7[] = {-80,18,-76,48,-52,-38,52,-82,40,-44,-90,86,-86,-36,-32,-2,56,-12,-88,14,-16,8,52,24,46,56,84,-36,84,-60,72,-46,32,-16,-20,68,-86,-62,58,8,78,-52,22,-28,-22,-42,12,-48};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1};
int param0_9[] = {20,94,36,2,50,62,84,50,66,75,1,18,41,48,72,61,86,22,54,6,71,46,92,68,59,51,89,31,58,78,82,84};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {11,22,33,20,24,7,16,30,14,25};
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