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

int f_gold ( int arr [ ], int n, int x, int k ) {
  int i = 0;
  while ( i < n ) {
    if ( arr [ i ] == x ) return i;
    i = i + max ( 1, abs ( arr [ i ] - x ) / k );
  }
  printf("number is not present!");
  return - 1;
}


int f_filled ( int arr [ ], int n, int x, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,5,9,11,14,18,19,21,26,32,38,38,43,47,49,52,55,61,65,67,69,73,74,79,84,90,91,91,92,93,94,99};
int param0_1[] = {12,-86,-66,-50,-48,78,-92,-56,-2,66,64};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {10,87,39,87,45,33,5,37,70,69,88,78,90,3};
int param0_4[] = {-78,-70,-68,-60,-52,-34,-24,-4,12,18,58,58,64,76,84,94};
int param0_5[] = {0,1,0,1,1,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,1,0,0,1,1,1,0,1,0,1,0,0,1,1,0,0,1,0,1,0,1,0};
int param0_6[] = {5,5,7,11,11,15,22,23,28,38,41,53,54,57,59,68,71,89};
int param0_7[] = {-4,0,60,-14,-48,54,-96,-68,-40,64,-50,-74,-20,-22,48,-48,42,62,66,84,54,-52,-52,6,46,-90,-18,90};
int param0_8[] = {0,0,0,0,0,0,0,1,1,1,1,1};
int param0_9[] = {30,91,34,44,3,76,43,75,49,33,74,72,68,79,26,62,23,5,32,75,82,25,7,19,32,87,87,94,34,62,3,32,59};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {22,5,35,9,14,26,16,18,9,32};
    int param2[] = {19,10,37,8,9,36,17,14,8,30};
    int param3[] = {26,5,43,10,13,32,16,23,9,24};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i]) == f_gold(param0[i],param1[i],param2[i],param3[i]))
        {
            n_success+=1;
        }
    }
    printf("number is not present!");
    return 0;
}