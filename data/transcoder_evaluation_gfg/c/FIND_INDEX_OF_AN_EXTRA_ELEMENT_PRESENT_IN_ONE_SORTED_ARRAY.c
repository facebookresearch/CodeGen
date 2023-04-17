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

int f_gold ( int arr1 [ ], int arr2 [ ], int n ) {
  for ( int i = 0;
  i < n;
  i ++ ) if ( arr1 [ i ] != arr2 [ i ] ) return i;
  return n;
}


int f_filled ( int arr1 [ ], int arr2 [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,6,7,10,11,12,12,16,17,29,32,33,35,35,45,49,52,56,57,58,61,62,63,64,68,71,71,77,79,79,81,82,82,83,83,89,89,93,94,94};
int param0_1[] = {-48,-92,96,-18,10,-24,-4,96,-16,-78,4,-80,-96,-28,-78,68,2,-60,0};
int param0_2[] = {1};
int param0_3[] = {68,98,21,29,71,49};
int param0_4[] = {-80,-76,-76,-76,-68,-66,-56,-44,-38,-28,-24,-10,8,14,16,18,24,26,30,32,50,64,76,80,90,94,94,94};
int param0_5[] = {0,0,1,0,1,0,1,1,1,1,0,1,0,0,0,1,1,1,1,1,1,1,1,0,0,1,0,1,0,1,0,1,1,1,0,1};
int param0_6[] = {3,7,16,17,20,22,29,32,34,34,35,40,40,40,41,46,49,58,60,62,63,64,64,68,70,73,76,79,83,86,90,92,99};
int param0_7[] = {18,-68,-6,-32,-76,-86,-8,76,-46,20,-80,54,-88,-58,-48,-66,-66,18,-28,-74,-72,-26,-92,-78,24,-22,-80,-80,82,-2,-72,-88,-54,-84,-8};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {74,75,52,58,34,53,51,45,34,28,53,94,10,20,23,12,95,78,48,11};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {3,12,13,14,15,17,18,19,22,24,28,29,33,37,41,42,44,49,51,51,52,53,56,56,59,60,64,64,67,70,71,78,83,88,88,90,92,93,93,95};
int param1_1[] = {-38,-40,-50,50,-26,-80,64,54,74,-44,-40,-92,-16,4,-60,-42,-60,-74,38};
int param1_2[] = {0};
int param1_3[] = {97,90,25,89,57,41};
int param1_4[] = {-90,-88,-66,-60,-48,-48,-46,-42,-40,-36,-26,-4,2,4,4,8,16,18,34,50,52,56,64,80,86,90,92,96};
int param1_5[] = {0,0,0,0,0,1,1,1,1,1,1,1,1,0,1,0,1,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,1,0,0,1};
int param1_6[] = {4,4,7,13,23,23,25,25,26,34,38,39,39,45,48,50,52,54,58,59,60,65,72,76,80,80,80,84,87,90,92,94,96};
int param1_7[] = {-30,96,92,-12,-14,-68,-16,20,74,-42,36,84,-82,66,44,70,-92,-56,-28,-68,-4,10,-4,90,72,84,68,14,32,60,40,60,-34,58,-56};
int param1_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_9[] = {62,56,17,1,11,30,59,18,99,21,86,49,24,85,25,56,21,66,23,96};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {36,16,0,3,14,22,26,17,24,17};
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