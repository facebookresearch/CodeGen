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
  int invcount = 0;
  for ( int i = 0;
  i < n - 2;
  i ++ ) {
    for ( int j = i + 1;
    j < n - 1;
    j ++ ) {
      if ( arr [ i ] > arr [ j ] ) {
        for ( int k = j + 1;
        k < n;
        k ++ ) {
          if ( arr [ j ] > arr [ k ] ) invcount ++;
        }
      }
    }
  }
  return invcount;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {11,17,27,29,31,31,32,44,45,93};
int param0_1[] = {-48,-10,-44,-94,50,-24,30,72,-6,56,94,-44,-96,-52,-2,68,-52,30,98,0,12,-98,-94,48,-96,-86};
int param0_2[] = {0,0,0,1,1,1,1,1,1};
int param0_3[] = {78,82,51,92,88,95};
int param0_4[] = {-98,-96,-84,-72,-70,-62,-62,-58,-56,-54,-52,-52,-52,-50,-40,-40,-38,-36,-34,-26,-26,-22,-22,-20,-12,-8,-2,4,14,14,18,22,28,32,34,34,42,44,54,58,60,64,74,80,88,90,92,94,96};
int param0_5[] = {1,0,0,0};
int param0_6[] = {2,3,5,5,5,7,7,15,16,21,29,29,35,39,39,40,42,44,46,48,48,52,52,52,54,55,57,62,67,67,67,70,71,71,76,78,79,87,94,96};
int param0_7[] = {-60,-42,20,52,-54,40,56};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {98,81,23,71,82,31,15,21,4,68,68,22,77,83,22,9,10,56};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {5,15,6,3,47,3,39,6,37,13};
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