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

bool f_gold ( int arr [ ], int n, int k ) {
  int count;
  for ( int i = 0;
  i < n;
  i ++ ) {
    count = 0;
    for ( int j = 0;
    j < n;
    j ++ ) {
      if ( arr [ j ] == arr [ i ] ) count ++;
      if ( count > 2 * k ) return false;
    }
  }
  return true;
}


bool f_filled ( int arr [ ], int n, int k ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,1,2,3,1};
int param0_1[] = {2,3,3,5,3,3};
int param0_2[] = {0,0,1,1,1};
int param0_3[] = {7,60,78,91,80,75,85,21,41,63,1,84,69,13,94,25,54,54,52,68,53,35,17,37,98,27,2,31};
int param0_4[] = {-96,-94,-82,-80,-78,-66,-36,-24,-18,-12,-2,-2,6,8,10,12,36,38,42,58,64,68,82,84,86,88,94};
int param0_5[] = {0,1,1,1,0,0,0,0,1,0,0,0,1,0,0,1,1,1,1,1,1,0,0,0,0,1,0,1,1,0,0,0,0,1,1,0,0,0,1,0,0,1,1,1,0};
int param0_6[] = {16,19,25,25,32,37,48,59,60,60,71,74,77,81,91,94};
int param0_7[] = {-62,-94,72,-22,86,-80,64,98,-82,-50,12,-4,56,46,-80,2,-86,-44,-26,68,-94,-82,74,26,94,40,50,-40,-42,-10};
int param0_8[] = {0,0,0,0,0,1,1,1};
int param0_9[] = {83,57,2,47,70,22,49,51,25,57,32,7,8,99,6,86,24,79,42,43,1,24,68,11,24,12,43,40,14,45,11,46,12,80,66};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {5,6,2,24,24,34,10,20,5,21};
    int param2[] = {2,2,1,2,3,2,8,4,2,33};
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