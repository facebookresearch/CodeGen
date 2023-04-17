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

int f_gold ( int set [ ], int n ) {
  if ( n <= 2 ) return n;
  int L [ n ] [ n ];
  int llap = 2;
  for ( int i = 0;
  i < n;
  i ++ ) L [ i ] [ n - 1 ] = 2;
  for ( int j = n - 2;
  j >= 1;
  j -- ) {
    int i = j - 1, k = j + 1;
    while ( i >= 0 && k <= n - 1 ) {
      if ( set [ i ] + set [ k ] < 2 * set [ j ] ) k ++;
      else if ( set [ i ] + set [ k ] > 2 * set [ j ] ) {
        L [ i ] [ j ] = 2, i --;
      }
      else {
        L [ i ] [ j ] = L [ j ] [ k ] + 1;
        llap = max ( llap, L [ i ] [ j ] );
        i --;
        k ++;
      }
    }
    while ( i >= 0 ) {
      L [ i ] [ j ] = 2;
      i --;
    }
  }
  return llap;
}


int f_filled ( int set [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {3,4,4,7,8,19,21,22,25,27,28,29,38,40,41,42,43,46,50,50,53,53,54,55,60,64,64,69,70,75,77,81,81,82,86,87,87,88,91,94,97};
int param0_1[] = {40,-6,50,-18,42,78,38,-90,-44,-42,-86,78,-68,2,-32,-20,-44,54,80,54,70,26,82,-14,-74,-20,74,82};
int param0_2[] = {0,0,0,0,1,1,1};
int param0_3[] = {76,80};
int param0_4[] = {-92,-90,-88,-76,-76,-60,-46,-40,-24,-8,-8,-6,2,12,36,38,58,76,80};
int param0_5[] = {1,1,1,0,0,0,0,1,1,1,0,0,0,1,0,1,1};
int param0_6[] = {5,8,11,27,27,32,32,37,50,51,55,61,62,68,73,83};
int param0_7[] = {52,-74,-32,-64,-52,-60,-70,36,70,40,40,-18,90,-70,-82,-64,-8,-6,36,4,-58,62,-96,78,36,90,-70,-6,-84,24,84,32,-90,36,70,-60,-56,78,48,34,-16,80,82,58,14,-6,-8,76};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {11,21,76,45,8,49,97,66,17,11,87,4,34,89,79,88,6,91,19,56,91,25,17,90,26,59,34,32,43,17,98,39,72,78,93,43};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {27,21,5,1,13,15,8,29,27,26};
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