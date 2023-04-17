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

int f_gold ( int a [ ], int n ) {
  return floor ( ( - 1 + sqrt ( 1 + ( 8 * n ) ) ) / 2 );
}


int f_filled ( int a [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,2,2,3,5,6,7,8,8,12,15,16,18,18,20,21,21,22,22,24,24,25,30,35,42,49,52,55,55,63,68,70,72,73,77,80,83,87,87,88,88,94,95,97};
int param0_1[] = {48,-72,84,-24,28,94,36,28,32,66,-62,64,6,-68,-12,46,4,98,18,86,-60,76,14,98};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {11,16,84,8,86,44,79,11,73,12,29,62,22,44,28,8,48,92,73,63,59,44,95,66};
int param0_4[] = {-94,-94,-92,-88,-86,-82,-80,-80,-78,-76,-56,-56,-50,-44,-42,-36,-36,-32,-32,-26,-14,-12,-6,12,24,28,34,38,42,42,46,50,56,62,62,74,84,92,94};
int param0_5[] = {0,1,0,1,0,1,1,0,1,1,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,1,1,1,0,1,1,1,1,1,0,0};
int param0_6[] = {2,2,3,3,3,4,5,13,16,18,21,22,27,28,32,34,36,37,41,42,43,51,52,52,54,54,61,65,67,67,68,71,75,77,77,78,80,81,81,84,86,90,90,93,93,94,99,99};
int param0_7[] = {54,-86};
int param0_8[] = {0,1};
int param0_9[] = {5,54,49,80,56,62,31,49,60,19,45,94,33,46,32};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {22,12,25,14,19,24,31,1,1,8};
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