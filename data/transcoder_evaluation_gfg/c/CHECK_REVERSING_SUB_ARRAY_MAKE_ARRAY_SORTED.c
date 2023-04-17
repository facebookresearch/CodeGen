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

bool f_gold ( int arr [ ], int n ) {
  int temp [ n ];
  for ( int i = 0;
  i < n;
  i ++ ) temp [ i ] = arr [ i ];
  sort ( temp, temp + n );
  int front;
  for ( front = 0;
  front < n;
  front ++ ) if ( temp [ front ] != arr [ front ] ) break;
  int back;
  for ( back = n - 1;
  back >= 0;
  back -- ) if ( temp [ back ] != arr [ back ] ) break;
  if ( front >= back ) return true;
  do {
    front ++;
    if ( arr [ front - 1 ] < arr [ front ] ) return false;
  }
  while ( front != back );
  return true;
}


bool f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {5,9,9,16,17,22,32,40,45,53,57,58,66,69,76,80,91,93,94};
int param0_1[] = {52,-76,-18,86,56};
int param0_2[] = {0,0,1};
int param0_3[] = {66,44,98,44};
int param0_4[] = {-96,-62,-56,-46,-44,-38,-38,-26,-22,-22,-16,-12,-6,12,22,34,36,44,44,68,70,74,94};
int param0_5[] = {1,1,0,0,1,1,1,1,0,1,1,1,0,0,1,1,1,0,0,1,0,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,0,0,1,1};
int param0_6[] = {5,9,11,12,13,16,19,23,23,23,25,27,27,28,31,36,40,44,48,59,60,63,66,66,67,67,69,69,70,71,73,76,76,79,86,86,92,92,93,93};
int param0_7[] = {6,82,-88,-46,-60,70,-54,-96,-94,46,-52,48,-26,-50,-92,-92,6,-6,42,0,-66,-96,66,6,-68,-30,-54,76,60,30,72,-66,-12,-74};
int param0_8[] = {0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {62,54,36,35,36,91,45,87,74,49,15,15,73,77,63,70,74,65,11,18};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {10,3,1,2,14,27,34,28,13,16};
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