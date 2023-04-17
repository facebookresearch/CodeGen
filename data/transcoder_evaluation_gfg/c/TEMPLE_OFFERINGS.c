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

int f_gold ( int n, int templeHeight [ ] ) {
  int sum = 0;
  for ( int i = 0;
  i < n;
  ++ i ) {
    int left = 0, right = 0;
    for ( int j = i - 1;
    j >= 0;
    -- j ) {
      if ( templeHeight [ j ] < templeHeight [ j + 1 ] ) ++ left;
      else break;
    }
    for ( int j = i + 1;
    j < n;
    ++ j ) {
      if ( templeHeight [ j ] < templeHeight [ j - 1 ] ) ++ right;
      else break;
    }
    sum += max ( right, left ) + 1;
  }
  return sum;
}


int f_filled ( int n, int templeHeight [ ] ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {12,46,16,9,0,38,28,9,18,29};
    int param1_0[] = {3,11,12,15,16,21,24,29,32,39,42,44,51,68,79,81,81,85,92,94};
int param1_1[] = {76,48,88,70,-64,66,-6,-58,26,-28,-42,-94,80,-4,-56,-46,4,90,-12,-78,64,18,-38,26,56,-24,66,-18,-12,0,-94,12,-10,4,-68,-20,88,2,-58,16,46,-80,-42,44,-86,96,-44};
int param1_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_3[] = {2,95,20,50,2,58,20,14,65,69,78,7};
int param1_4[] = {-88};
int param1_5[] = {0,0,0,0,1,0,1,0,0,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,0,0,0,0,1,0,1,1,0,0,0,1,1,1,0,0};
int param1_6[] = {2,3,6,8,9,10,14,17,17,22,25,27,29,29,30,32,33,35,38,42,50,51,51,57,59,59,59,60,62,62,63,67,70,75,76,77,81,81,83,84};
int param1_7[] = {-52,62,74,-62,-58,62,38,42,-50,20};
int param1_8[] = {0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1};
int param1_9[] = {96,15,9,9,40,34,17,4,51,49,34,66,97,28,64,65,92,56,74,48,43,17,82,8,21,39,83,35,42,37,64,34,42,59,45,61,55,93,94,29,20,96,77,66};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
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