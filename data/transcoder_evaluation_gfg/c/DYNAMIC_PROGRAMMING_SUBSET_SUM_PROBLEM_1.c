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

bool f_gold ( int set [ ], int n, int sum ) {
  bool subset [ n + 1 ] [ sum + 1 ];
  for ( int i = 0;
  i <= n;
  i ++ ) subset [ i ] [ 0 ] = true;
  for ( int i = 1;
  i <= sum;
  i ++ ) subset [ 0 ] [ i ] = false;
  for ( int i = 1;
  i <= n;
  i ++ ) {
    for ( int j = 1;
    j <= sum;
    j ++ ) {
      if ( j < set [ i - 1 ] ) subset [ i ] [ j ] = subset [ i - 1 ] [ j ];
      if ( j >= set [ i - 1 ] ) subset [ i ] [ j ] = subset [ i - 1 ] [ j ] || subset [ i - 1 ] [ j - set [ i - 1 ] ];
    }
  }
  return subset [ n ] [ sum ];
}


bool f_filled ( int set [ ], int n, int sum ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {3,4,4,5,8,11,11,13,14,14,14,14,19,21,24,24,28,31,32,32,34,37,37,38,38,39,43,43,44,47,48,49,58,63,67,72,77,80,81,83,88,92,93,99};
int param0_1[] = {30,-64,6,-8,-8,-36,66,36,30,-14,32,-44,-42,42,-92};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {71,46,18,96,58,19,94,45,71,18,70,65,32,90,28,36,89,19,12,10,72,66,90,33,61,21,5,83,50,11,99,20,43,3,42,45,59,74,72,6,40,7,9};
int param0_4[] = {-96,-78,-72,-22,2,14,18,36,72,76,80};
int param0_5[] = {0,1,1,1,0,0,1,1,0,1,0,0,0,1,0,0,1,1,0,1,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,0,1,0,0};
int param0_6[] = {2,4,10,10,13,15,15,16,20,21,26,31,32,33,36,37,38,40,42,44,50,55,58,58,59,61,64,66,67,69,71,76,80,82,82,84,86,90,91,96,97,98};
int param0_7[] = {80,-94,96,44,58,-36,78,-88,64,86,-52,86,-66,98,90,0,-98,-38,-70,40,-52,34,-96,32,28,-16,82,-78,4,-72,-22,-78,56,78,48,18,26,-94,32,64,14,58};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {82,86,4,32,78,63,59,89,44,24,19,82,98,89,80,31};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {37,11,24,38,6,20,33,25,28,15};
    int param2[] = {29,8,19,28,8,34,36,27,31,10};
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