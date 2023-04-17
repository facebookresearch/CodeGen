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

int f_gold ( int arr [ ], int dep [ ], int n ) {
  sort ( arr, arr + n );
  sort ( dep, dep + n );
  int plat_needed = 1, result = 1;
  int i = 1, j = 0;
  while ( i < n && j < n ) {
    if ( arr [ i ] <= dep [ j ] ) {
      plat_needed ++;
      i ++;
      if ( plat_needed > result ) result = plat_needed;
    }
    else {
      plat_needed --;
      j ++;
    }
  }
  return result;
}


int f_filled ( int arr [ ], int dep [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {8,24,28,64,75,86,93,95};
int param0_1[] = {2,-30,-8,-78,58,-42,-94,84,-58,14,78,34,30,6,-18,-92,0,94,-54,58,0,-86,66,86,8,-26,50,16,-30,-68,98,-28,-4,-6};
int param0_2[] = {0,0,0,0,0,0,1};
int param0_3[] = {51,5,48,61,71,2,4,35,50,76,59,64,81,5,21,95};
int param0_4[] = {-64,-52,44,52,90};
int param0_5[] = {0,0,1,0,1,0,1,1,0,1,1,1,0,1,0,1,0,1,0,0,0,1,1,1,0,1,0,1,1,1};
int param0_6[] = {2,15,25,55,72,96,98};
int param0_7[] = {-60,30,-58,52,40,74,74,76,-72,-48,8,-56,-24,-40,-98,-76,-56,-20,30,-30,-34,4,-34};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {37,84,20,34,56,1,87,72};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {19,30,41,51,62,68,85,96};
int param1_1[] = {40,22,-24,80,-76,-4,-8,-34,96,-98,16,28,14,52,10,-10,-62,64,-48,10,-64,-90,-52,46,34,50,50,-84,68,-12,-44,28,-22,78};
int param1_2[] = {0,0,0,0,0,1,1};
int param1_3[] = {67,84,86,43,50,90,49,8,40,67,5,51,40,28,31,47};
int param1_4[] = {-62,-16,22,26,58};
int param1_5[] = {0,0,1,1,1,0,1,1,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0};
int param1_6[] = {3,6,11,19,26,37,39};
int param1_7[] = {-96,-40,-76,52,-20,-28,-64,-72,36,56,52,34,14,8,-50,6,-82,-98,-8,18,-76,-66,-22};
int param1_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_9[] = {68,62,84,54,15,29,70,96};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {6,18,6,8,3,17,6,20,22,6};
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