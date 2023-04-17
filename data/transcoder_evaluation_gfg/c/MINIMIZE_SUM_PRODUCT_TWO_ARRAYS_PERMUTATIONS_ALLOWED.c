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

int f_gold ( int A [ ], int B [ ], int n ) {
  sort ( A, A + n );
  sort ( B, B + n );
  int result = 0;
  for ( int i = 0;
  i < n;
  i ++ ) result += ( A [ i ] * B [ n - i - 1 ] );
  return result;
}


int f_filled ( int A [ ], int B [ ], int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {31,85};
int param0_1[] = {22,-6,84,70,84,6,28,-74,-14,68,22,90,-10};
int param0_2[] = {0,0,0,0,0,0,0,0,1,1,1,1,1,1,1};
int param0_3[] = {12,33,93,2,83,9,61,84,9,69,2};
int param0_4[] = {-92,-88,-84,-78,-78,-76,-66,-54,-52,-48,-46,-44,-40,-34,-32,-24,-20,-14,-6,-4,2,6,10,10,22,26,32,36,36,40,46,48,56,58,64,76,80,80,80,84,84,84,92};
int param0_5[] = {1,0,1,1,0,1,1,0,1,0,0,1,1,1,0,0,0,0,0,0,1,0,1,1,0,1,0,1,1,0,0,0,1,0};
int param0_6[] = {4,6,6,20,22,23,26,39,40,47,50,68,68,70,73,77,80,82,85};
int param0_7[] = {78,60,-8,46,-12};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {60,66,84,99,85,89,28,97,85,71,53,93,23,9,45,26,49,95,64,33,70,34,10,1,68,39,53,12};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {18,33};
int param1_1[] = {2,-48,-36,-4,-22,-98,-74,-92,-72,-4,48,-32,94};
int param1_2[] = {0,0,0,0,0,1,1,1,1,1,1,1,1,1,1};
int param1_3[] = {85,92,92,1,54,31,69,4,39,81,52};
int param1_4[] = {-98,-90,-82,-80,-76,-66,-62,-62,-62,-50,-50,-50,-32,-30,-14,-12,4,6,12,14,16,30,30,30,32,34,40,42,50,52,56,58,60,62,62,64,66,68,78,82,86,90,94};
int param1_5[] = {0,1,1,1,0,0,0,0,0,1,0,1,0,0,0,0,1,0,1,1,0,1,1,0,0,1,1,0,0,0,0,1,1,1};
int param1_6[] = {2,3,15,21,22,26,35,37,37,38,57,59,62,63,64,76,81,85,91};
int param1_7[] = {-72,-80,-30,16,-38};
int param1_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param1_9[] = {37,33,33,77,78,34,28,1,63,15,51,50,90,22,71,23,68,55,2,22,31,54,76,36,2,27,96,89};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {1,6,14,7,26,32,17,2,17,15};
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