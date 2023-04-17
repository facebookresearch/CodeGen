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

int f_gold ( int array [ ], int start, int end ) {
  if ( start > end ) return end + 1;
  if ( start != array [ start ] ) return start;
  int mid = ( start + end ) / 2;
  if ( array [ mid ] == mid ) return f_gold ( array, mid + 1, end );
  return f_gold ( array, start, mid );
}


int f_filled ( int array [ ], int start, int end ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {3,6,7,9,11,14,18,30,30,32,32,34,37,44,45,45,48,48,48,52,58,60,63,67,69,69,81,83,87,89,97,99};
int param0_1[] = {88,-62,16,80,66,78,88,38,52,-96,48,98,96,-62,18,34,-58,30,-10,26,-98,48,-96,4,92,36,36,-36,-32,-70,62,-58,-58,-84,86,-98};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {79,99,79,85,61,58,62,61,39,87,39,74,36,70,30,43,20,52,54,50,81,98,42};
int param0_4[] = {-98,-72,-46,-44,-42,-40,-16,-4,62,70,74};
int param0_5[] = {1,1,0,1,0,0,0,0,1,1,0,1,0,1,1,1,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0};
int param0_6[] = {58};
int param0_7[] = {4,-84,-42,12,-50,42,-36,-38,-36,98,-2,20,6,-96,-78,24,34,88,0,74,0,-8,-86,-68,-42,98,-26,86,-70,-32,-82,78,46,58,84,4,-60,-90,-52,-78};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {8};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {24,19,26,20,8,26,0,37,28,0};
    int param2[] = {18,26,28,20,10,23,0,31,28,0};
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