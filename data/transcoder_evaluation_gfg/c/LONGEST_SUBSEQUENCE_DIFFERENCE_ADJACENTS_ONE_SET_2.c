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
  unordered_map < int, int > um;
  int longLen = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    int len = 0;
    if ( um . find ( arr [ i ] - 1 ) != um . end ( ) && len < um [ arr [ i ] - 1 ] ) len = um [ arr [ i ] - 1 ];
    if ( um . find ( arr [ i ] + 1 ) != um . end ( ) && len < um [ arr [ i ] + 1 ] ) len = um [ arr [ i ] + 1 ];
    um [ arr [ i ] ] = len + 1;
    if ( longLen < um [ arr [ i ] ] ) longLen = um [ arr [ i ] ];
  }
  return longLen;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {20,48,58};
int param0_1[] = {-36,94,-20,-90,-80,88,46,-8,-36,22,70,-16,-48,-54,-82,38,10,-84,12,10,-14,50,12,-28,-64,-38,-84,-62,-56,32,-78,34,-34,48};
int param0_2[] = {0,0,0};
int param0_3[] = {50,28,14,52,92,30,30,27,66,77,39,42,28,84,63,55,18,34,57,45,81,38,23,31,9,35,25,39,30,5,28,7,42,42};
int param0_4[] = {-96,-70,-64,-60,-56,-44,-40,-32,-30,-22,-10,14,26,28,28,38,58,78,80};
int param0_5[] = {1,0,0,0,1,0,0,1,0,1};
int param0_6[] = {8,19,30,37,44,46,49,50,51,57,65,67,70,70,76,83,91,92};
int param0_7[] = {40,62,-6,88,58,66,-40,46,-32,80,22,-30,32,-74,20,-82,-58,-18,30,68,-2,38,-76,-58,22,-22,74};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1};
int param0_9[] = {46,6,71,56,21,97,80,67,26,25,79,86,64,84,53,50,29,19,95,58,14,15,63,1,76,64,11,47,9,97,54,27};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {2,29,1,22,11,8,13,20,12,17};
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