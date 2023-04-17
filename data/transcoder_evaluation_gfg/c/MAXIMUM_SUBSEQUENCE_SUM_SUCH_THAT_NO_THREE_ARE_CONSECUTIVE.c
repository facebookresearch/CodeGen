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
  int sum [ n ];
  if ( n >= 1 ) sum [ 0 ] = arr [ 0 ];
  if ( n >= 2 ) sum [ 1 ] = arr [ 0 ] + arr [ 1 ];
  if ( n > 2 ) sum [ 2 ] = max ( sum [ 1 ], max ( arr [ 1 ] + arr [ 2 ], arr [ 0 ] + arr [ 2 ] ) );
  for ( int i = 3;
  i < n;
  i ++ ) sum [ i ] = max ( max ( sum [ i - 1 ], sum [ i - 2 ] + arr [ i ] ), arr [ i ] + arr [ i - 1 ] + sum [ i - 3 ] );
  return sum [ n - 1 ];
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {5,6,8,9,10,10,16,17,17,20,21,22,23,28,29,32,36,37,40,41,42,43,47,47,48,48,49,49,52,52,53,59,61,64,65,79,79,81,87,91,92,98};
int param0_1[] = {98,76,-80,-30,82,52,-14,28,98,18,82,52,26,-62,-8};
int param0_2[] = {0,0,0,0,0,1,1,1,1};
int param0_3[] = {21,26,85,73,47,10,54,9,11,70,42,95,44,91};
int param0_4[] = {-94,-92,-90,-84,-76,-68,-60,-50,-34,-34,-20,-16,-6,18,50,54,66,70,96};
int param0_5[] = {1,0,1,1,1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1};
int param0_6[] = {2,3,4,4,14,14,18,21,24,26,29,31,32,34,36,37,38,40,42,44,44,54,63,69,77,77,82,82,86,87,90,93,95};
int param0_7[] = {-46,64,-44,88,-74,54,40,-2,-24,94,40,-44,56,-54,-60,-86,-58,48,-90,12,-76,-30,94,-34,14,12,80,-40,60};
int param0_8[] = {0,0,0,0,0,0,0,0,0,1,1,1,1,1};
int param0_9[] = {4,32,63,23,44,57,59,69,88,61,66,61,65,33,79,58,71,2,80,41,83,12,20,9,7,40,36,97,10,98,66,78,71,37,53};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {35,7,7,12,9,16,31,22,7,26};
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