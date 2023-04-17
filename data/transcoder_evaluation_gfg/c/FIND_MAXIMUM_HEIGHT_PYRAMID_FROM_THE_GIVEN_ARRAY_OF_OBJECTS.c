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

int f_gold ( int boxes [ ], int n ) {
  sort ( boxes, boxes + n );
  int ans = 1;
  int prev_width = boxes [ 0 ];
  int prev_count = 1;
  int curr_count = 0;
  int curr_width = 0;
  for ( int i = 1;
  i < n;
  i ++ ) {
    curr_width += boxes [ i ];
    curr_count += 1;
    if ( curr_width > prev_width && curr_count > prev_count ) {
      prev_width = curr_width;
      prev_count = curr_count;
      curr_count = 0;
      curr_width = 0;
      ans ++;
    }
  }
  return ans;
}


int f_filled ( int boxes [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {7,8,11,11,14,19,25,27,41,42,46,52,53,54,55,58,59,62,63,66,67,69,74,75,77,81,83,84,88,88,93,93,94};
int param0_1[] = {80,72,40,-78,-72,20,-28,-18,-96,14,20,-60,-56,-92,12,86,16,76,30,76,16};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {12,85,16,78,85,48,91,1,65,22,15,84,67,14,73,19,40,98,4,33,43,37,66,27,45,81,50,95,63,6,95,67,67,97,59,13,21,64,37,80};
int param0_4[] = {-98,-92,-90,-88,-88,-74,-64,-64,-64,-62,-60,-52,-48,-46,-42,-42,-38,-34,-28,-26,-20,-20,-18,-4,0,2,2,6,18,18,18,20,24,24,26,32,40,46,58,66,74,78,90,96};
int param0_5[] = {1,1,1,0,0,1,1,0,1,0,1,1,0,0,1,0,1,0,1,1,1,0,0,0,0,1,0,0,0,1,0,0,1,1,1,1,1,1,1,0};
int param0_6[] = {8,12,13,13,13,16,16,17,19,20,22,23,26,29,29,30,31,37,38,39,39,41,45,45,46,49,49,53,56,62,62,66,67,68,68,69,69,73,77,78,82,85,85,88,88,97};
int param0_7[] = {36,-30,-84,4,-20,-28,-88,72,40,46,-68,-8,18,-24,94,-64,-76,8,82,-6,-98,-70,82,60,-58,-98,86,34,-76,-44,-22,-26,90,20,-38,16,94,94,-78,-42,78,-74,2,8,-62};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {70,54,71,85,51,28,64,85,21,88,27,27,77,50,29,39,57,92,37,93,64,48,22,30,28,23,97,4,3,61,96};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {22,12,35,35,30,21,26,25,26,18};
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