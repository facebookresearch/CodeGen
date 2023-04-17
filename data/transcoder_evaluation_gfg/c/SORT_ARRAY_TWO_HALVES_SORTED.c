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

void f_gold ( int A [ ], int n ) {
  sort ( A, A + n );
}


void f_filled ( int A [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,3,11,13,18,24,26,30,31,34,42,43,43,44,44,47,49,52,53,55,56,57,58,58,60,64,66,67,69,70,70,71,74,76,77,82,85,89,90,96,98};
int param0_1[] = {-78,81,87,14,25,24,-70,-92,-2,-43,11,-27,15,-80,-75,-81,-95,-25,28,-28,55,-60,-74,-73,90,-17,28,78,70,57,67,88,69,-67,-3,11,-84,-77,35,-74,-4,-88,-28,33};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {6,46,50,38,88,18,27,41,72,92,74,17,62,29,58,70,78,22,6,26,39,12,99,14,22,51,23,48,71,50,89,13,85,10,55,9,79,52,2,25,13,98,51,58,34,35,3,59,70};
int param0_4[] = {-98,-88,-76,-71,-71,-63,-59,-58,-57,-42,-40,-37,-36,-34,-33,-33,-27,-26,-23,-9,-8,-6,-5,-1,0,3,16,21,29,30,33,39,39,43,47,50,52,60,63,66,73,74,76,77,92,92,96,97};
int param0_5[] = {1,0,0,1,1,1,0,1,0,0,0,1,1,1,0,1,0,0,0,0,0,0,1,0,1,0,1,1,1,1,0,0,0,0,1,1,1,0,1,0};
int param0_6[] = {46,86};
int param0_7[] = {58,-31,37,-15,-89,-31,-1,-9,94,59,61,67,-6,74,65,15,88,-69,-89,-13,21,30,5};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {94,5,98,22,77,57,47,54,3,53,84,31};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {33,31,15,46,42,31,1,21,19,10};
    int filled_function_param0_0[] = {2,3,11,13,18,24,26,30,31,34,42,43,43,44,44,47,49,52,53,55,56,57,58,58,60,64,66,67,69,70,70,71,74,76,77,82,85,89,90,96,98};
int filled_function_param0_1[] = {-78,81,87,14,25,24,-70,-92,-2,-43,11,-27,15,-80,-75,-81,-95,-25,28,-28,55,-60,-74,-73,90,-17,28,78,70,57,67,88,69,-67,-3,11,-84,-77,35,-74,-4,-88,-28,33};
int filled_function_param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1};
int filled_function_param0_3[] = {6,46,50,38,88,18,27,41,72,92,74,17,62,29,58,70,78,22,6,26,39,12,99,14,22,51,23,48,71,50,89,13,85,10,55,9,79,52,2,25,13,98,51,58,34,35,3,59,70};
int filled_function_param0_4[] = {-98,-88,-76,-71,-71,-63,-59,-58,-57,-42,-40,-37,-36,-34,-33,-33,-27,-26,-23,-9,-8,-6,-5,-1,0,3,16,21,29,30,33,39,39,43,47,50,52,60,63,66,73,74,76,77,92,92,96,97};
int filled_function_param0_5[] = {1,0,0,1,1,1,0,1,0,0,0,1,1,1,0,1,0,0,0,0,0,0,1,0,1,0,1,1,1,1,0,0,0,0,1,1,1,0,1,0};
int filled_function_param0_6[] = {46,86};
int filled_function_param0_7[] = {58,-31,37,-15,-89,-31,-1,-9,94,59,61,67,-6,74,65,15,88,-69,-89,-13,21,30,5};
int filled_function_param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int filled_function_param0_9[] = {94,5,98,22,77,57,47,54,3,53,84,31};
int *filled_function_param0[10] = {filled_function_param0_0,filled_function_param0_1,filled_function_param0_2,filled_function_param0_3,filled_function_param0_4,filled_function_param0_5,filled_function_param0_6,filled_function_param0_7,filled_function_param0_8,filled_function_param0_9};
    int filled_function_param1[] = {33,31,15,46,42,31,1,21,19,10};
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