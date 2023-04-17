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

bool f_gold ( int arr [ ], int n, int x ) {
  if ( n < 2 ) return false;
  unordered_set < int > s;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( arr [ i ] == 0 ) {
      if ( x == 0 ) return true;
      else continue;
    }
    if ( x % arr [ i ] == 0 ) {
      if ( s . find ( x / arr [ i ] ) != s . end ( ) ) return true;
      s . insert ( arr [ i ] );
    }
  }
  return false;
}


bool f_filled ( int arr [ ], int n, int x ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,2,3,7,23,23,25,27,37,42,53,56,58,61,69,78,79,84,85,86,90,93,95};
int param0_1[] = {-10,-18,88,-36,78,66,-70,-34,-88,-98,-70,-4,-94,-92,-76,-78,-30,-48,-72,86,-64,38,-80,20,70,-32,-90,74,-78,12,-54,88,38,-96,28};
int param0_2[] = {0,0,0,0,0,0,0,0,1,1};
int param0_3[] = {83,61,55,89,16,78,44,54,22,49,58,62,53,99,35,83,29,19,96,39,60,6,34,67,43,29,46,3,81,78,80,39,86,78,21};
int param0_4[] = {-96,-88,-80,-62,-58,-56,-54,-52,-34,-20,-6,-2,6,20,52,54,70,72,80,82,94};
int param0_5[] = {0,1,1,0,0,1,1,1};
int param0_6[] = {8,11,11,20,22,23,26,27,31,38,40,40,45,46,46,48,50,61,73,76,78,78,79,80,81,84,90,91,93,95};
int param0_7[] = {18};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {19,37,47,40,72,59,51,53,92,3,21,81,29,48,97,59,10,74,11,37,49,95,88,85,6,26,76,33};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {15,17,9,23,18,4,24,0,37,22};
    int param2[] = {17,22,5,27,12,6,28,0,39,21};
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