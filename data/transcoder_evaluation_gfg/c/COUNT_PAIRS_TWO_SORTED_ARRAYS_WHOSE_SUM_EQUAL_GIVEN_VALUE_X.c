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

int f_gold ( int arr1 [ ], int arr2 [ ], int m, int n, int x ) {
  int count = 0;
  for ( int i = 0;
  i < m;
  i ++ ) for ( int j = 0;
  j < n;
  j ++ ) if ( ( arr1 [ i ] + arr2 [ j ] ) == x ) count ++;
  return count;
}


int f_filled ( int arr1 [ ], int arr2 [ ], int m, int n, int x ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {11,13,16,23,26,28,31,34,37,39,44,48,56,59,79,91,96,98};
int param0_1[] = {50,14,-98,14,90,36,66,44,10,-98,-24,-36,-32,-50};
int param0_2[] = {0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {88,14,29,87,86,58};
int param0_4[] = {-98,-92,-88,-86,-82,-76,-72,-66,-56,-48,-34,-28,-28,-26,-20,-18,-18,-16,-16,-12,-4,0,6,12,16,20,22,30,34,34,36,56,58,62,64,80,82,94};
int param0_5[] = {1,1,1,1,0,1,1,0,0,0,1,1,1,1,1,0,0,0,1,0,0,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,1,0,1,1,1,0,0};
int param0_6[] = {70,70,74};
int param0_7[] = {-20,-12,-50,76,24,64,-22,-4,-68};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {68,75,51,45,73,95,48,53,70,41,65,47,46,43,79,29,50};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {1,1,9,14,17,23,26,31,33,36,53,60,71,75,76,84,87,88};
int param1_1[] = {34,-6,-66,0,-6,82,60,-98,-8,60,-2,4,22,76};
int param1_2[] = {0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param1_3[] = {91,95,64,4,63,35};
int param1_4[] = {-94,-90,-88,-84,-82,-78,-76,-72,-70,-58,-58,-46,-42,-40,-40,-32,-22,-20,-18,-12,-8,-6,6,6,18,20,34,46,60,62,66,72,72,76,76,78,92,98};
int param1_5[] = {1,0,1,1,0,0,1,0,1,0,1,0,1,0,0,0,1,1,0,1,1,0,1,1,1,0,1,0,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,1,0,0};
int param1_6[] = {15,55,84};
int param1_7[] = {18,98,-88,86,72,-44,82,94,58};
int param1_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_9[] = {4,6,76,65,16,13,85,43,31,14,81,90,24,87,40,25,88};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {9,11,14,3,34,39,1,5,27,10};
    int param3[] = {15,12,9,5,32,26,1,4,26,10};
    int param4[] = {11,8,12,5,23,34,1,7,37,9};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i],param4[i]) == f_gold(param0[i],param1[i],param2[i],param3[i],param4[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}