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

int f_gold ( int arr1 [ ], int arr2 [ ], int n ) {
  int index = n;
  int left = 0, right = n - 1;
  while ( left <= right ) {
    int mid = ( left + right ) / 2;
    if ( arr2 [ mid ] == arr1 [ mid ] ) left = mid + 1;
    else {
      index = mid;
      right = mid - 1;
    }
  }
  return index;
}


int f_filled ( int arr1 [ ], int arr2 [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {7,18,19,25,26,27,31,39,44,46,59,60,66,72,78,83,84,92,94};
int param0_1[] = {-14,-56,92,-90,96,-84,64,-38,-20,84,56,92,18,-78,98,-96,-60,88,-52,-28,30,-90,14,76,56,20,-18,-94,-82,-2,96,-60,-64,-90,42,6,20,-38,82,-86,-4,82,54,-88};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {13,64,73,50,73,19,92,10,64,79,58,41,97,53,53,10,96,45,47,38,99};
int param0_4[] = {-96,-94,-90,-90,-78,-70,-64,-64,-58,-58,-52,-40,-36,-34,-34,-30,-26,-2,0,2,14,18,24,28,28,30,34,40,42,48,66,72,86,90,92,98};
int param0_5[] = {1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,1,0};
int param0_6[] = {10,51,74,74,75,80,90};
int param0_7[] = {-44,48,20,-38,-48,-26,56,-62,-94,-18,30,66,-16,80,96,-40,-80,32,88,-56,-76,16,72,-94,4,-34,-92,70,-90,-54,64,-90};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {19,53,13,91,52,62,39,84,68,45,32,40,13,68,79,76,11,42,76,30,81,3,30,15,85,76,1};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {2,5,12,13,17,20,22,46,51,63,64,66,66,76,87,87,90,91,96};
int param1_1[] = {54,44,-50,26,4,-26,-76,98,-14,36,82,0,-60,18,52,82,-12,-8,-26,-58,22,-70,24,48,56,-46,92,98,-50,-72,-66,8,40,12,-80,-86,90,-30,76,-92,80,-62,0,-48};
int param1_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_3[] = {24,42,54,13,88,63,50,73,64,66,86,84,53,4,44,58,44,42,36,94,34};
int param1_4[] = {-94,-92,-90,-88,-86,-82,-82,-80,-76,-74,-64,-60,-58,-46,-44,-36,-30,-30,-30,-18,-16,-8,-6,12,14,20,26,38,40,42,42,68,78,82,88,98};
int param1_5[] = {0,0,1,1,0,0,1,0,1,1,0,1,0,1,1,1,1,1,1,1,0};
int param1_6[] = {12,20,36,38,61,64,93};
int param1_7[] = {-76,92,-66,20,86,40,64,16,54,-6,54,-88,-24,38,86,2,30,70,98,-46,28,34,40,-88,-96,92,22,14,-36,-96,-48,-72};
int param1_8[] = {0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_9[] = {33,65,36,82,30,95,42,33,9,21,25,90,54,59,21,45,3,93,67,50,97,72,77,54,75,8,6};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {11,26,31,13,29,19,5,28,14,25};
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