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
  unordered_map < int, int > um;
  int mod_arr [ n ], max = 0;
  int curr_sum = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    curr_sum += arr [ i ];
    mod_arr [ i ] = ( ( curr_sum % k ) + k ) % k;
  }
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( mod_arr [ i ] == 0 ) max = i + 1;
    else if ( um . find ( mod_arr [ i ] ) == um . end ( ) ) um [ mod_arr [ i ] ] = i;
    else if ( max < ( i - um [ mod_arr [ i ] ] ) ) max = i - um [ mod_arr [ i ] ];
  }
  return max;
}


int f_filled ( int arr [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {14,16,17,17,31,32,34,35,37,38,39,46,47,52,57,58,60,61,69,75,76,77,81,88,97};
int param0_1[] = {-16,64,-62,-86,10,-40,52,50,-42,34,-32,-32,90,72,-96,-46,-6,92,14,98,-66,96,-48,-80,-22,-82,-50,-60,-70,82,-78,-68,88,-56,24,-52};
int param0_2[] = {0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_3[] = {33,1,92,27,17,46,79,78,95,34,3,56,12,26,24,60,58,63,98,8,76,73,26,58,38,49,43,59,83,21,13,99,3,89,32,21,14,95,8,7,99,83,59,2,69,44,66};
int param0_4[] = {-92,-76,-58,-56,-54,-20,-18,-16,-14,8,20,52,72,82,82,84};
int param0_5[] = {1,0,1,1,0,0,1,0,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,1,1,0,0,1,0,1,0,0,0,0};
int param0_6[] = {7,7,8,9,13,14,16,18,19,20,24,24,30,32,32,45,49,55,62,62,84,90,90,93,95,98};
int param0_7[] = {-28,-52,-84,-98,48,74,48,-34,-38,54};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {30,44,9,92,82,11,66,22,87,20};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {23,35,13,40,15,34,22,7,28,9};
    int param2[] = {23,21,13,37,15,26,14,8,37,9};
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