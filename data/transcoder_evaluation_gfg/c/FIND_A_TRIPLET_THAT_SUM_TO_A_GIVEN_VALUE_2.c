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

bool f_gold ( int A [ ], int arr_size, int sum ) {
  for ( int i = 0;
  i < arr_size - 2;
  i ++ ) {
    unordered_set < int > s;
    int curr_sum = sum - A [ i ];
    for ( int j = i + 1;
    j < arr_size;
    j ++ ) {
      if ( s . find ( curr_sum - A [ j ] ) != s . end ( ) ) {
        printf ( "Triplet is %d, %d, %d", A [ i ], A [ j ], curr_sum - A [ j ] );
        return true;
      }
      s . insert ( A [ j ] );
    }
  }
  return false;
}


bool f_filled ( int A [ ], int arr_size, int sum ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,6,8,8,9,11,13,13,15,17,21,24,38,38,42,43,46,46,47,54,55,56,57,58,60,60,60,62,63,63,65,66,67,67,69,81,84,84,85,86,95,99};
int param0_1[] = {20,-86,-24,38,-32,-64,-72,72,68,94,18,-60,-4,-18,-18,-70,6,-86,46,-16,46,-28};
int param0_2[] = {0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param0_3[] = {13,96,31,39,23,39,50,10,21,64,41,54,44,97,24,91,79,86,38,49,77,71,8,98,85,36,37,65,42,48};
int param0_4[] = {-86,-68,-58,-56,-54,-54,-48,-40,-36,-32,-26,-16,-14,-12,-12,-4,-4,-4,0,10,22,22,30,54,62,68,88,88};
int param0_5[] = {0,1,1,1,1,0,0};
int param0_6[] = {8,8,9,13,20,24,29,52,53,96};
int param0_7[] = {18,-92,-10,26,58,-48,38,66,-98,-72,4,76,-52,20,60,-56,96,60,-10,-26,-64,-66,-22,-86,74,82,2,-14,76,82,40,70,-40,-2,-46,-38,22,98,58};
int param0_8[] = {1,1,1,1};
int param0_9[] = {72};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {27,21,17,17,21,5,9,30,2,0};
    int param2[] = {24,20,13,18,25,3,8,30,2,0};
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