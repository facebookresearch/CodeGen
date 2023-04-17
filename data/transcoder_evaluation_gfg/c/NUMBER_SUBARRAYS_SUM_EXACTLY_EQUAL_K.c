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

int f_gold ( int arr [ ], int n, int sum ) {
  unordered_map < int, int > prevSum;
  int res = 0;
  int currsum = 0;
  for ( int i = 0;
  i < n;
  i ++ ) {
    currsum += arr [ i ];
    if ( currsum == sum ) res ++;
    if ( prevSum . find ( currsum - sum ) != prevSum . end ( ) ) res += ( prevSum [ currsum - sum ] );
    prevSum [ currsum ] ++;
  }
  return res;
}


int f_filled ( int arr [ ], int n, int sum ) {}

int main(void) {
    int n_success = 0;
    int param0_0[] = {9,18,27,52,70,91};
int param0_1[] = {60,-88,-48,90,-28,20,18,34,-58,76,-78,-18,68,-48,8,34,60,-34,-10,32,78,-84,-22,54,-18,-82,-70,-58,-20,-76,88,-30,-6,68};
int param0_2[] = {0,0,0,0,0,0,0,0,1,1,1,1};
int param0_3[] = {67,39,22,32,59,44,86,26,46,60,99,12,32,46,16,22,45,85,21,92,77,50,65,23,93,26,23,20,32,83,60,22,11,45,99,31,72};
int param0_4[] = {-86,-84,-82,-82,-28,-12,4,24,62,72};
int param0_5[] = {1,0,0,1,0,1,1,1,0,1,1,1,0,0,1,1,1,1};
int param0_6[] = {8,20,25,27,28,28,30,31,32,36,39,41,51,53,53,54,56,58,59,77,78,85,88,92,99};
int param0_7[] = {60,40,-96,-76,-34,-18,38,-62,50,56,64,-94,-50,50,-80,42,-66,-42,68,70,78,-18,-24,-48,-92,64,14,24,-94,-98,18,44,-58};
int param0_8[] = {0,0,0,0,1,1,1,1,1,1,1,1};
int param0_9[] = {73,52,37,80,4,26,3,76,32,79,31,32,8,87,42,50,51};
int *param0[10] = {param0_0,param0_1,param0_2,param0_3,param0_4,param0_5,param0_6,param0_7,param0_8,param0_9};
    int param1[] = {5,32,11,25,7,16,13,22,11,8};
    int param2[] = {4,30,11,25,5,13,18,17,8,14};
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