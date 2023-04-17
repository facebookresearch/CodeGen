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
  unordered_map < int, int > inc, dcr;
  int len_inc [ n ], len_dcr [ n ];
  int longLen = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    int len = 0;
    if ( inc . find ( arr [ i ] - 1 ) != inc . end ( ) ) len = inc [ arr [ i ] - 1 ];
    inc [ arr [ i ] ] = len_inc [ i ] = len + 1;
  }
  for ( int i = n - 1;
  i >= 0;
  i -- ) {
    int len = 0;
    if ( dcr . find ( arr [ i ] - 1 ) != dcr . end ( ) ) len = dcr [ arr [ i ] - 1 ];
    dcr [ arr [ i ] ] = len_dcr [ i ] = len + 1;
  }
  for ( int i = 0;
  i < n;
  i ++ ) if ( longLen < ( len_inc [ i ] + len_dcr [ i ] - 1 ) ) longLen = len_inc [ i ] + len_dcr [ i ] - 1;
  return longLen;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {78};
int param0_1[] = {-6,-18,-48,58,-54,76,80,-56,86,58,-86,-86,-88,32,12,58,58,-16,86,-24,84,86,36,18,30,-32,-4,-36,-72,-4,42,94};
int param0_2[] = {0,1};
int param0_3[] = {92,26,72,8,66,28,34,61,28};
int param0_4[] = {-86,-82,-76,-68,-66,-64,-62,-56,-48,-42,-38,-30,-22,-18,-10,-10,-4,-2,4,28,42,44,50,50,56,58,60,76,82,86,86,98};
int param0_5[] = {0,0,1,0,1,1,0,0,1,0,1,1,0,1,1,1,0,0,0,0,1,0};
int param0_6[] = {3,4,8,9,12,13,16,19,23,25,29,31,34,36,38,41,42,47,49,50,51,51,58,63,66,70,73,74,75,75,75,76,76,80,82,83,83,84,86,89,90,91,91,95,96};
int param0_7[] = {4,-76,60,48,-14,72};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {66,80,79,72,1,67,20,67,32,40,22,64,58,67,10,21,37,49};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {0,18,1,5,25,17,44,3,17,15};
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