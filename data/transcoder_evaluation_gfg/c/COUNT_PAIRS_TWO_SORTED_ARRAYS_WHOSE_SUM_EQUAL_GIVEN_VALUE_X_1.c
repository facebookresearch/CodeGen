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

int f_gold ( int arr1 [ ], int arr2 [ ], int m, int n, int x ) {
  int count = 0;
  unordered_set < int > us;
  for ( int i = 0;
  i < m;
  i ++ ) us . insert ( arr1 [ i ] );
  for ( int j = 0;
  j < n;
  j ++ ) if ( us . find ( x - arr2 [ j ] ) != us . end ( ) ) count ++;
  return count;
}


int f_filled ( int arr1 [ ], int arr2 [ ], int m, int n, int x ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {1,2,5,5,9,11,12,14,16,18,35,36,39,44,50,52,52,59,69,81,82,84,85,87,87,87,88,88,89,90,90,92,97};
int param0_1[] = {52,28,-38,78,-86,78,-48,-70,-80,28,-8,60,-28,90,6,76,32,-54,30,30,-32,-24,-36,62,36,-66,56,92,-20,90,32};
int param0_2[] = {0,0,0,0,0,0,0,0,1,1,1,1,1,1,1};
int param0_3[] = {91,95,13,13,76,18,36,86,26,13,17,68,58,42,38,9,42,90,14,74,38,64,15};
int param0_4[] = {-96,-94,-94,-92,-74,-70,-66,-54,-48,-20,-18,-10,-6,-2,2,18,36,48,52,58,68,74,88,90,94};
int param0_5[] = {1,1,1,0,0,0,1,1,0,0,1,0,1,0,1,1,1,0,1,0,1,0,0,1,1,1,1,0,1,1,0};
int param0_6[] = {7,18,19,20,24,25,25,27,30,35,39,42,58,59,63,64,64,66,66,68,69,77,86,93};
int param0_7[] = {86,44,10,80,12,52,-92,2,42,-32,-14,2,-42,40,96,22,58,-90,-20,22,96,10,-92,-28,-28,80,36,72,-2,32,-46,62,-58,20,22,32,-98,-2,-42,-90,10,70,54,-32};
int param0_8[] = {0,0,1,1,1,1};
int param0_9[] = {43,2,4,99,45,80,27,8,64,77,57,55,71,67,51,42,58,70,5,62,55,20,61,47,66,80,70,24,56,22,58,63,61,41,20,97,47};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {5,5,8,20,20,24,25,29,34,37,43,45,48,49,59,60,68,70,70,72,72,75,76,77,79,81,84,85,86,88,95,96,96};
int param1_1[] = {-88,-32,30,32,-46,62,-92,-90,-18,-18,10,16,60,-40,32,-88,60,-82,76,50,86,-82,-48,-68,-42,34,4,0,98,92,-78};
int param1_2[] = {0,0,0,0,0,0,0,1,1,1,1,1,1,1,1};
int param1_3[] = {16,96,8,35,12,27,81,21,32,82,95,81,53,76,72,16,9,16,61,1,36,71,28};
int param1_4[] = {-92,-72,-72,-64,-58,-52,-30,-28,-24,-24,-16,-10,-2,4,12,22,30,38,44,62,64,68,86,88,90};
int param1_5[] = {1,0,1,1,1,0,0,0,0,1,0,1,1,0,0,1,0,1,0,0,1,0,0,0,0,0,1,1,1,0,0};
int param1_6[] = {2,2,18,20,22,22,31,35,36,40,41,41,41,42,42,43,45,61,79,83,87,91,95,96};
int param1_7[] = {-4,-76,-98,14,30,-10,-10,62,88,-94,-74,-82,84,44,58,8,-42,-66,-18,68,-78,42,-32,38,-98,38,-78,42,86,-38,-6,-72,-44,8,-6,-48,-62,82,94,-92,-56,28,-54,34};
int param1_8[] = {0,0,1,1,1,1};
int param1_9[] = {11,66,41,17,93,25,24,17,12,33,62,86,48,68,36,36,39,82,7,66,5,48,27,9,56,6,61,91,98,74,61,63,98,96,57,63,85};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {17,30,13,11,19,18,22,26,5,24};
    int param3[] = {29,27,11,12,14,19,18,36,3,29};
    int param4[] = {32,17,8,15,21,29,18,31,5,21};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i],param4[i]) == f_gold(param0[i],param1[i],param2[i],param3[i],param4[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}