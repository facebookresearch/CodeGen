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

long long int f_gold ( int A [ ], int B [ ], int m, int n ) {
  long long int dp [ n + 1 ] [ m + 1 ];
  memset ( dp, 0, sizeof ( dp ) );
  for ( int i = 1;
  i <= n;
  i ++ ) for ( int j = i;
  j <= m;
  j ++ ) dp [ i ] [ j ] = max ( ( dp [ i - 1 ] [ j - 1 ] + ( A [ j - 1 ] * B [ i - 1 ] ) ), dp [ i ] [ j - 1 ] );
  return dp [ n ] [ m ];
}


long long int f_filled ( int A [ ], int B [ ], int m, int n ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {7,9,22,68};
int param0_1[] = {24,40,98,58,-24,24,76,48,-92,-16,-46,-48,-70,88,66,2,44,36,34,34,46,90,-80,-24,-58,68,72,-20,-62,-40};
int param0_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param0_3[] = {32,15,41,41,4,42,22,33,33,11,68,5,41,80,39,15,36,75,41,11,25,40,50,19,39,12,75,28,52,20,63,5,27,53,19,62,98,72,10,90,74,93,52,81,91,65,90,93};
int param0_4[] = {-94,-76,-68,-50,-28,-20,18,24,30,54,74,84,98};
int param0_5[] = {1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,0,1,1,0,1,1,1,0,0,0,0,1,0,0,0,0,1,0,0,1,1,1,0,1,0};
int param0_6[] = {14,27,43,49};
int param0_7[] = {78,-26,-12,38,-90};
int param0_8[] = {0,1,1,1};
int param0_9[] = {12,69,57,7,52,14,15,83,67,57,15,86,81,43,1,64,45,68,30,23,14,70,13,51,23,33,98,68,24,43,12,82,46};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1_0[] = {14,22,54,58};
int param1_1[] = {30,-88,6,-26,-76,14,-80,-30,-58,76,40,-28,-54,38,-60,-60,88,-80,-22,90,50,-48,68,-26,26,-2,68,-16,88,-72};
int param1_2[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1};
int param1_3[] = {80,18,9,29,62,89,4,40,47,15,35,82,22,97,63,54,7,58,64,73,54,79,21,21,20,19,56,42,6,97,7,34,55,35,57,86,73,88,20,29,48,52,8,77,2,12,6,47};
int param1_4[] = {-88,-80,-78,-68,-44,-38,42,50,62,68,70,80,92};
int param1_5[] = {1,0,0,1,1,1,1,1,1,0,0,1,1,0,1,1,0,0,1,0,1,1,0,1,0,1,1,0,1,0,0,1,0,0,1,0,1,0,1,0,1};
int param1_6[] = {51,59,76,83};
int param1_7[] = {14,50,-6,-38,80};
int param1_8[] = {0,0,0,1};
int param1_9[] = {12,48,57,40,47,36,22,50,68,98,77,78,39,55,87,75,65,27,33,27,70,34,67,71,84,33,7,61,3,9,67,92,60};
int *param1[10] = {param1_0,param1_1,param1_2,param1_3,param1_4,param1_5,param1_6,param1_7,param1_8,param1_9};
    int param2[] = {3,22,22,30,11,21,2,3,3,17};
    int param3[] = {2,22,19,25,8,33,2,2,2,32};
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