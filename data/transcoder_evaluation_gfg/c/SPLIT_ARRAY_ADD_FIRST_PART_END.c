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

void f_gold ( int arr [ ], int n, int k ) {
  for ( int i = 0;
  i < k;
  i ++ ) {
    int x = arr [ 0 ];
    for ( int j = 0;
    j < n - 1;
    ++ j ) arr [ j ] = arr [ j + 1 ];
    arr [ n - 1 ] = x;
  }
}


void f_filled ( int arr [ ], int n, int k ) {}


int main(void) {
    int n_success = 0;
    int param0_0[] = {75};
int param0_1[] = {-58,-60,-38,48,-2,32,-48,-46,90,-54,-18,28,72,86,0,-2,-74,12,-58,90,-30,10,-88,2,-14,82,-82,-46,2,-74};
int param0_2[] = {0,0,0,0,0,1,1,1,1,1,1};
int param0_3[] = {45,51,26,36,10,62,62,56,61,67,86,97,31,93,32,1,14,25,24,30,1,44,7,98,56,68,53,59,30,90,79,22};
int param0_4[] = {-88,-72,-64,-46,-40,-16,-8,0,22,34,44};
int param0_5[] = {0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,0,1,1,0,1,0,1,1,1,0,0,0,1,0,0,0,1,1,0,0,1,1,0,1,0,0,1,1,1,1,0};
int param0_6[] = {8,17,20,23,31,32,37,37,44,45,48,64,64,67,69,71,75,77,78,81,83,87,89,92,94};
int param0_7[] = {-8,-88,-68,48,8,50,30,-88,74,-16,6,74,36,32,22,96,-2,70,40,-46,98,34,2,94};
int param0_8[] = {0,0,0,0,1,1,1,1,1};
int param0_9[] = {80,14,35,25,60,86,45,95,32,29,94,6,63,66,38};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {0,27,7,23,6,23,21,23,5,9};
    int param2[] = {0,17,7,24,6,30,20,13,8,7};
    int filled_function_param0_0[] = {75};
int filled_function_param0_1[] = {-58,-60,-38,48,-2,32,-48,-46,90,-54,-18,28,72,86,0,-2,-74,12,-58,90,-30,10,-88,2,-14,82,-82,-46,2,-74};
int filled_function_param0_2[] = {0,0,0,0,0,1,1,1,1,1,1};
int filled_function_param0_3[] = {45,51,26,36,10,62,62,56,61,67,86,97,31,93,32,1,14,25,24,30,1,44,7,98,56,68,53,59,30,90,79,22};
int filled_function_param0_4[] = {-88,-72,-64,-46,-40,-16,-8,0,22,34,44};
int filled_function_param0_5[] = {0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,0,1,1,0,1,0,1,1,1,0,0,0,1,0,0,0,1,1,0,0,1,1,0,1,0,0,1,1,1,1,0};
int filled_function_param0_6[] = {8,17,20,23,31,32,37,37,44,45,48,64,64,67,69,71,75,77,78,81,83,87,89,92,94};
int filled_function_param0_7[] = {-8,-88,-68,48,8,50,30,-88,74,-16,6,74,36,32,22,96,-2,70,40,-46,98,34,2,94};
int filled_function_param0_8[] = {0,0,0,0,1,1,1,1,1};
int filled_function_param0_9[] = {80,14,35,25,60,86,45,95,32,29,94,6,63,66,38};
int *filled_function_param0[10] = {filled_function_param0_0,filled_function_param0_1,filled_function_param0_2,filled_function_param0_3,filled_function_param0_4,filled_function_param0_5,filled_function_param0_6,filled_function_param0_7,filled_function_param0_8,filled_function_param0_9};
    int filled_function_param1[] = {0,27,7,23,6,23,21,23,5,9};
    int filled_function_param2[] = {0,17,7,24,6,30,20,13,8,7};
    for(int i = 0; i < len(param0); ++i)
    {
        f_filled(filled_function_param0[i],filled_function_param1[i],filled_function_param2[i]);
        f_gold(param0[i],param1[i],param2[i]);
        if(equal(begin(param0[i]), end(param0[i]), begin(filled_function_param0[i])) && param1[i] == filled_function_param1[i] && param2[i] == filled_function_param2[i])
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}