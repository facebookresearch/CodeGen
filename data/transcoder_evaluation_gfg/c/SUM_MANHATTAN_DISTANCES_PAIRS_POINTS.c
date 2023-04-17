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

int f_gold ( int x [ ], int y [ ], int n ) {
  int sum = 0;
  for ( int i = 0;
  i < n;
  i ++ ) for ( int j = i + 1;
  j < n;
  j ++ ) sum += ( abs ( x [ i ] - x [ j ] ) + abs ( y [ i ] - y [ j ] ) );
  return sum;
}


int f_filled ( int x [ ], int y [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {2,4,6,6,8,11,12,13,14,19,20,22,24,28,29,30,32,35,37,44,48,49,51,51,56,59,59,62,65,68,68,68,72,75,77,78,89,89,91,93,95,99};
int param0_1[] = {16,76,2,42,-24,-82,68,-2,98,-42,-72,28,-22,-52,28,-38,36,66,84,64,-28,86,52,84,-98,-30};
int param0_2[] = {0,0,0,0,0,1,1,1,1,1};
int param0_3[] = {61,37,57,99,22,72,38,85,23,85,15,4,49,9,15,25,7,63,79,6,85,30,12,34,38,6,59,62,59,34,72,97,70,44,95,58,99};
int param0_4[] = {-96,-86,-82,-72,-72,-64,-62,-60,-56,-56,-56,-54,-52,-40,-36,-30,-10,10,18,26,28,56,56,56,64,90,92,94};
int param0_5[] = {1,0,1,1,1,0,1};
int param0_6[] = {6,10,24,25,31,41,43,45,47,65,67,90};
int param0_7[] = {-74,92,34,56,-54,-98,-76,-34,16,32,-4,-16,22,90,-52,-90,-60,70,-40,78,96,-68,78,-56,-94};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {20,32};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {6,19,19,22,25,27,31,33,34,35,37,38,38,44,46,50,51,55,58,58,64,64,64,64,65,66,66,66,67,70,75,78,79,81,81,81,82,84,84,86,94,96};
int param1_1[] = {-34,92,-24,-62,28,72,-10,10,8,90,-72,-24,50,-46,52,58,68,-62,-64,-78,-12,24,62,-30,62,-60};
int param1_2[] = {0,0,0,0,1,1,1,1,1,1};
int param1_3[] = {72,41,77,62,78,36,75,28,91,39,32,56,60,64,21,15,80,85,28,22,53,58,69,62,60,48,66,91,38,66,54,5,24,1,49,71,49};
int param1_4[] = {-98,-98,-96,-96,-82,-80,-80,-68,-62,-60,-46,-38,-26,-26,-20,-18,16,22,24,26,34,46,52,52,74,76,90,92};
int param1_5[] = {1,0,1,0,0,1,1};
int param1_6[] = {4,7,11,19,21,39,57,80,84,93,94,97};
int param1_7[] = {14,20,24,-92,58,12,78,78,-90,96,-44,36,30,-46,-30,-80,26,-2,26,28,-16,-50,-2,-36,-8};
int param1_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_9[] = {23,50};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {37,24,5,26,26,3,10,21,23,1};
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