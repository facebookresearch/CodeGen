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
  int high = 0;
  for ( int i = 0;
  i < n;
  i ++ ) high = max ( high, arr [ i ] );
  int count [ high + 1 ] = {
    0 };
    for ( int i = 0;
    i < n;
    i ++ ) count [ arr [ i ] ] ++;
    int counter = 0;
    for ( int i = high;
    i >= 1;
    i -- ) {
      int j = i;
      counter = 0;
      while ( j <= high ) {
        if ( count [ j ] >= 2 ) return j;
        else if ( count [ j ] == 1 ) counter ++;
        j += i;
        if ( counter == 2 ) return i;
      }
    }
  }
  

int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {7,9,9,13,14,26,37,40,44,44,46,46,48,49,52,52,57,58,64,66,71,72,76,76,78,80,85,88,90,90,93,93,97,98};
int param0_1[] = {-56,94,84,14,-6,84,84,-14,-60,-50,38,-20,66,-16};
int param0_2[] = {0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_3[] = {36,38,30,23,73,29,70,35,49,77,98,86};
int param0_4[] = {-88,-88,-70,-70,-68,-68,-68,-64,-58,-50,-42,-36,-34,-32,-32,-30,-28,-24,-18,-8,0,0,10,10,14,14,28,30,32,32,40,40,48,54,56,60,62,72,76,78,86,88,98,98};
int param0_5[] = {0,1,0,1,0,1,0,0};
int param0_6[] = {3,5,5,10,13,25,27,32,35,36,36,38,40,45,53,53,58,59,68,79,79,79,87,98};
int param0_7[] = {28,2,-10,70,50,6,32,-6,48,-28,18,86,-96,64,-92,14,44,-36,-32,92,6,36,76,-68,-22,34,-48,-54,28,-90,34};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_9[] = {86,82,57,48,75,17,60,3,91,51};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {29,8,13,7,34,6,12,17,16,8};
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