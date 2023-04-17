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
  i ++ ) if ( arr [ i ] & 1 ) arr [ i ] *= - 1;
  sort ( arr, arr + n );
  for ( int i = 0;
  i < n;
  i ++ ) if ( arr [ i ] & 1 ) arr [ i ] *= - 1;
}


void f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4};
int param0_1[] = {8,-74,89,65,51,-15,68,51,23,44,89};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {51,74,43,15,38,15,5,93};
int param0_4[] = {-96,-75,-64,-20,-5,-2,1,40,46,64};
int param0_5[] = {0,0,1,0,0,1,0,0,0};
int param0_6[] = {1,2,4,4,17,22,23,28,35,38,39,39,41,42,42,45,46,49,49,49,50,59,62,68,69,71,73,76,78,79,80,87,88,88,90,90,91,93,95,96,98};
int param0_7[] = {11,68,-52,-49,-57,-2,83,77,24,-20,85,11,43,-73,96,92,58,64,95,13,-14,14,24,-51,-24,-45,-44,96,-5,-56,59};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {44,7,44,68,34,66,69,55,10,96,42,41,77,69,10,10,91,60,51};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {0,8,28,6,7,5,34,24,14,13};
    int filled_function_param0_0[] = {4};
int filled_function_param0_1[] = {8,-74,89,65,51,-15,68,51,23,44,89};
int filled_function_param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int filled_function_param0_3[] = {51,74,43,15,38,15,5,93};
int filled_function_param0_4[] = {-96,-75,-64,-20,-5,-2,1,40,46,64};
int filled_function_param0_5[] = {0,0,1,0,0,1,0,0,0};
int filled_function_param0_6[] = {1,2,4,4,17,22,23,28,35,38,39,39,41,42,42,45,46,49,49,49,50,59,62,68,69,71,73,76,78,79,80,87,88,88,90,90,91,93,95,96,98};
int filled_function_param0_7[] = {11,68,-52,-49,-57,-2,83,77,24,-20,85,11,43,-73,96,92,58,64,95,13,-14,14,24,-51,-24,-45,-44,96,-5,-56,59};
int filled_function_param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1};
int filled_function_param0_9[] = {44,7,44,68,34,66,69,55,10,96,42,41,77,69,10,10,91,60,51};
int *filled_function_param0[10] = {filled_function_param0_0,filled_function_param0_1,filled_function_param0_2,filled_function_param0_3,filled_function_param0_4,filled_function_param0_5,filled_function_param0_6,filled_function_param0_7,filled_function_param0_8,filled_function_param0_9};
    int filled_function_param1[] = {0,8,28,6,7,5,34,24,14,13};
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