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

bool f_gold ( int arr [ ], int n, int sum ) {
  bool subset [ 2 ] [ sum + 1 ];
  for ( int i = 0;
  i <= n;
  i ++ ) {
    for ( int j = 0;
    j <= sum;
    j ++ ) {
      if ( j == 0 ) subset [ i % 2 ] [ j ] = true;
      else if ( i == 0 ) subset [ i % 2 ] [ j ] = false;
      else if ( arr [ i - 1 ] <= j ) subset [ i % 2 ] [ j ] = subset [ ( i + 1 ) % 2 ] [ j - arr [ i - 1 ] ] || subset [ ( i + 1 ) % 2 ] [ j ];
      else subset [ i % 2 ] [ j ] = subset [ ( i + 1 ) % 2 ] [ j ];
    }
  }
  return subset [ n % 2 ] [ sum ];
}


bool f_filled ( int arr [ ], int n, int sum ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,6,7,9,11,23,25,33,55,81,82,90,93,98};
int param0_1[] = {-44,-96,48,90,-26,66,-82,16,80,96,64,64,-78,-8,20,-74,-32,62,88,-62,28,-46,-40,-62,18,-46,50,-32,-26,-68,66,20,6,34,-20,-96,-26,-76,-64,46,-38};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {78,36,15,81,56,57,73,78,88,11,93,89,68,96,32,67,6,19,17,48,64,5,74,91,36,96,57,85,96,43,98,79,73,2};
int param0_4[] = {-84,-60,-56,-32,70,82};
int param0_5[] = {0,1,0,0,1,1,1,0,1};
int param0_6[] = {42,57,77,85,87,89,90};
int param0_7[] = {-82,68,70,-18,44,-48,-24,82,8,74,90,-72,-66,24,44,24,26,-80,-70,16,90,-54,-32,-54,70,48,-56,-16,-42};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {3,30,94,96,95,21,84,76,35,52,18,87,60,28,78,72,80,58,65,5};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {10,36,29,23,4,8,3,14,23,16};
    int param2[] = {7,40,39,29,4,5,6,14,24,14};
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