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

void f_gold ( int arr [ ], int n ) {
  int max_idx = n - 1, min_idx = 0;
  int max_elem = arr [ n - 1 ] + 1;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( i % 2 == 0 ) {
      arr [ i ] += ( arr [ max_idx ] % max_elem ) * max_elem;
      max_idx --;
    }
    else {
      arr [ i ] += ( arr [ min_idx ] % max_elem ) * max_elem;
      min_idx ++;
    }
  }
  for ( int i = 0;
  i < n;
  i ++ ) arr [ i ] = arr [ i ] / max_elem;
}


void f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,1,2,3,9,10,14,22,26,28,29,29,30,32,32,32,34,37,39,40,42,42,42,43,45,47,49,52,53,54,56,58,59,68,71,73,76,81,81,83,84,91,94};
int param0_1[] = {50,46,6,-57,67,34,-52,26,-93,97,-84,29,15,-63,65,25,-19,92,-38,-28,89,25,61,-34,-70,-80,88,-18,7,52,32,-63,32,-23,-11,46,-12,94,76,-67,-42};
int param0_2[] = {0,0,0,0,0,0,1,1,1};
int param0_3[] = {15,99,57,69,22,64,41,87,71,56,23,25,91,6,34,63,9,60,49,97,51,60,70,37,31,98,41,62,93,58,14,36,36,79,8,26,36,48,85,28,68,62,80,86,76,80,51};
int param0_4[] = {-99,-99,-90,-90,-85,-85,-79,-77,-72,-71,-67,-66,-61,-39,-39,-35,-35,-23,-20,-18,-16,-13,-2,1,5,6,10,24,27,32,33,38,48,67,70,76,82,88};
int param0_5[] = {0,0,0,1,0,1,0,1,1,1,0,0,0,1,0,0,0,0,1,1,0,0,0,1,0,1,1,0,0,0,1,1,0,1,0,0,1,1,1,1,0,0,0,1,0};
int param0_6[] = {2,22,32,34,43,66,70,74,94,94};
int param0_7[] = {-99,-28,76,-50,41,-85,-47,72,-92,-26,-54,-31,14,47,66,23};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {19,31,26,42,41,23,47,13,89,66,66,16,73,28,77,35,41,77,31,85,32,54,98,72,59};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {29,38,4,30,34,33,6,10,42,20};
    int filled_function_param0_0[] = {1,1,2,3,9,10,14,22,26,28,29,29,30,32,32,32,34,37,39,40,42,42,42,43,45,47,49,52,53,54,56,58,59,68,71,73,76,81,81,83,84,91,94};
int filled_function_param0_1[] = {50,46,6,-57,67,34,-52,26,-93,97,-84,29,15,-63,65,25,-19,92,-38,-28,89,25,61,-34,-70,-80,88,-18,7,52,32,-63,32,-23,-11,46,-12,94,76,-67,-42};
int filled_function_param0_2[] = {0,0,0,0,0,0,1,1,1};
int filled_function_param0_3[] = {15,99,57,69,22,64,41,87,71,56,23,25,91,6,34,63,9,60,49,97,51,60,70,37,31,98,41,62,93,58,14,36,36,79,8,26,36,48,85,28,68,62,80,86,76,80,51};
int filled_function_param0_4[] = {-99,-99,-90,-90,-85,-85,-79,-77,-72,-71,-67,-66,-61,-39,-39,-35,-35,-23,-20,-18,-16,-13,-2,1,5,6,10,24,27,32,33,38,48,67,70,76,82,88};
int filled_function_param0_5[] = {0,0,0,1,0,1,0,1,1,1,0,0,0,1,0,0,0,0,1,1,0,0,0,1,0,1,1,0,0,0,1,1,0,1,0,0,1,1,1,1,0,0,0,1,0};
int filled_function_param0_6[] = {2,22,32,34,43,66,70,74,94,94};
int filled_function_param0_7[] = {-99,-28,76,-50,41,-85,-47,72,-92,-26,-54,-31,14,47,66,23};
int filled_function_param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int filled_function_param0_9[] = {19,31,26,42,41,23,47,13,89,66,66,16,73,28,77,35,41,77,31,85,32,54,98,72,59};
int *filled_function_param0[10] = {filled_function_param0_0,filled_function_param0_1,filled_function_param0_2,filled_function_param0_3,filled_function_param0_4,filled_function_param0_5,filled_function_param0_6,filled_function_param0_7,filled_function_param0_8,filled_function_param0_9};
    int filled_function_param1[] = {29,38,4,30,34,33,6,10,42,20};
    for(int i = 0; i < len(param0); ++i)
    {
        f_filled(filled_function_param0[i],filled_function_param1[i]);
        f_gold(param0[i],param1[i]);
        if(equal(begin(param0[i]), end(param0[i]), begin(filled_function_param0[i])) && param1[i] == filled_function_param1[i])
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}