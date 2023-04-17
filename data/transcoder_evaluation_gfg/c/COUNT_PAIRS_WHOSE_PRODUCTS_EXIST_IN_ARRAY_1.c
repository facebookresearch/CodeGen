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
  int result = 0;
  set < int > Hash;
  for ( int i = 0;
  i < n;
  i ++ ) Hash . insert ( arr [ i ] );
  for ( int i = 0;
  i < n;
  i ++ ) {
    for ( int j = i + 1;
    j < n;
    j ++ ) {
      int product = arr [ i ] * arr [ j ];
      if ( Hash . find ( product ) != Hash . end ( ) ) result ++;
    }
  }
  return result;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {7,10,17,17,18,20,27,28,29,29,31,32,41,43,45,46,63,66,69,69,70,75,87,95};
int param0_1[] = {-60};
int param0_2[] = {0,0,0,0,0,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {52,83,36,57,93,11,32,91,52};
int param0_4[] = {-98,-94,-90,-88,-76,-76,-64,-62,-60,-50,-46,-32,-24,-22,-20,-16,-4,-2,6,10,20,28,30,32,34,38,40,42,54,64,72,76,82,82,86,92,92,98,98};
int param0_5[] = {0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1,1,0,1,0,1,1,1,0,1,0,0,0,1,0,0,0,1,0,1,1,1,0,1,1,0};
int param0_6[] = {2,3,10,12,15,23,26,28,29,30,31,31,33,33,35,41,45,48,50,50,53,53,56,65,66,67,68,68,72,72,75,76,79,82,90,94,94,95,97,99};
int param0_7[] = {14,36,-54,-54};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,1,1,1,1,1};
int param0_9[] = {5,69,37,80,21,98,70,70,74,95,6,67,44,55,52,89,84,99,65,52};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {17,0,9,8,22,42,35,3,12,12};
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