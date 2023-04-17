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

int f_gold ( int arr [ ], int n, int x ) {
  int i = 0;
  while ( i < n ) {
    if ( arr [ i ] == x ) return i;
    i = i + abs ( arr [ i ] - x );
  }
  printf("number is not present!");
  return - 1;
}


int f_filled ( int arr [ ], int n, int x ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4};
int param0_1[] = {97,35,60,96,3,67,72,95,55,9,69,28,15,91,31,59};
int param0_2[] = {-84,-78,-74,-70,-68,-60,-56,-54,-48,-46,-28,-16,-6,0,0,8,8,8,12,16,26,30,32,34,36,40,46,48,70,70,72,76,78,78,80,84,84,86};
int param0_3[] = {1,0,1,1,1,1,0,1,1,1,1};
int param0_4[] = {55,64,76,79,93,96};
int param0_5[] = {66,-90,98,-50,0,46,42,64,-96,-80,-96,20,-10,-84};
int param0_6[] = {0,0,0,0,0,0,1};
int param0_7[] = {94,4,34,87,32,3,92,68,57,76,24,33,3,4,30,70,49,30,72,82,16,53,6,24,92,96,89,28,21,8,36,9,40,85,51,1,63,68,74,26,40,3,9,32,67,4,6,73};
int *param0[8] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7};
    int param1[] = {12,1,6,15,22,5,4,8,6,25};
    int param2[] = {3,1,5,9,31,7,4,13,5,25};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i]) == f_gold(param0[i],param1[i],param2[i]))
        {
            n_success+=1;
        }
    }
    printf("number is not present!");
    return 0;
}