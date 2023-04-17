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

int f_gold ( int arr [ ], int n, int k ) {
  unordered_map < int, int > count_map;
  for ( int i = 0;
  i < n;
  i ++ ) count_map [ arr [ i ] ] ++;
  for ( int i = 0;
  i < n;
  i ++ ) if ( count_map [ arr [ i ] ] == k ) return arr [ i ];
  return - 1;
}


int f_filled ( int arr [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,3,4,4,7,18,20,23,27,30,31,31,32,35,36,43,45,46,49,50,53,55,59,60,64,64,65,68,78,80,80,85,95};
int param0_1[] = {-26,32,36,6,64,24,-28,96};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {38,40,43,70,20,40,95,96,81,82};
int param0_4[] = {-68,-8,-8,16,24,54};
int param0_5[] = {1,0,1,0,0,0,1,0,1,0,0,0,1};
int param0_6[] = {13,18,19,28,31,34,49,49,53,57,58,62,75,76,77,78,80,84,84,85,87,91,98,99};
int param0_7[] = {-4,24,-86,-84,30,-16,12,-92,-68,22};
int param0_8[] = {0,0,0,0,0,0,0,0,0,1,1,1,1};
int param0_9[] = {55,44,75,97,25,65,76,53,20,78,25,59,61,29,81,35,15,78,41,44,31,33,39,93,26,67};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {30,6,15,9,3,6,20,6,8,23};
    int param2[] = {2,3,7,1,2,4,2,5,10,20};
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