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
  int a = 0, b = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( i & 1 ) a = a * 10 + arr [ i ];
    else b = b * 10 + arr [ i ];
  }
  return a + b;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {3,4,5,10,14,16,18,42,43,43,45,46,51,52,53,58,61,66,79,81,82,84};
int param0_1[] = {48,-22,60,32,48,-2,-76,-50,-26,56,-86,98,-30,-22,82,-20,58,40,76,-2,82,-90,8,-46,22,94};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {79,45};
int param0_4[] = {-90,-68,-38,-34,-4,6,10,28,48,52,54,68,88,90};
int param0_5[] = {1,0,0,1,0,1,0,1,0,1,0,0,1,1,1,1,0,0,1,1,0,1,1,0};
int param0_6[] = {4,8,8,23,26,27,30,42,44,55,59,64,67,69,74,77,82,82,87,96,97};
int param0_7[] = {0,-18,-98,-36,-62,0,-32,-98,46,72,-18,30,-86,-42,-82,2,-76,-64,-66,-48,-28,52,-46,-76,76,10,70,4,18,94,88,80,-60,-36,62,96,-4,88,50};
int param0_8[] = {0,0,0,0,0,0,1,1,1,1};
int param0_9[] = {8,71,75,58,97,24,56,98,71,69,32,64,54,96,69,22,7,47,45,68,17,36,90,9,71,86,16,61,53,63,9,74,38,87,14,86,42,42,14,43,58,82,72,73,32};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {19,25,23,1,11,22,17,32,6,25};
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