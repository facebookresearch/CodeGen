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

int f_gold ( int a [ ], int b [ ], int n ) {
  sort ( a, a + n );
  sort ( b, b + n );
  int result = 0;
  for ( int i = 0;
  i < n;
  ++ i ) {
    result = result + abs ( a [ i ] - b [ i ] );
  }
  return result;
}


int f_filled ( int a [ ], int b [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,6,6,7,10,11,13,18,19,19,19,31,34,37,37,40,41,41,47,47,53,54,55,55,56,56,60,60,62,62,66,73,75,76,78,81,81,85,88,90,91,92,93,95,97,98};
int param0_1[] = {-12,-6,78,62,86,-32};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1};
int param0_3[] = {76,74};
int param0_4[] = {-92,-90,-88,-84,-76,-54,-44,-42,-38,-30,34,42};
int param0_5[] = {1,1,0,0,1,1,1,0,1,1,0,0,1,0,0,1,1,1};
int param0_6[] = {4,5,6,13,16,24,36,40,40,44,47,52,58,58,59,63,66,67,69,70,74,77,81,88,89,90,94,96};
int param0_7[] = {-16,66,-2,54,-8,10,44,-36,-54,50,92,84,-36,40,-12,98,36,22,-10};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {42,24,43,64,55,94,26,30,76,3,37,43,81,7,15,64,63,88,34,8,55,32,19,55};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {2,2,4,7,8,8,8,8,8,9,9,12,15,16,21,25,26,27,29,34,34,35,38,40,40,44,44,47,48,54,58,61,63,64,66,69,69,70,73,74,75,76,79,80,80,93};
int param1_1[] = {-86,20,32,52,50,-60};
int param1_2[] = {0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1};
int param1_3[] = {16,98};
int param1_4[] = {-80,-54,-34,12,14,16,16,46,50,64,84,92};
int param1_5[] = {0,1,1,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1};
int param1_6[] = {1,7,10,17,21,22,22,27,36,37,39,46,52,53,56,59,65,67,70,75,78,78,79,89,89,94,96,97};
int param1_7[] = {-76,-74,62,22,50,84,78,26,-62,-10,86,-10,-92,-10,86,-6,-58,-26,-18};
int param1_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_9[] = {96,11,63,90,28,80,44,63,17,81,80,69,66,22,81,4,86,74,91,17,3,81,65,98};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {23,4,14,1,8,14,24,16,36,22};
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