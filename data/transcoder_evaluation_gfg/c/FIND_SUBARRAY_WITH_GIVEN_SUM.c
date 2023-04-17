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

int f_gold ( int arr [ ], int n, int sum ) {
  int curr_sum, i, j;
  for ( i = 0;
  i < n;
  i ++ ) {
    curr_sum = arr [ i ];
    for ( j = i + 1;
    j <= n;
    j ++ ) {
      if ( curr_sum == sum ) {
        printf("Sum found between indexes ", i, " and ", j - 1);
        return 1;
      }
      if ( curr_sum > sum || j == n ) break;
      curr_sum = curr_sum + arr [ j ];
    }
  }
  printf("Sum found between indexes ", i, " and ", j - 1);
  return 0;
}


int f_filled ( int arr [ ], int n, int sum ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,8,8,10,15,18,19,22,25,26,30,32,35,36,40,41,43,48,53,57,59,63,64,68,71,76,76,77,78,89,96,97};
int param0_1[] = {-78,16,-16,-10,-2,-38,58,-72,-78,50,-68,-16,-96,82,70,2,-20};
int param0_2[] = {0,0,0,0,0,0,0,0,1,1,1,1,1,1};
int param0_3[] = {16,10,55,43,46,74,57,65,86,60,28,6,92};
int param0_4[] = {-98,-98,-90,-84,-84,-80,-76,-76,-70,-54,-48,-46,-44,-42,-38,-14,-12,-4,6,8,24,28,32,40,40,42,64,84,98};
int param0_5[] = {0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1};
int param0_6[] = {2,10,40,45,56,66,66,70,75,83,93,98};
int param0_7[] = {-20,30,56,-68,54,-6,78,-86,88,-66,76,-66,62,78,22,46,-94,-10,18,16,-36,34,-98,-84,-40,98,82,10,12,54,-88};
int param0_8[] = {0,0,1,1};
int param0_9[] = {38,24,12};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {26,9,9,10,23,12,10,30,2,1};
    int param2[] = {23,12,11,6,19,8,10,17,2,1};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i]) == f_gold(param0[i],param1[i],param2[i]))
        {
            n_success+=1;
        }
    }
    printf("Sum found between indexes ", i, " and ", j - 1);
    return 0;
}