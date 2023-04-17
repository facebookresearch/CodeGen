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

int f_gold ( int a [ ], int size ) {
  int max_so_far = INT_MIN, max_ending_here = 0, start = 0, end = 0, s = 0;
  for ( int i = 0;
  i < size;
  i ++ ) {
    max_ending_here += a [ i ];
    if ( max_so_far < max_ending_here ) {
      max_so_far = max_ending_here;
      start = s;
      end = i;
    }
    if ( max_ending_here < 0 ) {
      max_ending_here = 0;
      s = i + 1;
    }
  }
  return ( end - start + 1 );
}


int f_filled ( int a [ ], int size ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {7,7,16,20,21,22,34,34,37,37,49,53,54,55,58,59,60,66,67,68,73,80,80,88,90,98,99,99};
int param0_1[] = {-90,-98,-10,-84,24};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_3[] = {94,2,83,94,10,94,58,99,60,19,3,71,36,84,71,14,50,15};
int param0_4[] = {-98,-96,-70,-64,-56,-38,-34,-24,-22,-2,26,32,36,50,62,70,70,72,72,74,78,82,84,86};
int param0_5[] = {0,1,0,1,1,1,0,0,0,1,1,1,0,0,1,0,1,1,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,1,1,0,1,0,1,0};
int param0_6[] = {1,2,2,5,13,14,15,18,21,34,42,48,50,63,67,68,69,75,80,80,81,83,84,89,90,90,91,92,95,98};
int param0_7[] = {-88,-10,-88,-90,92,14,68,-90,-86};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {28,39,90,39,12,90,24,89,54,44,3,26,44,36,67,92,3,79,10,45,22,21,39,91,2,5,72,21,55,48,75,47};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {21,2,19,14,13,35,22,5,24,27};
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