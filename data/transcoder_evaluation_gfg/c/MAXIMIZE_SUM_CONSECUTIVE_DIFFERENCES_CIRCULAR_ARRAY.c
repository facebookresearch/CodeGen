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
  int sum = 0;
  sort ( arr, arr + n );
  for ( int i = 0;
  i < n / 2;
  i ++ ) {
    sum -= ( 2 * arr [ i ] );
    sum += ( 2 * arr [ n - i - 1 ] );
  }
  return sum;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {8,9,12,13,17,21,24,29,37,37,39,40,41,45,49,50,53,54,56,59,60,60,70,71,72,74,77,77,78,85,89,89,90,90,95,98,98};
int param0_1[] = {0,48,-32,28,-84,14,30,-80,92,76,-52,-20,52,78,20,32,96,66,48,26,88,6,94,32,-40,44,-84,54,-84,-80,-80,-64,-92,-84,-16,-18};
int param0_2[] = {0,0,0,1,1,1};
int param0_3[] = {47,7,84,96,59,53,80};
int param0_4[] = {-88,-80,-68,-62,-60,-60,-48,-46,-44,-38,-16,-16,0,0,2,8,20,36,40,40,44,54,60,68,70,82,82,84,92,94,96};
int param0_5[] = {1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,0,0,0,1,1,0,1,0,0,0,0,1,0,1,1,1,1,1,0,0,0,1,0,0,1,0,0,0,1,0,1,1};
int param0_6[] = {2,5,10,11,13,14,15,17,17,23,23,24,27,27,28,29,30,40,42,43,46,47,51,52,57,64,65,73,74,75,76,77,81,81,82,87,89,93,95,95,99};
int param0_7[] = {-72,-84,84,2,-76,48,12,-72,-92,-72,38,26,-38,26,50,2,20,26,-48,30,24,-12,-84,-54,20,-16,-94,26,-22,86};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {57,74,53,52,80,31,27,53,8,57,46,73,46,56,73,84,37,7,97};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {34,24,3,5,29,32,35,21,37,13};
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