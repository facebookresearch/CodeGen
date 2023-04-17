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
  unordered_map < int, int > mp;
  for ( int i = 0;
  i < n;
  i ++ ) mp [ arr [ i ] ] ++;
  for ( int i = 0;
  i < n;
  i ++ ) if ( mp [ arr [ i ] ] == 1 ) return arr [ i ];
  return - 1;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {6,7,14,18,18,18,21,25,28,38,40,42,42,45,48,50,50,50,53,54,58,59,62,65,65,66,67,68,69,73,74,76,77,83,84,85,87};
int param0_1[] = {24,-84,86,-50,60,-36,92,70,84,40,-8,74,-24,-38,98,40,-78,-36,38,-22,-98,82,-22,80,-80,-62,16,-46,18,64,16,2,24,-92,-46,42,38,8,72,8,14,-68,18,16,-82,8,58,-2};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1};
int param0_3[] = {59,77,13,49,90};
int param0_4[] = {-80,-76,-66,-60,-44,-42,-38,-36,-32,-30,-24,-18,-6,2,4,14,32,42,54,70,92,98};
int param0_5[] = {0,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1,1,1,0,1,0,1,0,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0};
int param0_6[] = {6,22,24,27,29,30,35,42,57,59,59,63,71,73,76,98};
int param0_7[] = {-82,-48,36};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {88,49,13,64,30,60,26,55,55,97,98,69,72,72,79,59,46,87,76,61,87,12,91,8,34,15,93,64,83,33,69,58,32,14,72,67,25,7,55,21,12,78,63};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {33,25,16,2,12,33,13,1,35,24};
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