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

bool f_gold ( int arr [ ], int n ) {
  if ( n == 0 || n == 1 ) return true;
  for ( int i = 1;
  i < n;
  i ++ ) if ( arr [ i - 1 ] > arr [ i ] ) return false;
  return true;
}


bool f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {6,8,8,16,19,19,21,23,26,33,34,36,38,39,41,41,45,47,52,52,55,57,60,60,60,61,69,69,70,70,72,73,73,75,78,81,84,84,85,88,88,89,90,91,97};
int param0_1[] = {2,-90,66,24,-18,70,34,18,84,-62};
int param0_2[] = {1,1};
int param0_3[] = {12,88,65,82,23,39,60,27,57,44,70,28,23,34,25,11,48,65,10,73,26,10,18,60,73,45,26,9,36,15,24,40,2,4,95,20,39,45};
int param0_4[] = {-38,38,40,72};
int param0_5[] = {1,0,0,0,1};
int param0_6[] = {11,15,16,17,17,17,22,23,23,25,27,28,28,31,33,36,38,40,42,44,46,49,51,51,52,60,62,65,67,71,74,77,77,78,78,79,83,83,86,86,87,87,87,88,91,92,97,97,97};
int param0_7[] = {-26,-90,-78,-76,-58,-64,-72,-34,-58,-48,78,-50,-30,26,-60,26};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {56,51,63,30,10,88,23,1,48,4,28,44};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {22,9,1,23,2,3,44,9,23,10};
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