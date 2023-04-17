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
  sort ( arr, arr + n );
  int sum = 0;
  for ( int i = 0;
  i < n;
  i ++ ) sum += ( arr [ i ] * i );
  return sum;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,3,4,6,7,8,9,11,19,23,24,30,31,31,32,41,43,43,46,47,50,50,51,53,57,63,63,69,73,74,79,80,81,81,85,86,88,92,93,95,98,99};
int param0_1[] = {90,66,-98,-42,-10,90,-6,76,-80,-62,-40,90,-34,-76,90,-42,80,-74,10,-78,-16,32,52,-82,-98,-68,12,92,72,-10,98,76,-52,-58,62,68,20,-58};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1};
int param0_3[] = {79,52,45,58,44,13,14,99,8,44,42,98,47,44};
int param0_4[] = {-90,-88,-68,-66,-46,-42,-40,-20,-16,4,8,8,8,20,28,52,84,98};
int param0_5[] = {1,1,0,0,1,0,1,0,0,0,1,1,1,1,0,1,0,0,0,0,1};
int param0_6[] = {5,6,7,9,11,13,16,19,22,25,26,27,28,29,32,32,32,33,36,40,43,43,47,49,51,51,52,53,59,61,63,65,66,66,67,72,73,73,75,76,80,86,87,89,89,91,96,98,99};
int param0_7[] = {26,34,-26,-14,40,-20,54,48,-20,28,68,-78,-32,-96,-12,70,-24,92,-14,64,64,40,-8,88,-98,-4,-22,52,32,-52,2,6,-66,-38,-90,-48,-6,-30,76,32,96,-34,-12};
int param0_8[] = {0,0,1,1};
int param0_9[] = {84,32,75,21,62,49,88,49,47,20,49,18,71,34,88,44,84};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {22,24,13,11,14,13,42,39,3,8};
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