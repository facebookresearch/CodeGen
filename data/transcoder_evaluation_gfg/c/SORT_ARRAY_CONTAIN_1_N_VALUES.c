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
  for ( int i = 0;
  i < n;
  i ++ ) {
    arr [ i ] = i + 1;
  }
}


void f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {3,3,6,7,9,11,15,15,17,19,21,23,26,27,37,48,48,51,53,53,59,64,69,69,70,71,72,84,93,96};
int param0_1[] = {66,-28,6,25,-65,19,-86,-86,-90,40,-62};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {85,84,8,36,93,76,14,54,85,86};
int param0_4[] = {-90,-82,-80,-73,-67,-62,-62,-61,-58,-56,-56,-52,-50,-49,-49,-43,-43,-30,-26,-26,-15,-14,-13,-4,10,19,20,22,26,29,34,35,37,45,49,52,54,66,67,80,84,87,89,90};
int param0_5[] = {1,1,0,0,0,1,0,1,1,1,0,0,0,1,0,1,0,0,1,1,0,0,0,1,1,0,0,1,0,1,1,1};
int param0_6[] = {10,11,13,19,19,30,33,36,40,42,44,47,49,52,53,58,66,68,72,82,87,89,90,94};
int param0_7[] = {-46,-35,40,-76,-66,-47,36,-82,-43,12,-95,54,58,82,-87,-17,-71,-97,-10,4,23,86,-24};
int param0_8[] = {0,0,0,0,0,1,1,1,1,1,1};
int param0_9[] = {88,76,16,23,40,60,73,32,15,13,5,75,74,52,77,41,53,50,15,7,40,28,32,99,15,85};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {19,8,26,9,31,29,21,12,6,18};
    int filled_function_param0_0[] = {3,3,6,7,9,11,15,15,17,19,21,23,26,27,37,48,48,51,53,53,59,64,69,69,70,71,72,84,93,96};
int filled_function_param0_1[] = {66,-28,6,25,-65,19,-86,-86,-90,40,-62};
int filled_function_param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int filled_function_param0_3[] = {85,84,8,36,93,76,14,54,85,86};
int filled_function_param0_4[] = {-90,-82,-80,-73,-67,-62,-62,-61,-58,-56,-56,-52,-50,-49,-49,-43,-43,-30,-26,-26,-15,-14,-13,-4,10,19,20,22,26,29,34,35,37,45,49,52,54,66,67,80,84,87,89,90};
int filled_function_param0_5[] = {1,1,0,0,0,1,0,1,1,1,0,0,0,1,0,1,0,0,1,1,0,0,0,1,1,0,0,1,0,1,1,1};
int filled_function_param0_6[] = {10,11,13,19,19,30,33,36,40,42,44,47,49,52,53,58,66,68,72,82,87,89,90,94};
int filled_function_param0_7[] = {-46,-35,40,-76,-66,-47,36,-82,-43,12,-95,54,58,82,-87,-17,-71,-97,-10,4,23,86,-24};
int filled_function_param0_8[] = {0,0,0,0,0,1,1,1,1,1,1};
int filled_function_param0_9[] = {88,76,16,23,40,60,73,32,15,13,5,75,74,52,77,41,53,50,15,7,40,28,32,99,15,85};
int *filled_function_param0[10] = {filled_function_param0_0,filled_function_param0_1,filled_function_param0_2,filled_function_param0_3,filled_function_param0_4,filled_function_param0_5,filled_function_param0_6,filled_function_param0_7,filled_function_param0_8,filled_function_param0_9};
    int filled_function_param1[] = {19,8,26,9,31,29,21,12,6,18};
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