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
  queue < int > q;
  sort ( arr, arr + n );
  q . push ( arr [ 0 ] );
  for ( int i = 1;
  i < n;
  i ++ ) {
    int now = q . front ( );
    if ( arr [ i ] >= 2 * now ) q . pop ( );
    q . push ( arr [ i ] );
  }
  return len(q);
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,3,17,17,18,28,28,29,34,43,44,52,54,80,84,84,91,92,97};
int param0_1[] = {-34,70,-90,-10,-26,64,4,28,24,-90,-78,72,74,80,82,-94};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {20,87,5,62,12,81,30,83,96,16,2,76,3,8,37,53,55,88};
int param0_4[] = {-94,-92,-60,-58,-54,-42,-36,-12,-8,-2,8,14,18,20,26,32,38,56,58,60,70,78,80,86,98};
int param0_5[] = {0,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0};
int param0_6[] = {1,1,2,3,3,11,16,18,19,21,21,22,22,24,27,28,29,43,43,52,55,57,60,62,62,63,65,66,70,70,73,77,78,79,79,80,85,85,86,88,89,90,97,98};
int param0_7[] = {88,12,-22,-60,30,-30,-14,80,-58,-80,-10,86,-94,-14,4,-18,-18,54,-82,-8,-68,-6,-44,-44,50,88,-78,-42,12,52,44,14,6,48,18,-30,4};
int param0_8[] = {0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_9[] = {82,62,43,39,5,90,75,50,16,83,52,69,71,3,89,10,51,69,32,96,5,43,83,12,31,81,22,59,52,47,86,49,56,90,31,59};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {12,10,40,9,18,9,30,21,7,28};
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