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

int f_gold ( int arr [ ], int low, int high ) {
  if ( high >= low ) {
    int mid = ( low + high ) / 2;
    if ( mid == arr [ mid ] ) return mid;
    if ( mid > arr [ mid ] ) return f_gold ( arr, ( mid + 1 ), high );
    else return f_gold ( arr, low, ( mid - 1 ) );
  }
  return - 1;
}


int f_filled ( int arr [ ], int low, int high ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {9};
int param0_1[] = {1,1,0,1,1,0,1,0,0};
int param0_2[] = {1,4,16,16,19,28,34,34,35,36,37,46,49,52,54,60,60,60,63,70,75,77,80,81,81,84,85,87,93,99};
int param0_3[] = {30,30,-94,-10,2,58};
int param0_4[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_5[] = {72,38,91,63,30,67,39,29,96,42};
int *param0[6] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5};
    int param1[] = {0,0,0,1,2,0,0,0,0,0};
    int param2[] = {16,4,4,5,5,7,5,5,12,7};
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