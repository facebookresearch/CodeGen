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

int f_gold ( int arr [ ], int l, int r, int x ) {
  if ( r >= l ) {
    int mid = l + ( r - l ) / 2;
    if ( arr [ mid ] == x ) return mid;
    if ( mid > l && arr [ mid - 1 ] == x ) return ( mid - 1 );
    if ( mid < r && arr [ mid + 1 ] == x ) return ( mid + 1 );
    if ( arr [ mid ] > x ) return f_gold ( arr, l, mid - 2, x );
    return f_gold ( arr, mid + 2, r, x );
  }
  return - 1;
}


int f_filled ( int arr [ ], int l, int r, int x ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {75,91,93};
int param0_1[] = {-92,-96,-68,-40,70};
int param0_2[] = {-92,-86,-68,-40,70};
int param0_3[] = {-3,-1,0,30,10,45,70,60};
int param0_4[] = {-3,-1,0,10,5,45,60,50};
int param0_5[] = {-3,-1,0,10,30,45,60,70};
int param0_6[] = {0,0,1};
int param0_7[] = {1,1,1};
int param0_8[] = {30,2,30,45};
int *param0[9] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8};
    int param1[] = {0,0,0,0,0,0,0,0,0,0};
    int param2[] = {15,15,4,4,7,7,7,2,2,3};
    int param3[] = {71,71,-96,20,0,12,18,20,17,28};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i]) == f_gold(param0[i],param1[i],param2[i],param3[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}