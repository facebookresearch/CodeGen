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

int f_gold ( int A [ ], int n ) {
  int min_val = * min_element ( A, A + n );
  return ( min_val * ( n - 1 ) );
}


int f_filled ( int A [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,9,10,13,13,15,16,16,17,18,18,23,24,24,25,25,25,32,32,36,38,39,40,40,40,41,43,48,51,56,59,60,70,72,74,76,79,83,83,85,88,90,92,94,95,95};
int param0_1[] = {46,-10,56,46,-30,-68,50,8,72,-2,38,-12,20,-30,-38,-78,-18,-34,16,94,30,-86,36,88,-26,-56,-98,-92,96,-70,-78,-60,20,-54,36,-12,78,24,14,98,-14,-88,76,12};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {59,64,29,99,29,63,29,63,88,94,82,92,99,56,51,74,73,22,42,37,21,36,68,69,16,81,3,85,67,13,41,87,67,99,83,47,95,90,24,31,1,54,61,35,51,13};
int param0_4[] = {-98,-92,-82,-78,-76,-72,-64,-60,-44,-28,-22,-22,-14,-12,2,2,4,6,10,14,16,24,28,28,32,34,36,46,46,48,52,60,62,66,68,72,74,84,96};
int param0_5[] = {1,1,1,1,1,0,1};
int param0_6[] = {5,20,34,37,51,55,89};
int param0_7[] = {-70,78,-52,-82,-24,96,-32,8,-50,38,-76,-56,64,-28,-22,94,52,-32,66,-34,-30,14,42,98,96,-56,50,50,-24,-56,70,6,78,86,52,-40,92,46,46,-14,-74,40};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {51,42,29,30,65,42,7,2,90,85,1,47,79,98,90,66,47,54,32,83};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {26,25,32,45,31,6,3,33,26,19};
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