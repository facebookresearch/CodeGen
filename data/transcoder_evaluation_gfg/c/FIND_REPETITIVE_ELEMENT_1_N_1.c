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
  return accumulate ( arr, arr + n, 0 ) - ( ( n - 1 ) * n / 2 );
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,8,27,34,39,42,43,54,72};
int param0_1[] = {-38,-66,-38,-48,-96,74,-32,-62,-34,-32,-88,-12,-8,-4};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1};
int param0_3[] = {88,86,23,81,76,16,94,64,59,50,71,62,10,89,73,64,65,96,83,40,99,40,77,33,14,62,6,89,74,96,93,29,15,93,9,58,98,76,23,23,70,99};
int param0_4[] = {-96,-94,-82,-64,-56,-40,-36,-34,-32,-24,-24,-22,-20,-20,-20,-18,-18,-12,-10,-6,16,20,20,22,26,30,36,46,46,50,50,52,64,64,64,68,72,74,76,92,96,98};
int param0_5[] = {0,1,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1,1,0,1,1};
int param0_6[] = {2,6,7,13,19,23,37,39,42,42,43,45,52,53,55,56,59,63,66,71,76,85,86,89,92,94,96,99};
int param0_7[] = {52,-56,-12,78,6,32,0,36,34,-54,-74,-32};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {10,42,50,5,74,81,30,76,6,34,86,4,77,71,96,22,34,50,35,16,60,11,21,38};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {5,9,8,31,28,25,27,11,15,13};
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