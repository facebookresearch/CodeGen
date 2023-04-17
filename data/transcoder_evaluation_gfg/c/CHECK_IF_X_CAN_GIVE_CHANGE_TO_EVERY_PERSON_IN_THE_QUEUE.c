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

int f_gold ( int notes [ ], int n ) {
  int fiveCount = 0;
  int tenCount = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    if ( notes [ i ] == 5 ) fiveCount ++;
    else if ( notes [ i ] == 10 ) {
      if ( fiveCount > 0 ) {
        fiveCount --;
        tenCount ++;
      }
      else return 0;
    }
    else {
      if ( fiveCount > 0 && tenCount > 0 ) {
        fiveCount --;
        tenCount --;
      }
      else if ( fiveCount >= 3 ) {
        fiveCount -= 3;
      }
      else return 0;
    }
  }
  return 1;
}


int f_filled ( int notes [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {20};
int param0_1[] = {5,5,5,20,10};
int param0_2[] = {5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,10,10,10,10,10,10,10,10,10,10,10,10,10};
int param0_3[] = {10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,18};
int param0_4[] = {5,5,20};
int param0_5[] = {10,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5};
int param0_6[] = {5,10,20,5,5,5,5,5,5,5,5,5,5,5,5};
int param0_7[] = {-82,-10,-78,-84,68,62,10,20,-86,-98,92,70,40,-12,-20,-36,8,-70,6,8,44,-24,8,-18,76,-54,-14,-94,-68,-62,-24,-36,-74,92,92,-80,48,56,94};
int param0_8[] = {10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5};
int param0_9[] = {46,46,93,57,82,34,83,80,77,36,80,85,69,28,9,56,49,27,83,25,1,80,99,14,69,82,79,71,74,34};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {4,5,27,12,2,17,7,31,25,20};
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