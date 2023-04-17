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

int f_gold ( int k, int x [ ], int y [ ], int n ) {
  int dis [ n ];
  for ( int i = 0;
  i < n;
  i ++ ) dis [ i ] = x [ i ] * x [ i ] + y [ i ] * y [ i ];
  sort ( dis, dis + n );
  return dis [ k - 1 ];
}


int f_filled ( int k, int x [ ], int y [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0[] = {1,18,13,15,11,27,25,33,4,7};
    int param1_0[] = {7,91};
int param1_1[] = {-44,32,-78,40,12,-54,-80,94,66,50,-52,20,84,-76,84,-90,-62,44,-26,-44,-12,-14,38,44,76,-60,98,-88,38,48,84,-76,-70,34};
int param1_2[] = {0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_3[] = {68,59,97,56,66,12,22,62,26,14,9,74,7,47,58,20,79,56,43,98,60,52,88,66,20,13,25,36,3};
int param1_4[] = {-82,-66,-56,-54,-36,-20,0,8,18,20,22,56,56,66,76,82,90,98};
int param1_5[] = {0,0,1,1,0,0,0,1,0,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,1,1,0,1,0,0,0};
int param1_6[] = {3,6,6,7,9,10,11,13,14,17,17,20,20,22,31,34,38,39,51,55,58,59,59,61,62,71,75,75,77,79,79,81,87,90,92,92,92,94,95,96};
int param1_7[] = {-60,6,-66,-84,-86,-26,-2,36,-40,4,8,4,70,-16,-46,-94,90,-68,54,42,50,96,-16,50,92,12,-34,-42,90,82,24,32,-84,-14,-6,-76,68,-20,-90,12,14,54,-98,-34,20,46,-32,44,-34};
int param1_8[] = {0,0,0,0,1,1,1};
int param1_9[] = {58,81,35,53,29,76,58,77,21,39,1,49,77,43,88};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2_0[] = {15,83};
int param2_1[] = {74,26,-28,-86,-98,44,82,-2,-56,4,90,-14,-22,50,-14,8,-58,-70,84,-24,-54,82,66,60,52,2,-54,2,42,-8,88,22,-68,20};
int param2_2[] = {0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param2_3[] = {47,12,60,97,28,75,81,14,31,69,66,60,77,20,11,78,4,52,47,67,11,50,89,23,81,62,53,95,14};
int param2_4[] = {-88,-72,-56,-44,-44,-30,-24,-12,-10,-4,4,6,8,34,56,72,74,94};
int param2_5[] = {0,1,0,1,0,0,1,1,1,0,1,0,0,0,0,1,1,0,1,1,1,1,0,0,1,0,1,0,0,0,1,1,0,0,0,1};
int param2_6[] = {2,3,5,11,13,14,16,17,17,17,18,18,23,24,27,33,37,41,42,45,47,47,56,58,61,65,67,68,71,72,75,76,78,83,86,92,93,94,96,96};
int param2_7[] = {12,52,66,-58,94,36,-92,-2,-78,80,-90,20,-40,32,76,-68,64,52,80,-76,-48,36,-46,6,74,70,-4,-26,96,-10,50,-94,-88,56,-88,54,-42,-34,-66,14,-78,32,-32,90,-68,-18,-26,-56,-8};
int param2_8[] = {0,1,1,1,1,1,1};
int param2_9[] = {88,77,5,55,78,80,70,2,68,63,80,85,81,67,88};
int *param2[10] = {param2_0,param2_1,param2_2,param2_3,param2_4,param2_5,param2_6,param2_7,param2_8,param2_9};
    int param3[] = {1,25,17,28,14,25,33,26,3,12};
    for(int i = 0; i < len(param0); ++i)
    {
        if(f_filled(param0[i],param1[i],param2[i],param3[i]) == f_gold(param0[i],param1[i],param2[i],param3[i]))
        {
            n_success+=1;
        }
    }
    printf("#Results:", " ", n_success, ", ", len(param0));
    return 0;
}