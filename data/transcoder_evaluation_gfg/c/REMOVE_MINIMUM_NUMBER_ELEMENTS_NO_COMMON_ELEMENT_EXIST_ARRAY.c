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

int f_gold ( int a [ ], int b [ ], int n, int m ) {
  unordered_map < int, int > countA, countB;
  for ( int i = 0;
  i < n;
  i ++ ) countA [ a [ i ] ] ++;
  for ( int i = 0;
  i < m;
  i ++ ) countB [ b [ i ] ] ++;
  int res = 0;
  for ( auto x : countA ) if ( countB . find ( x . first ) != countB . end ( ) ) res += min ( x . second, countB [ x . first ] );
  return res;
}


int f_filled ( int a [ ], int b [ ], int n, int m ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {4,7,10,12,12,24,29,38,45,51,53,54,59,68,72,73,85,86,88,92,92,95};
int param0_1[] = {-6,48,-70,14,-86,56,80,-64,64,-88,-14,78,14,-18,52,2,22,88};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1};
int param0_3[] = {10,93,2,16,36,49,36,86,6,99,95,2};
int param0_4[] = {-98,-96,-80,-64,-42,-30,-6,10,62,66,82};
int param0_5[] = {1,1,0,1,1};
int param0_6[] = {7,11,13,15,21,33,36,39,66,99};
int param0_7[] = {-40};
int param0_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_9[] = {79,91,31,16,28,45,37,43,73,73,76,28,71,60,64,60,99,36,47,38,65,34,22,94,84,51,72,45,71,2};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {7,9,17,23,25,26,29,32,35,56,56,58,59,59,62,63,72,82,85,86,95,97};
int param1_1[] = {-62,-58,60,-30,42,8,66,-48,-18,64,-76,-90,-48,-90,-24,64,-88,-98};
int param1_2[] = {0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1};
int param1_3[] = {99,28,7,21,62,89,82,41,43,77,8,14};
int param1_4[] = {-62,-50,-42,24,44,46,52,54,60,72,72};
int param1_5[] = {1,1,1,0,0};
int param1_6[] = {23,36,42,44,62,65,70,78,82,89};
int param1_7[] = {-98};
int param1_8[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_9[] = {58,94,12,27,98,38,75,20,94,43,32,90,23,41,88,2,62,96,53,57,48,79,6,16,11,46,73,57,67,7};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {15,15,10,6,9,4,9,0,31,18};
    int param3[] = {13,9,10,10,6,2,9,0,26,18};
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