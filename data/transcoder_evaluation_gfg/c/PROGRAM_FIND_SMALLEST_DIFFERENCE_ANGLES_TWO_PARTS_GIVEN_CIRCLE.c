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
  int l = 0, sum = 0, ans = 360;
  for ( int i = 0;
  i < n;
  i ++ ) {
    sum += arr [ i ];
    while ( sum >= 180 ) {
      ans = min ( ans, 2 * abs ( 180 - sum ) );
      sum -= arr [ l ];
      l ++;
    }
    ans = min ( ans, 2 * abs ( 180 - sum ) );
  }
  return ans;
}


int f_filled ( int arr [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,4,5,5,13,14,14,16,19,20,30,31,32,33,35,38,38,42,44,44,48,48,52,58,60,64,65,66,68,69,70,70,71,72,73,79,81,83,83,84,86,87,88,88,91,92,95,95,98};
int param0_1[] = {-56,88,-50,70,20,58,42,-56,-52,-78,98,20,-26,4,20,-66,-46,-58,74,74,-72,2,16,-78,-4,10,58,60,-46,-2,32,-96,24,-6,90,-64,-24,-38,26,66,-42,-86,48,92,28,6,-54,-6};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {52,67,62};
int param0_4[] = {-56,-22,32,42,66};
int param0_5[] = {1,0,1,0,0,0,0,0,1,0,0,1,1,1,1,1,0};
int param0_6[] = {38,46,58,72};
int param0_7[] = {16,62,90,40,30,-56,-92,-56,60,42,-64,92,-30,-70,42,-48,-54,54,48,94,-44,-46,10,48,22,-24,-62,34,60,24,-60,50,40,34};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {86,43,74,84,86,14,45,7,92,36,79,13,67,18,96,77,13,22,28,36,57,56,99,57,8,48,5,79,65,64,96,6,36,91,53,55,11,12,80,99,50,40,4,9,52,41};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {27,29,25,1,4,10,2,20,37,40};
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