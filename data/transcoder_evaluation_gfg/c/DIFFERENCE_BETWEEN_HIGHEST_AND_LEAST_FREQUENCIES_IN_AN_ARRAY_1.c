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
  unordered_map < int, int > hm;
  for ( int i = 0;
  i < n;
  i ++ ) hm [ arr [ i ] ] ++;
  int max_count = 0, min_count = n;
  for ( auto x : hm ) {
    max_count = max ( max_count, x . second );
    min_count = min ( min_count, x . second );
  }
  return ( max_count - min_count );
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,3,23,24,39,53,55,57,59,60,68,87};
int param0_1[] = {-76,46,50,90,-98,98,8,-14,24,-70,-86,-44,-88,-60,76,-16,-24,24,52,-94,-44,-76,60,-12,-70,10,90,70,64,-4,-88,28,62,74,-30,64,-78,-54,14,62,40,76,-26,26};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {61,48,24,48,26,49,90,88,55,4,49};
int param0_4[] = {-94,-80,-76,-72,-66,-62,-62,-60,-58,-48,-46,-42,-30,-20,-12,0,8,22,30,36,52,58,64,64,66,66,70,74,78,84,84,92,94,96};
int param0_5[] = {1,1,0,1,1,1,0,0,0,0,1,0,0,1,1,1,0,1,0,0,0,1,1,1,1,0,0,1,0,0,0,1,0,1};
int param0_6[] = {4,9,20,22,24,29,30,34,51,54,55,60,76,94,99};
int param0_7[] = {2,46,72,0,60,32,24,-12,-54,86,-78,8,10,22,98,4,-56,-94,52,30,16,-14,80,96,22,86,6,-34,92,-50,0,-6,16,32,58,-74,-16,-70,-88,70,-16};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {76,63,32,60,35,16,36,56,30,32,79,21,56,40,93,54,30,89,20,74,95,1,74,18,57,59,13};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {7,37,19,6,30,33,11,22,33,26};
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