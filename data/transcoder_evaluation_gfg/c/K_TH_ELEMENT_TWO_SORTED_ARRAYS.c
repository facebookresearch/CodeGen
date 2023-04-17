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

int f_gold ( int arr1 [ ], int arr2 [ ], int m, int n, int k ) {
  int sorted1 [ m + n ];
  int i = 0, j = 0, d = 0;
  while ( i < m && j < n ) {
    if ( arr1 [ i ] < arr2 [ j ] ) sorted1 [ d ++ ] = arr1 [ i ++ ];
    else sorted1 [ d ++ ] = arr2 [ j ++ ];
  }
  while ( i < m ) sorted1 [ d ++ ] = arr1 [ i ++ ];
  while ( j < n ) sorted1 [ d ++ ] = arr2 [ j ++ ];
  return sorted1 [ k - 1 ];
}


int f_filled ( int arr1 [ ], int arr2 [ ], int m, int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,2,4,4,9,10,14,16,16,19,20,21,25,26,29,36,36,37,38,44,44,49,53,54,56,61,62,64,72,72,73,77,80,84,84,87,93,94};
int param0_1[] = {2,4,-90,62,22,-94,-74,-22,44,-94,20,-40,20,0,32,24,78,8,4,98,-74,-60};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {85,44,62,2,71,88,60,78,32,46,17,47,65,78,65,94};
int param0_4[] = {-94,-84,-82,-70,-70,-60,-54,-54,-52,-52,-46,-40,-40,-36,-34,-32,-30,-22,-18,-16,-10,-4,8,12,18,22,32,38,38,44,50,56,64,82,84,86,88};
int param0_5[] = {0,0,0,1,1,0,0,0,0,1,1,1,0,0,1,1,1,0,1,1,1,1,0,1,1,1};
int param0_6[] = {53,96,99};
int param0_7[] = {98,86,36,-68,86,22,52,-20,-2,74,-72,86,80,-78,14,62,10,94,-66,78,28,92,-8,46,-24,66};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {6,21,86,58,48,27,18,73,16,79,51,33,63,26,37,88,48,58,44,32,58,23,31};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {6,8,10,10,12,14,24,31,33,33,35,35,35,41,46,47,49,51,52,56,57,59,62,65,72,72,73,73,79,80,82,83,83,84,87,87,93,99};
int param1_1[] = {58,74,-46,38,-58,-78,-32,-84,84,-54,84,-34,-26,88,74,48,26,-92,68,-86,74,88};
int param1_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_3[] = {18,3,15,9,61,73,3,62,87,1,54,97,61,37,23,65};
int param1_4[] = {-92,-68,-64,-62,-54,-52,-52,-34,-24,-22,-20,-12,-12,-10,6,10,14,22,22,24,24,30,30,36,36,48,50,56,58,64,68,80,84,88,88,92,94};
int param1_5[] = {1,0,0,0,1,0,0,0,1,1,0,1,0,1,1,1,0,1,0,1,1,0,0,0,1,0};
int param1_6[] = {30,55,56};
int param1_7[] = {72,-72,-90,24,-22,60,78,-68,98,26,-30,-20,44,-96,8,90,0,98,-24,-68,-32,-62,0,-60,26,-98};
int param1_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_9[] = {87,77,44,15,70,89,36,79,82,3,18,76,37,79,85,97,19,53,17,74,87,58,49};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {27,18,30,11,19,24,1,22,42,14};
    int param3[] = {21,11,31,11,26,17,1,19,40,22};
    int param4[] = {23,12,42,13,28,23,1,24,42,19};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i],param4[i]) == f_gold(param0[i],param1[i],param2[i],param3[i],param4[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}