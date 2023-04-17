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

int f_gold ( int S [ ], int n ) {
  bool found = false;
  sort ( S, S + n );
  for ( int i = n - 1;
  i >= 0;
  i -- ) {
    for ( int j = 0;
    j < n;
    j ++ ) {
      if ( i == j ) continue;
      for ( int k = j + 1;
      k < n;
      k ++ ) {
        if ( i == k ) continue;
        for ( int l = k + 1;
        l < n;
        l ++ ) {
          if ( i == l ) continue;
          if ( S [ i ] == S [ j ] + S [ k ] + S [ l ] ) {
            found = true;
            return S [ i ];
          }
        }
      }
    }
  }
  if ( found == false ) return INT_MIN;
}


int f_filled ( int S [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {8,12,14,15,16,20,27,28,29,30,35,41,46,51,53,55,55,58,63,64,72,73,75,75,75,82,82,86,89,91,92,94,95,95,97,97,98};
int param0_1[] = {-62,48,-22,-44,-58,-50,-82,34,26,-2,86,-44,92,-96,42,-20,10,74,-56,-12,-28,-40};
int param0_2[] = {0,0,0,0,0,0,0,1,1,1};
int param0_3[] = {84,58,10,67,77,66,10,47,65,55,54};
int param0_4[] = {-46,-28,-20,-18,4,8,18,38,90,90};
int param0_5[] = {0,1,1,1,0,1,1,0,0,1,1,0,0,0,0,1,1,1,1,0,0,1,0,0,0,0,1,0,1,0,0,1,1,0,1,1,0,0,1,0,0,1,0,1,0};
int param0_6[] = {11,13,14,21,26,28,36,39,41,42,43,44,49,49,57,58,59,59,63,64,67,69,70,75,78,79,83,83,86,91,92,93,96,96,96,97};
int param0_7[] = {74,52,-16,34,-88,62,54,46,-82,76,-48,54,50,-66,-18,78,-48,38,96,-32,-82,0,-76,46,-56,4,-30,-70,-62};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {55,74,18,4,68,66,33,61,66,92,21,9,49,14,99,87,74,6,11,25,5,58,56,20};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {24,19,8,5,6,35,30,16,17,23};
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