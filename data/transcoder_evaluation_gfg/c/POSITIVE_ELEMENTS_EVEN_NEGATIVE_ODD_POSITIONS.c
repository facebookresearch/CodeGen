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

void f_gold ( int a [ ], int size ) {
  int positive = 0, negative = 1;
  while ( true ) {
    while ( positive < size && a [ positive ] >= 0 ) positive += 2;
    while ( negative < size && a [ negative ] <= 0 ) negative += 2;
    if ( positive < size && negative < size ) swap ( a [ positive ], a [ negative ] );
    else break;
  }
}


void f_filled ( int a [ ], int size ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {8,11,18,23,24,28,28,34,35,42,44,53,57,65,71,72,76,78,82,82,85,86,92,93};
int param0_1[] = {0,-95,-51,-2,-70,-28,3,-37,75,-74,85,-63,-93,27,68,-8,67,90,3,-47,32,8,12,53,-93,56,97};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {28,85,78,33,10,83,30,22,3,82,75,48,2,76,54,6,40,93,94};
int param0_4[] = {-98,-94,-7,-3,1,11,11,83,88};
int param0_5[] = {0,0,1,0,0,0,1,0,1,1,1,0,0,1,1,0,1,1,0,1,0,0,1,0,0,0,1,1,1,0,0,1,1,0,1,1,1,1,1,0};
int param0_6[] = {8,35,37,38,39,46,49,54};
int param0_7[] = {-60,-66,-4,-21,27,-83,61,75,10,-48,18,-91,-67,88,13,49,86,-15,97,-90,-94,15,21,41,-35,-80,-43,-54};
int param0_8[] = {0,0,0,0,0,0,0,0,1,1};
int param0_9[] = {62,36,39,53,90,78,56,1,56,4,30};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {15,15,40,10,7,35,6,21,5,8};
    int filled_function_param0_0[] = {8,11,18,23,24,28,28,34,35,42,44,53,57,65,71,72,76,78,82,82,85,86,92,93};
int filled_function_param0_1[] = {0,-95,-51,-2,-70,-28,3,-37,75,-74,85,-63,-93,27,68,-8,67,90,3,-47,32,8,12,53,-93,56,97};
int filled_function_param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int filled_function_param0_3[] = {28,85,78,33,10,83,30,22,3,82,75,48,2,76,54,6,40,93,94};
int filled_function_param0_4[] = {-98,-94,-7,-3,1,11,11,83,88};
int filled_function_param0_5[] = {0,0,1,0,0,0,1,0,1,1,1,0,0,1,1,0,1,1,0,1,0,0,1,0,0,0,1,1,1,0,0,1,1,0,1,1,1,1,1,0};
int filled_function_param0_6[] = {8,35,37,38,39,46,49,54};
int filled_function_param0_7[] = {-60,-66,-4,-21,27,-83,61,75,10,-48,18,-91,-67,88,13,49,86,-15,97,-90,-94,15,21,41,-35,-80,-43,-54};
int filled_function_param0_8[] = {0,0,0,0,0,0,0,0,1,1};
int filled_function_param0_9[] = {62,36,39,53,90,78,56,1,56,4,30};
int *filled_function_param0[10] = {filled_function_param0_0,filled_function_param0_1,filled_function_param0_2,filled_function_param0_3,filled_function_param0_4,filled_function_param0_5,filled_function_param0_6,filled_function_param0_7,filled_function_param0_8,filled_function_param0_9};
    int filled_function_param1[] = {15,15,40,10,7,35,6,21,5,8};
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